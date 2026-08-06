# 使用日志与初始化

AB 实验助手使用日志写入 MySQL `da_agent_data.ab_experiment_agent_log`，经 logapi（与 da_agents_v2 相同的 Data-ai Token）。**只有这一张使用日志表。**

建表 DDL：`scripts/ddl/create_ab_experiment_agent_log.sql`（由数据部在 MySQL 执行）。

本地脚本：

| 脚本 | 用途 |
|------|------|
| `scripts/ab_setup.py` | 初始化：姓名、部门、Data-ai Token |
| `scripts/usage_logger.py` | 写入 setup / design_start / stage_pass / design_end |

## 初始化（只问 3 项）

进入设计主流程前，必须完成初始化。只收集：

| 项 | 用途 | 落盘（勿提交 Git） |
|----|------|-------------------|
| 姓名 | 写日志 `user_name`，格式 `中文名 英文名`，如 `王璐 Kosmeo` | `~/.ab-experiment-agent/profile.yaml` |
| 部门 | 写日志 `department`，如 `商业化运营部` | 同上 |
| Data-ai Token | logapi 写日志鉴权；同时写入 `DATA_AI_MCP_TOKEN` 与 `LOGAPI_TOKEN`（同值） | `~/.ab-experiment-agent/agent.env` |

规则：

- 缺任一则先完成初始化，再进入必要性等设计 Gate。
- Token 只粘贴到对话或经 `ab_setup.py --set-token` 写入本地 env；**不回显全文**，不入库、不进飞书、不进日志表、不进 commit。
- 若本机已有 DA Agents 的 `profile.yaml`（`user_name` / `department`）或 `DATA_AI_MCP_TOKEN` / `LOGAPI_TOKEN`，可复用；缺什么再问什么。
- 初始化成功后立刻写一条 `event_type=setup`。

检查命令：

```bash
python3 scripts/ab_setup.py --show
python3 scripts/ab_setup.py --set-profile "王璐 Kosmeo" "商业化运营部"
python3 scripts/ab_setup.py --set-token "<token>"
```

## 表字段

| 字段 | 必填 | 说明 |
|------|------|------|
| `log_id` | 是 | 本条日志 ID |
| `session_id` | 是 | 同一次设计会话；start / stage_pass / end 共用 |
| `user_name` | 是 | `中文名 英文名` |
| `department` | 是 | 部门 |
| `event_time` | 是 | 东八区时间 |
| `event_type` | 是 | `setup` / `design_start` / `stage_pass` / `design_end` |
| `stage_code` | 是 | 见下表；`design_end` 必须用 `session_complete` 或 `session_abort`，不得再用笼统的 `session` |
| `stage_name` | 是 | 阶段中文名 |
| `client_tool` | 否 | `cursor` / `codex` / `claude` |
| `user_query` | 条件必填 | **setup 可空**；`design_start` / `stage_pass` / `design_end` **必须**写触发该事件的 owner 原话或确认句 |
| `experiment_name` | 否 | 实验名；已知则写 |
| `result_summary` | 条件必填 | `stage_pass` / `design_end` **必须**写一句阶段结论；setup / design_start 建议写 |
| `extra_json` | 条件必填 | `stage_pass` **必须**写结构化确认点（见下）；其它事件建议写；**禁止 token / 密钥** |

### `extra_json` 建议结构（stage_pass）

```json
{
  "confirmed": {
    "goal": "...",
    "strategy": "...",
    "scene": "...",
    "core_metric": "..."
  },
  "pending": ["..."],
  "standard_mapping": {
    "scenario": "展示灵活促销banner",
    "scenario_gap": "信息流内部广告需新增标准场景"
  }
}
```

只放业务确认摘要，不放 token、完整对话、PII 以外的账号密钥。

## stage_code

| stage_code | stage_name | 对应 |
|------------|------------|------|
| `setup` | 初始化 | 仅 `event_type=setup` |
| `session` | 会话开始 | 仅 `event_type=design_start` |
| `session_complete` | 设计完整收口 | 仅 `event_type=design_end` 且完整完成 |
| `session_abort` | 设计中途结束 | 仅 `event_type=design_end` 且中途结束 |
| `g1_necessity` | 必要性 | Gate 1 |
| `g2_core_metric` | 核心指标 | Gate 2 |
| `g3_audience` | 实验对象 | Gate 3 |
| `g4_scene` | 实验场景 | Gate 4 |
| `g5_data_support` | 数据支持 | Gate 5 |
| `g6_grouping` | 分组 | Gate 6 |
| `g7_exclusion` | 互斥 | Gate 7 |
| `g8_caliber` | 数据口径 | Gate 8 |
| `g9_sample_gray` | 样本量/灰度 | Gate 9 |
| `g10_formal_doc` | 正式文档 | Gate 10 |

## 写入时机（硬规则）

| 时机 | event_type | stage_code |
|------|------------|------------|
| 初始化成功 | `setup` | `setup` |
| 开始进入设计（进入 Gate1） | `design_start` | `session` |
| 某个 Gate **刚确认通过** | `stage_pass` | `g1`…`g10` 对应码 |
| 设计完整收口 | `design_end` | `session_complete` |
| 设计中途结束 | `design_end` | `session_abort` |

### design_end 口径（固定，必须区分两种）

`event_type` 都是 `design_end`，用 `stage_code` + `extra_json.end_status` 区分：

| 类型 | stage_code | end_status | 何时写 |
|------|------------|------------|--------|
| **完整收口** | `session_complete` | `completed` | Gate10 已通过，且已完成「是否创建飞书文档？」询问收口（答「否」立即写；答「是」则在创建尝试结果回报后写） |
| **中途结束** | `session_abort` | `aborted` | 用户明确结束本轮（如「先到这里」「结束这个任务」），且尚未达到完整收口条件 |

`extra_json` 对 `design_end` **必填**，至少包含：

```json
{
  "end_status": "completed",
  "last_completed_gate": "g10_formal_doc",
  "feishu_doc": "created|skipped|n/a"
}
```

中途结束示例：

```json
{
  "end_status": "aborted",
  "last_completed_gate": "g7_caliber",
  "pending": ["样本量查数", "灰度", "正式文档"]
}
```

### 不写日志

- Gate 中间追问、澄清、grilling
- 点名查数、标签/指标只读发现
- 未真正开设计的入口面板浏览

### 返工

用户跳回并重做某 Gate 后再次通过：对该 Gate **再写一条** `stage_pass`（可观察返工）。

## 会话与脚本

- `setup` 可用独立 `session_id`。
- 同一设计会话的 `design_start`、各 `stage_pass`、`design_end` **必须同一 `session_id`**。
- Agent 写入优先调用：

```bash
python3 scripts/usage_logger.py --event setup --summary "初始化完成"
python3 scripts/usage_logger.py --event design_start --session-id S1 --user-query "帮我设计..." --summary "进入设计"
python3 scripts/usage_logger.py --event stage_pass --session-id S1 --stage g1_necessity \
  --user-query "主要是在信息流内部广告或灵活促销banner" \
  --summary "必要性通过：..." \
  --extra-json '{"confirmed":{"scene":"灵活促销banner/信息流内广"},"pending":["核心指标"]}'
python3 scripts/usage_logger.py --event design_end --session-id S1 \
  --end-status aborted --user-query "先到这里" --summary "用户中途结束" \
  --extra-json '{"end_status":"aborted","last_completed_gate":"g7_caliber"}'
python3 scripts/usage_logger.py --event design_end --session-id S1 \
  --end-status completed --user-query "不创建飞书文档" --summary "Gate全过；已跳过飞书文档" \
  --extra-json '{"end_status":"completed","last_completed_gate":"g10_formal_doc","feishu_doc":"skipped"}'
```

硬约束：写 `stage_pass` 时若缺少 `user_query` 或 `extra_json`，视为日志不合格，必须补写或更新该行后再继续。写 `design_end` 时必须带 `--end-status completed|aborted`，并写入对应 `stage_code`。

日志写入失败时：向 owner 说明失败原因（网络/鉴权/表未建），**不得阻断**已确认的设计推进；不得把 token 打进错误信息。

## 与 DA 的边界

- 复用同一 Data-ai / logapi Token 与身份信息时可复用，不强制用户重复配置。
- **不复用** `ab_review_query_log`（那是复盘查数日志）。
- 本表只服务 AB 实验助手使用漏斗，不写查数 SQL、不写反馈工单。
