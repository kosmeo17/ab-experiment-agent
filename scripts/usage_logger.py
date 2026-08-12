#!/usr/bin/env python3
"""Write AB Experiment Agent usage logs to da_agent_data.ab_experiment_agent_log via logapi."""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib import error, request

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from ab_setup import (  # noqa: E402
    get_logapi_url,
    get_token,
    load_profile,
    setup_status,
    try_reuse_da_profile,
)

DB = "da_agent_data"
TABLE = "ab_experiment_agent_log"
TZ_CN = timezone(timedelta(hours=8))

STAGE_MAP = {
    "setup": "初始化",
    "session": "会话开始",
    "session_complete": "设计完整收口",
    "session_abort": "设计中途结束",
    "g1_necessity": "必要性",
    "g2_core_metric": "核心指标",
    "g3_audience_scene": "实验对象与触发场景",
    "g4_data_support": "数据支持",
    "g5_grouping": "分组",
    "g6_exclusion": "互斥",
    "g7_caliber": "数据口径",
    "g8_sample_gray": "样本量/灰度",
    "g9_formal_doc": "正式文档",
}

EVENT_TYPES = ("setup", "design_start", "stage_pass", "design_end")
END_STATUS_COMPLETED = "completed"
END_STATUS_ABORTED = "aborted"
END_STATUS_TO_STAGE = {
    END_STATUS_COMPLETED: "session_complete",
    END_STATUS_ABORTED: "session_abort",
}


def new_id(prefix: str = "log") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:16]}"


def now_cn() -> str:
    return datetime.now(TZ_CN).strftime("%Y-%m-%d %H:%M:%S")


def resolve_identity() -> tuple[str, str, str]:
    profile = load_profile()
    reused = try_reuse_da_profile() if not (profile.get("user_name") and profile.get("department")) else {}
    user_name = (profile.get("user_name") or reused.get("user_name") or "").strip()
    department = (profile.get("department") or reused.get("department") or "").strip()
    client_tool = (profile.get("client_tool") or "").strip()
    if not user_name or not department:
        raise RuntimeError("缺少姓名或部门。请先运行 scripts/ab_setup.py --set-profile ...")
    return user_name, department, client_tool


def logapi_insert(row: dict[str, Any]) -> dict[str, Any]:
    token = get_token()
    if not token:
        raise RuntimeError("缺少 Data-ai Token。请先运行 scripts/ab_setup.py --set-token ...")
    url = f"{get_logapi_url().rstrip('/')}/insert"
    payload = {"db": DB, "table": TABLE, "rows": [row]}
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode("utf-8")
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise RuntimeError(f"logapi insert HTTP {exc.code}: {detail}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"logapi 请求失败: {exc.reason}") from exc
    data = json.loads(raw) if raw else {}
    if isinstance(data, dict) and data.get("error"):
        raise RuntimeError(f"logapi insert error: {data.get('error')}")
    return data if isinstance(data, dict) else {"raw": data}


def build_row(
    *,
    event_type: str,
    session_id: str,
    stage_code: str,
    user_query: str | None = None,
    experiment_name: str | None = None,
    result_summary: str | None = None,
    extra: dict[str, Any] | None = None,
    client_tool: str | None = None,
) -> dict[str, Any]:
    if event_type not in EVENT_TYPES:
        raise ValueError(f"event_type 必须是 {EVENT_TYPES}")
    if stage_code not in STAGE_MAP:
        raise ValueError(f"未知 stage_code: {stage_code}")
    user_name, department, profile_tool = resolve_identity()
    row: dict[str, Any] = {
        "log_id": new_id("log"),
        "session_id": session_id,
        "user_name": user_name,
        "department": department,
        "event_time": now_cn(),
        "event_type": event_type,
        "stage_code": stage_code,
        "stage_name": STAGE_MAP[stage_code],
        "client_tool": client_tool or profile_tool or None,
        "user_query": user_query,
        "experiment_name": experiment_name,
        "result_summary": result_summary,
        "extra_json": json.dumps(extra, ensure_ascii=False) if extra else None,
    }
    # drop Nones for consistent insert column set? logapi requires consistent columns;
    # keep keys, convert None to "" for text fields that are nullable — API accepts null.
    return row


def write_event(
    event_type: str,
    *,
    session_id: str | None = None,
    stage: str | None = None,
    end_status: str | None = None,
    user_query: str | None = None,
    experiment_name: str | None = None,
    result_summary: str | None = None,
    extra: dict[str, Any] | None = None,
    client_tool: str | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    extra = dict(extra or {})

    if event_type == "setup":
        session_id = session_id or new_id("sess_setup")
        stage_code = "setup"
    elif event_type == "design_start":
        if not session_id:
            raise ValueError("design_start 需要 --session-id")
        if not (user_query or "").strip():
            raise ValueError("design_start 必须提供 --user-query（owner 原话或确认句）")
        stage_code = "session"
    elif event_type == "design_end":
        if not session_id:
            raise ValueError("design_end 需要 --session-id")
        if not (user_query or "").strip():
            raise ValueError("design_end 必须提供 --user-query（owner 原话或确认句）")
        if not (result_summary or "").strip():
            raise ValueError("design_end 必须提供 --summary")
        status = (end_status or extra.get("end_status") or "").strip()
        if status not in END_STATUS_TO_STAGE:
            raise ValueError("design_end 必须提供 --end-status completed|aborted")
        stage_code = END_STATUS_TO_STAGE[status]
        extra["end_status"] = status
        if not (extra.get("last_completed_gate") or "").strip():
            raise ValueError("design_end 的 --extra-json 必须包含 last_completed_gate")
    elif event_type == "stage_pass":
        if not session_id:
            raise ValueError("stage_pass 需要 --session-id")
        if not stage:
            raise ValueError("stage_pass 需要 --stage")
        if not (user_query or "").strip():
            raise ValueError("stage_pass 必须提供 --user-query（解锁该 Gate 的 owner 原话）")
        if not (result_summary or "").strip():
            raise ValueError("stage_pass 必须提供 --summary")
        if not extra:
            raise ValueError("stage_pass 必须提供 --extra-json（confirmed/pending 等确认摘要）")
        stage_code = stage
    else:
        raise ValueError(event_type)

    # Forbid secrets in extra
    if extra:
        banned = ("token", "password", "secret", "authorization", "cookie")
        blob = json.dumps(extra, ensure_ascii=False).lower()
        if any(b in blob for b in banned):
            raise ValueError("extra_json 不得包含 token/密钥类字段")

    row = build_row(
        event_type=event_type,
        session_id=session_id,
        stage_code=stage_code,
        user_query=user_query,
        experiment_name=experiment_name,
        result_summary=result_summary,
        extra=extra or None,
        client_tool=client_tool,
    )
    if dry_run:
        return {"dry_run": True, "row": row}
    result = logapi_insert(row)
    return {
        "inserted": result,
        "row": {
            "log_id": row["log_id"],
            "session_id": row["session_id"],
            "event_type": event_type,
            "stage_code": stage_code,
            "end_status": extra.get("end_status") if event_type == "design_end" else None,
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="写入 AB 实验助手使用日志")
    parser.add_argument("--event", required=True, choices=EVENT_TYPES)
    parser.add_argument("--session-id", help="设计会话 ID；setup 可省略")
    parser.add_argument("--stage", choices=[k for k in STAGE_MAP if k.startswith("g")], help="stage_pass 必填")
    parser.add_argument(
        "--end-status",
        choices=[END_STATUS_COMPLETED, END_STATUS_ABORTED],
        help="design_end 必填：completed=完整收口，aborted=中途结束",
    )
    parser.add_argument("--user-query", default=None)
    parser.add_argument("--experiment-name", default=None)
    parser.add_argument("--summary", default=None, help="result_summary")
    parser.add_argument("--client-tool", choices=["cursor", "codex", "claude"], default=None)
    parser.add_argument("--extra-json", default=None, help="扩展 JSON 字符串")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--check-setup", action="store_true", help="仅检查初始化是否完整")
    args = parser.parse_args(argv)

    if args.check_setup:
        status = setup_status()
        print(json.dumps(status, ensure_ascii=False, indent=2))
        return 0 if status["complete"] else 2

    extra = json.loads(args.extra_json) if args.extra_json else None
    try:
        out = write_event(
            args.event,
            session_id=args.session_id,
            stage=args.stage,
            end_status=args.end_status,
            user_query=args.user_query,
            experiment_name=args.experiment_name,
            result_summary=args.summary,
            extra=extra,
            client_tool=args.client_tool,
            dry_run=args.dry_run,
        )
    except Exception as exc:  # noqa: BLE001 - CLI boundary
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
