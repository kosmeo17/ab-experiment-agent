# AB Experiment Agent Instructions

This repository packages the AB Experiment Agent rules. When an agent works in this repo or uses it as project context, treat `SKILL.md` as the primary instruction source.

## Required Reading

- Read `SKILL.md` before changing rules, assets, scripts, tests, or examples.
- Read only the directly relevant files under `references/` for the current task.
- For feedback about this agent, read `references/feedback-maintenance.md`.
- For external CMS / DA / Feishu / UI / PRD capability freshness, read `references/dependency-version-checks.md`.
- For user labels, read `references/user-labels.md` and use CMS / CMS-CLI read-only discovery when real label knowledge is needed.

## Operating Boundaries

- Do not create, update, publish, send, or modify external Feishu / CMS / GitLab resources without explicit user authorization.
- Do not store tokens, cookies, webhooks, session values, or credentials in files, logs, tables, git remotes, commit messages, or replies.
- Do not treat local documentation as proof that CMS labels, metrics, events, traffic, baselines, or production configs exist. Use the appropriate read-only source.
- Keep metric names in Chinese for owner-facing output. English keys may appear only as system keys, event names, field names, or explanation.
- Keep changes scoped. When rule behavior changes, update the matching acceptance case and regression checklist.

## Verification

After editing this repo, run:

```bash
bash -n install.sh
git diff --check
```

If the change affects installed Codex usage, sync the source repo to the local skill installation and compare both directories:

```bash
rsync -a --exclude .git /Users/sequioa/Documents/AB实验/ab-experiment-agent/ /Users/sequioa/.codex/skills/ab-experiment-agent/
diff -qr -x .git /Users/sequioa/Documents/AB实验/ab-experiment-agent /Users/sequioa/.codex/skills/ab-experiment-agent
```
