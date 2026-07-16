---
name: cms
description: "Use when the user types /CMS, /cms, asks to use CMS-CLI, or wants to query, inspect, compare, draft, or safely operate HelloTalk internal CMS configurations, schemas, APIs, service switches, popups, splash screens, paywall/VIP commercial configuration, blue privilege pages, or CMS backend data. Always default to read-only analysis and require explicit confirmation before any CMS write, publish, enable, disable, delete, rollback, cache refresh, or production-impacting operation."
---

# CMS CLI

## Overview

Use this skill for HelloTalk internal CMS work through `cms-cli`. Treat `/CMS` as an explicit request to use this workflow.

This is not the Vercel headless CMS skill. It is for the local HelloTalk `cms-cli` tool in the CMS backend workspace.

## Safety Rules

- Default to read-only queries, analysis, comparison, drafts, and risk notes.
- Do not call write APIs unless the user explicitly confirms the exact operation.
- For production writes, require a separate confirmation after explaining environment, target config, before/after values, impact scope, effective mechanism, risks, and rollback.
- Treat VIP, paywall, pricing, promotion, paid benefits, ads, growth campaigns, popups, splash screens, and service switches as high-risk configuration.
- Use `--dry-run` for any operation that may write before asking for confirmation.
- If login is expired, say so and ask the user to run or approve `cms-cli auth login` before continuing.

## Common Commands

Check login:

```bash
cms-cli auth status
cms-cli auth whoami
```

Discover API/schema:

```bash
cms-cli schema search <keyword>
cms-cli schema get <api-or-schema-id>
```

Read CMS API data:

```bash
cms-cli api GET <path> --env test --format json
cms-cli api GET <path> --env prod --format json
```

Use `--jq` for compact projections when useful. Use `--debug` only when troubleshooting.

## Workflow

1. Read project instructions first, especially `AGENTS.md` and any relevant `docs/scenarios/` files in the current CMS workspace.
2. Confirm the target environment from the user request or query context. If unclear, do not assume production.
3. Check `cms-cli auth status` if an API call is needed.
4. Use `schema search` and `schema get` to identify the correct interface before calling APIs.
5. Prefer test environment for exploration unless the user explicitly asks for production read-only checks.
6. Present results as confirmed facts vs. inference when the distinction affects a decision.
7. For requested changes, draft the exact plan and wait for explicit confirmation before any write.

## Output Pattern

For read-only checks:

- State environment, data source, and query time.
- Summarize the key result first.
- Show IDs, names, status, date windows, regions, versions, priority, audience, and risk-relevant fields.
- Note gaps or ambiguous fields instead of guessing.

For change plans:

- Separate read-only verification from write steps.
- Include before value, after value, impact scope, effective mechanism, risk, and rollback.
- Ask for explicit confirmation only after the plan is concrete.
