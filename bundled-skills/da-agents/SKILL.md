---
name: da-agents
description: "Use when the user types /da_agents, /da-agents, mentions da_agents, da_agents_v2, DA Agent v2, or wants to route HelloTalk data work through the local DA Agents v2 project, including data queries, TA/Doris metric lookup, AB experiment review, business analysis, DA setup/profile work, feedback submission, or report/share-summary generation."
---

# da_agents

## Overview

Use this skill as the Codex trigger entry for the local DA Agents v2 project:

Use the DA Agents v2 project at `${DA_AGENTS_HOME}` when set, otherwise `~/Projects/da_agents_v2`.

The skill should not duplicate DA Agents v2 rules. It should route the task into that project and read the project-maintained source of truth before acting.

## Trigger Inputs

- `/da_agents`
- `/da-agents`
- `da_agents`
- `da_agents_v2`
- DA Agent v2
- Requests for HelloTalk 查数、AB 实验复盘、专项分析、TA SQL 查询、Doris 指标库、业务指标库、DA setup/profile、反馈登记、下钻思路分享稿

## Required First Reads

Before doing task work, read:

1. `${DA_AGENTS_HOME:-~/Projects/da_agents_v2}/AGENTS.md`
2. Any `.cursor/rules/*.mdc` file selected by `AGENTS.md` for the detected mode
3. Relevant operator docs only when the user asks about setup, usage, rollout, feedback, or troubleshooting

Key docs:

- `${DA_AGENTS_HOME:-~/Projects/da_agents_v2}/docs/getting_started_for_operators.md`
- `${DA_AGENTS_HOME:-~/Projects/da_agents_v2}/docs/user_guide.md`
- `${DA_AGENTS_HOME:-~/Projects/da_agents_v2}/config/codex/README.md`

## Routing

Use `AGENTS.md` as the router:

- AB review: read `.cursor/rules/agent-ab-review.mdc` and related AB rules.
- Quick data query: read `.cursor/rules/agent-router.mdc`, then Doris/TA/query-task rules as directed.
- Deep analysis: read `.cursor/rules/agent-controller.mdc` and analysis-chain rules as directed.
- Setup/profile: read setup/profile rules and docs.
- Feedback: read `.cursor/rules/agent-feedback.mdc`.
- Share summary: read `.cursor/rules/agent-task-share-summary.mdc`.

## Operating Rules

- Prefer running from `${DA_AGENTS_HOME:-~/Projects/da_agents_v2}` when executing DA scripts or reading task outputs.
- Check `.da/{system-user}/profile.yaml` before data requests, as required by the project rules.
- Do not invent data, event definitions, metric definitions, SQL results, or Feishu content.
- If data-ai MCP, Lark MCP, TA API, or logapi is unavailable, follow the setup/troubleshooting rule and pause if configuration cannot be completed.
- For AB reviews, require confirmation of experiment scheme, scenario, and metric list before calculation.
- Communicate in Chinese unless the user asks otherwise.
- Keep outputs decision-oriented: conclusion first, then口径、时间范围、分子/分母、基准组/对照组、绝对变化和相对变化.

## Useful Commands

Show setup status:

```bash
cd "${DA_AGENTS_HOME:-$HOME/Projects/da_agents_v2}"
python3 .cursor/skills/data-query-analyzer/scripts/da_setup.py --show
```

Detect AB intent:

```bash
cd "${DA_AGENTS_HOME:-$HOME/Projects/da_agents_v2}"
python3 .cursor/skills/data-query-analyzer/scripts/ab_experiment_lib.py detect-intent "用户原文"
```

Check TA API configuration:

```bash
cd "${DA_AGENTS_HOME:-$HOME/Projects/da_agents_v2}"
python3 .cursor/skills/data-query-analyzer/scripts/ta_api_env.py --show
```
