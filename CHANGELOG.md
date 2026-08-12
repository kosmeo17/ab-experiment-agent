# Changelog

本文件记录 AB 实验助手对用户 / 维护者可感知的变更。格式参考 [Keep a Changelog](https://keepachangelog.com/)。

## [Unreleased]

## [2026-08-12] - 使用日志

本次在分支 `ivan` 完成：**新建 ivan Branch；新增日志写入和初始化配置功能。**

### Added

- **使用日志**：新增单表 `da_agent_data.ab_experiment_agent_log`（DDL：`scripts/ddl/create_ab_experiment_agent_log.sql`），经 logapi / Data-ai Token 写入，对齐 da_agents_v2 的公共库写入方式。
- **初始化配置**：进入设计主流程前只需提供姓名（`中文名 英文名`）、部门、Data-ai Token；落盘至 `~/.ab-experiment-agent/`（`profile.yaml` + `agent.env`），不回显完整 Token。
- **本地脚本**：
  - `scripts/ab_setup.py`：写入 / 查看初始化状态；优先读取本机 AB 配置，可回退复用 DA Token。
  - `scripts/usage_logger.py`：写入 `setup` / `design_start` / `stage_pass` / `design_end`。
- **规则与文档**：`references/usage-logging.md`；并在 `SKILL.md`、`AGENTS.md`、`.cursor/rules`、`README.md`、`references/feishu-export.md` 接线初始化闸门与写日志时机。
- **验收与回归**：Acceptance Case 41；回归清单第 59 条。

### Changed

- **按强制 Gate 打点**：除初始化与会话起止外，每个 Gate 通过写一条 `stage_pass`（`g1_necessity` … `g9_formal_doc`），用于设计漏斗分析。
- **日志字段约束收紧**：
  - `design_start` / `stage_pass` / `design_end` 必须带 `user_query`。
  - `stage_pass` / `design_end` 必须带非空 `extra_json`（确认点摘要；禁止 token）。
  - `stage_pass` 必须带 `result_summary`。
- **`design_end` 区分完整收口与中途结束**（`event_type` 仍为 `design_end`）：
  - 完整收口：`stage_code=session_complete`，`extra_json.end_status=completed`（Gate9 通过并完成「是否创建飞书文档？」询问收口）。
  - 中途结束：`stage_code=session_abort`，`extra_json.end_status=aborted`（用户明确结束本轮）；CLI 必填 `--end-status completed|aborted`。
- **Token 加载优先级**：`~/.ab-experiment-agent/agent.env` 优先于进程环境变量与 DA 全局 env，避免旧 Token 覆盖本次配置。

### Notes

- 建表需数据部在 MySQL 执行 DDL；Agent 侧只通过 logapi 写入。
- 日志写入失败须告知原因，但不得阻断已确认的设计推进；错误信息不得包含 Token。
- `.gitignore` 增加 `.ab-experiment-agent/` 与本地 `tmp-*` 临时文件忽略规则。

## [Previous]

此前版本未维护本 Changelog；历史变更见 git history 与 README「本次更新」。
