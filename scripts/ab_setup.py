#!/usr/bin/env python3
"""AB 实验助手本地初始化：姓名、部门、Data-ai Token。

落盘（勿提交 Git）：
  ~/.ab-experiment-agent/profile.yaml
  ~/.ab-experiment-agent/agent.env

Token 同时写入 DATA_AI_MCP_TOKEN 与 LOGAPI_TOKEN（同值），供 logapi 写使用日志。
"""

from __future__ import annotations

import argparse
import getpass
import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - stdlib fallback
    yaml = None

HOME_DIR = Path.home() / ".ab-experiment-agent"
PROFILE_PATH = HOME_DIR / "profile.yaml"
AGENT_ENV_PATH = HOME_DIR / "agent.env"

MCP_TOKEN_ENV = "DATA_AI_MCP_TOKEN"
LOGAPI_TOKEN_ENV = "LOGAPI_TOKEN"
LOGAPI_URL_ENV = "LOGAPI_BASE_URL"
DEFAULT_LOGAPI_URL = "https://data-ai.hellotalk8.com/logapi/v1"

NAME_RE = re.compile(r"^\S+\s+\S+")


def mask_token(token: str) -> str:
    token = (token or "").strip()
    if not token:
        return "(empty)"
    if len(token) <= 8:
        return "***"
    return f"{token[:4]}...{token[-4:]}"


def ensure_home() -> None:
    HOME_DIR.mkdir(parents=True, exist_ok=True)
    HOME_DIR.chmod(0o700)


def _parse_simple_yaml(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, val = line.partition(":")
        out[key.strip()] = val.strip().strip("'\"")
    return out


def _dump_simple_yaml(data: dict[str, str]) -> str:
    lines = ["# AB Experiment Agent profile（勿提交 Git）"]
    for key, value in data.items():
        lines.append(f"{key}: {value}")
    return "\n".join(lines) + "\n"


def load_profile() -> dict[str, str]:
    if not PROFILE_PATH.exists():
        return {}
    text = PROFILE_PATH.read_text(encoding="utf-8")
    if yaml is not None:
        data = yaml.safe_load(text) or {}
        if not isinstance(data, dict):
            return {}
        return {str(k): str(v) for k, v in data.items() if v is not None}
    return _parse_simple_yaml(text)


def save_profile(user_name: str, department: str, client_tool: str | None = None) -> Path:
    user_name = (user_name or "").strip()
    department = (department or "").strip()
    if not NAME_RE.match(user_name):
        raise ValueError("姓名格式须为「中文名 英文名」，例如：王璐 Kosmeo")
    if not department:
        raise ValueError("部门不能为空")
    ensure_home()
    data = load_profile()
    data["user_name"] = user_name
    data["department"] = department
    if client_tool:
        data["client_tool"] = client_tool.strip()
    if yaml is not None:
        PROFILE_PATH.write_text(
            "# AB Experiment Agent profile（勿提交 Git）\n"
            + yaml.safe_dump(data, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )
    else:
        PROFILE_PATH.write_text(_dump_simple_yaml(data), encoding="utf-8")
    PROFILE_PATH.chmod(0o600)
    return PROFILE_PATH


def _parse_env_file(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not path.exists():
        return out
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        out[key.strip()] = val.strip().strip("'\"")
    return out


def _upsert_env_file(path: Path, updates: dict[str, str]) -> None:
    ensure_home()
    existing_lines: list[str] = []
    if path.exists():
        existing_lines = path.read_text(encoding="utf-8").splitlines()
    keys = set(updates)
    kept: list[str] = []
    seen: set[str] = set()
    for line in existing_lines:
        stripped = line.strip()
        if stripped.startswith("#") or "=" not in stripped:
            kept.append(line)
            continue
        key = stripped.split("=", 1)[0].strip()
        if key in keys:
            if key not in seen:
                kept.append(f"{key}={updates[key]}")
                seen.add(key)
            continue
        kept.append(line)
    for key, value in updates.items():
        if key not in seen:
            kept.append(f"{key}={value}")
    if not kept or not any(l.startswith("#") for l in kept):
        kept.insert(0, "# AB Experiment Agent agent.env（勿提交 Git）")
    path.write_text("\n".join(kept) + "\n", encoding="utf-8")
    path.chmod(0o600)


def load_env(*, prefer_local: bool = True) -> None:
    """Load tokens into os.environ.

    Priority when prefer_local=True (default):
      1) ~/.ab-experiment-agent/agent.env
      2) existing process env
      3) ~/.da_agent_env / ~/.da/{user}/agent.env
    """
    local = _parse_env_file(AGENT_ENV_PATH)
    if prefer_local:
        for key, value in local.items():
            if value:
                os.environ[key] = value
    else:
        for key, value in local.items():
            if value and not os.environ.get(key):
                os.environ[key] = value

    for path in (Path.home() / ".da_agent_env", Path.home() / ".da" / getpass.getuser() / "agent.env"):
        for key, value in _parse_env_file(path).items():
            if value and not os.environ.get(key):
                os.environ[key] = value


def get_token() -> str:
    load_env(prefer_local=True)
    # Prefer values from AB local agent.env when present.
    local = _parse_env_file(AGENT_ENV_PATH)
    return (
        (local.get(MCP_TOKEN_ENV) or local.get(LOGAPI_TOKEN_ENV) or "").strip()
        or (os.getenv(MCP_TOKEN_ENV) or os.getenv(LOGAPI_TOKEN_ENV) or "").strip()
    )


def get_logapi_url() -> str:
    load_env()
    return (os.getenv(LOGAPI_URL_ENV) or DEFAULT_LOGAPI_URL).strip()


def save_token(token: str, logapi_url: str | None = None) -> Path:
    token = (token or "").strip()
    if not token:
        raise ValueError("Data-ai Token 不能为空")
    url = (logapi_url or DEFAULT_LOGAPI_URL).strip() or DEFAULT_LOGAPI_URL
    os.environ[MCP_TOKEN_ENV] = token
    os.environ[LOGAPI_TOKEN_ENV] = token
    os.environ[LOGAPI_URL_ENV] = url
    _upsert_env_file(
        AGENT_ENV_PATH,
        {
            MCP_TOKEN_ENV: token,
            LOGAPI_TOKEN_ENV: token,
            LOGAPI_URL_ENV: url,
        },
    )
    return AGENT_ENV_PATH


def try_reuse_da_profile() -> dict[str, str]:
    candidates = [
        Path.home() / ".da" / getpass.getuser() / "profile.yaml",
    ]
    for path in candidates:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if yaml is not None:
            data = yaml.safe_load(text) or {}
        else:
            data = _parse_simple_yaml(text)
        if not isinstance(data, dict):
            continue
        name = str(data.get("user_name") or "").strip()
        dept = str(data.get("department") or "").strip()
        if name and dept:
            return {"user_name": name, "department": dept, "source": str(path)}
    return {}


def setup_status() -> dict:
    profile = load_profile()
    reused = {}
    if not profile.get("user_name") or not profile.get("department"):
        reused = try_reuse_da_profile()
    token = get_token()
    user_name = profile.get("user_name") or reused.get("user_name") or ""
    department = profile.get("department") or reused.get("department") or ""
    return {
        "complete": bool(user_name and department and token),
        "user_name": user_name,
        "department": department,
        "client_tool": profile.get("client_tool") or "",
        "token_masked": mask_token(token),
        "has_token": bool(token),
        "profile_path": str(PROFILE_PATH),
        "agent_env_path": str(AGENT_ENV_PATH),
        "reused_da_profile": reused.get("source") or "",
        "missing": [
            name
            for name, ok in (
                ("姓名", bool(user_name)),
                ("部门", bool(department)),
                ("Data-ai Token", bool(token)),
            )
            if not ok
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="AB 实验助手本地初始化")
    parser.add_argument("--show", action="store_true", help="展示初始化状态（token 脱敏）")
    parser.add_argument(
        "--set-profile",
        nargs=2,
        metavar=("NAME", "DEPARTMENT"),
        help='写入姓名与部门，如 --set-profile "王璐 Kosmeo" "商业化运营部"',
    )
    parser.add_argument("--client-tool", choices=["cursor", "codex", "claude"], help="可选记录客户端")
    parser.add_argument("--set-token", metavar="TOKEN", help="写入 Data-ai Token（同时作为 LOGAPI_TOKEN）")
    parser.add_argument("--json", action="store_true", help="--show 时输出 JSON")
    args = parser.parse_args(argv)

    if args.set_profile:
        path = save_profile(args.set_profile[0], args.set_profile[1], args.client_tool)
        print(f"已写入 profile: {path}")
    if args.set_token is not None:
        path = save_token(args.set_token)
        print(f"已写入 token 到: {path}（值已脱敏，不在此回显）")
    if args.show or (not args.set_profile and args.set_token is None):
        status = setup_status()
        if args.json:
            import json

            print(json.dumps(status, ensure_ascii=False, indent=2))
        else:
            print("AB 实验助手初始化状态")
            print(f"  完整: {'是' if status['complete'] else '否'}")
            print(f"  姓名: {status['user_name'] or '(缺失)'}")
            print(f"  部门: {status['department'] or '(缺失)'}")
            print(f"  Token: {status['token_masked']}")
            if status["reused_da_profile"]:
                print(f"  复用 DA profile: {status['reused_da_profile']}")
            if status["missing"]:
                print(f"  待补齐: {', '.join(status['missing'])}")
            print(f"  profile: {status['profile_path']}")
            print(f"  agent.env: {status['agent_env_path']}")
        return 0 if status["complete"] else 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
