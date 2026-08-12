# Acceptance Cases

Use these cases when forward-testing the skill. Each case validates conversation behavior and review judgment. Do not require DA/Doris/TA or other data-platform connections.

## Case 1: Short Summon

User:

```text
AB实验
```

Expected:

- Show compact ability panel.
- Offer review, idea coaching, sample/gray check, and Feishu document workflow.
- Do not ask for Doris, TA, DA, or data-platform setup.

Forbidden:

- Start a full review with no source material.
- Mention internal gate labels.

## Case 2: Early Idea With No Necessity

User:

```text
我想把访客页的按钮颜色换成红色，做个AB。
```

Expected:

- Ask one necessity question about the problem/business goal or why this strategy may help.
- Do not review grouping, sample size, or launch readiness.

Forbidden:

- Output `通过` or a full plan.
- Ask for service switch, dashboard, or gray percentage.

## Case 3: Necessity Established, Metrics Missing

User:

```text
现在访客页进入付费页的人很多但购买少，我们想改付费页权益说明，看看能不能提升收入。需要AB是因为不确定新说明会不会降低信任感。
```

Expected:

- Say the experiment can continue.
- Infer commercialization domain if not stated.
- Ask for or recommend the core judgment metric.

Forbidden:

- Jump to group ratio or implementation method.
- Ask for fixed 7-day or 14-day ARPU unless provided by user.

## Case 4: User Does Not Know Metrics

User:

```text
指标我不知道怎么写，你帮我想。
```

Expected:

- Provide one recommended core metric and two alternatives from the inferred business domain.
- State the main risk or assumption for each compactly.
- Ask the user to select or correct the core metric.

Forbidden:

- Ask the user to invent metrics from scratch.
- Mix core metric and observation metric selection in one confusing list.

## Case 5: Trigger Scene Missing

User:

```text
用户范围是非VIP用户，分两组，一组看原版，一组看新版。
```

Expected:

- Ask where/when the strategy actually triggers.
- Explain that trigger scene affects exposure, sample, and later review.

Forbidden:

- Approve grouping because user range and group descriptions exist.
- Ask sample-size details before trigger scene.

## Case 6: Sample Size Missing

User:

```text
核心指标是付费转化率，实验准备灰度10%，跑两周。
```

Expected:

- Ask for trigger-scene traffic first.
- Say gray ratio must be calculated from traffic and required sample.

Forbidden:

- Accept 10% as reasonable without traffic, baseline, and MDE.
- Tell the user to connect to a data platform.

## Case 7: Push-System Experiment

User:

```text
这是推送系统里的召回文案实验，不走ABtest后台。
```

Expected:

- Ask push-specific handoff fields only after user-facing plan is clear: split method, send rules, group content, frequency, delivery/click/conversion tracking.

Forbidden:

- Ask for ABtest service switch or switch values.

## Case 8: Formal Review With Missing Necessity

User:

```text
请review：实验名：新样式弹窗AB；目标：优化体验；对象：全量用户；分组：50/50；指标：点击率；灰度：20%。
```

Expected:

- Lead with `暂不建议进入实验设计/灰度配置`.
- Explain missing necessity in one sentence.
- Ask one highest-priority follow-up.

Forbidden:

- Spend most of the answer optimizing click metrics or gray release.

## Case 9: Feishu-Ready Draft With Gaps

User:

```text
帮我整理成飞书文档。
```

Expected:

- If hard-gate fields are missing, output a pending draft or ask the next blocking question.
- If the user only asks to organize content, prepare Feishu-ready text.
- If the user explicitly asks to create/update a Feishu document, use Feishu/Lark document tooling when available.
- Preserve `待补充` gaps instead of polishing them away.

Forbidden:

- Claim a Feishu document was created or updated before the tool action succeeds.
- Treat a Feishu document as proof that DA/Doris/TA data has been checked.

## Case 10: Mature Plan Review

User provides a mature plan with clear necessity, core metric, object, trigger scene, grouping, data support, sample-size evidence, monitoring, and rollback context.

Expected:

- Lead with `通过` or `可引导优化后调整`.
- Separate blockers from optimization suggestions.
- Offer a next-step menu such as prepare Feishu-ready content, check sample-size details, or polish wording.

Forbidden:

- Keep asking necessity questions already answered.
- Force external data verification.

## Case 11: Formal Draft Next Step Boundary

User asks the skill to generate or rewrite a formal AB plan draft after the necessary plan fields are present.

Expected:

- Output the draft in the standardized structure.
- End with draft confirmation: ask the owner to confirm goal, metrics, grouping, implementation method/service switch, and `待确认` markers.
- Keep monitoring and rollback as draft reminders unless launch readiness was requested.

Forbidden:

- Immediately ask for configuration owner/path, self-test population, launch owner, monitoring owner, or rollback owner.
- Treat the draft as configuration-ready only because it is readable.

## Case 12: Small Sample With Risk-Control Necessity

User says the target population is small, but AB is required because the strategy may hurt retention or user experience.

Expected:

- Continue the AB flow when necessity is valid.
- Mark sample size, expected lift/MDE, and conclusion reliability as `待确认` or underpowered risk.
- Explain that the experiment may support risk observation or require a longer period, but may not reliably prove a small core-metric lift.

Forbidden:

- Categorically reject AB only because traffic is small.
- Recommend a smaller traffic-pool safety validation only because the sample is already small.

## Case 13: Traffic Pool Ratio Versus Group Split Ratio

User says 100% of eligible users should enter the experiment traffic pool, then split 50/50 into control and treatment.

Expected:

- Accept this as a valid design when risk is manageable.
- Distinguish traffic-pool ratio from group split ratio.
- If sample is insufficient, recommend longer duration, broader object/scene, larger detectable-effect threshold, or limited interpretation.

Forbidden:

- Treat 100% eligible pool as the same thing as 100% treatment.
- Force a small gray/safety validation just because traffic is limited.

## Case 14: Feishu Document Title

User asks to create, update, rewrite, or prepare a Feishu/Lark AB experiment document.

Expected:

- Use or preserve the title format `AB实验 | xxxx`.
- Normalize a bare experiment title to `AB实验 | xxxx` unless the user explicitly asks for a different naming convention.

Forbidden:

- Change the document title to an alternate body-section style.
- Let example body structures override the title naming rule.

## Case 15: Strategy Package Comparison

User describes an experiment where the treatment differs from control as a package, such as Push timing + content + frequency guardrail.

Expected:

- Treat the package as the core comparison variable when the experiment is intended to test the package as a whole.
- State that attribution is package-level unless the owner needs component-level attribution.

Forbidden:

- Force the user to split every component into separate experiments by default.
- Claim the design is invalid only because more than one operational component changes inside the package.

## Case 16: PRD Implementation Scope Is Not User Scope

User provides a PRD for VIP Logo copy testing. The PRD says:

```text
情况1：展示每天价格，只做中英：中文“%@/天”；英文“%@/day”
情况2：展示每月价格，只做中英：中文“%@/月”；英文“%@/month”
```

Expected:

- Treat `只做中英` as copy/localization implementation scope, not experiment population scope.
- Do not limit experiment object to Chinese/English users unless the PRD or owner explicitly says so.
- Ask one clarification if user scope matters: `这里的只做中英是文案支持范围，还是实验只圈选中文/英文用户？`

Forbidden:

- Write `限定中文或英文语言用户` as the experiment object from this PRD alone.
- Use screenshot language or example copy as country/language eligibility.

## Case 17: Proxy Data Cannot Be Marked Fully Verified

The assistant found no formal Logo exposure event, then used `enterMyProfilePage` as a proxy for historical flow or baseline.

Expected:

- Keep status phrasing as `基于代理口径估算` or `待正式 Logo 展示事件复核`.
- In final plans and Feishu documents, clearly separate formal experiment exposure from historical proxy calculation.
- Avoid saying `历史基线、流量与样本量已经验证` unless formal numerator, denominator, events, and sample inputs were actually verified.

Forbidden:

- Put an over-strong callout at the top saying the plan is fully verified or ready for configuration when the key traffic event is still a proxy.
- Hide the proxy caveat only in a later footnote.

## Case 18: Formal Document Does Not Expose AI Internals

User asks to output a formal Feishu AB experiment document.

Expected:

- Use business-facing headings such as `业务判断与风险说明` or fold the content into `背景与必要性`.
- Mark uncertain inferred content as `待确认` when needed.

Forbidden:

- Use `业务域与 AI 推断` as a formal document section title.
- Make the document look like a raw model trace rather than an operator-facing plan.

## Case 19: Core Metric Confirmation Gate

User:

```text
你建议核心指标用 VIP ARPU，那就继续帮我算样本量。
```

Expected:

- If the user has explicitly accepted VIP ARPU, continue using it and state that the calculation is based on owner-confirmed VIP ARPU.
- If the assistant only recommended VIP ARPU but the user has not confirmed, ask the user to confirm or replace the core metric before calculating.
- Explain ARPU versus payment conversion rate when both are plausible.

Forbidden:

- Treat an AI recommendation as owner-confirmed.
- Calculate formal sample size from an unconfirmed core metric.

## Case 20: Observation Metric Duplicates Core Metric

User says the core metric is `VIP 付费转化率`, then asks for observation metrics.

Expected:

- Do not repeat `VIP 付费转化率` as an observation metric.
- Use related funnel or diagnostic metrics only if they add explanation, such as Paywall click rate, payment amount, ARPPU, or refund guardrail.
- Mark split metrics as process diagnostics, not alternate success criteria.

Forbidden:

- Put the same payment conversion rate under both core and observation metrics.

## Case 21: Group Design Stranger Self-Check

User provides a VIP price-display experiment where the PRD says the change applies only to the default product, but the default product may be annual and may have no discount outside promotions.

Expected:

- Flag the group design as P0 incomplete if monthly price source, calculation formula, SKU source, promotion state, currency/rounding, and A/B equivalence risk are unclear.
- Ask for the most blocking detail, or list the exact design holes in review mode.
- Do not proceed to sample size, gray, or formal Feishu document until the group design passes the self-check.

Forbidden:

- Only restate A/B/C/D variants without diagnosing that some variants may be identical or unconfigurable.

## Case 22: Concrete Mutual Exclusion Question

User asks whether the experiment needs mutual exclusion.

Expected:

- Ask whether there are running experiments, activities, or strategies affecting the same users, entrance, price/SKU, discount, copy, or core metric.
- Say if none exist, current design does not need mutex, but launch should include one final sweep.

Forbidden:

- Ask only `是否需要互斥吗？`

## Case 23: DA Query Pre-Confirmation

User asks the skill to check baseline or traffic for sample size.

Expected:

- First show intended events/fields, filters, numerator, denominator, unit, and time window.
- Tell the user to verify uncertain fields in the tracking-management system or with the data BP.
- Only after confirmation should the assistant route to `$da-agents`.

Forbidden:

- Directly run DA without exposing the planned caliber.
- Dump SQL, CSV paths, local paths, or log IDs by default.

## Case 24: Notebook Sample Size Inputs

User has a mature plan and asks for sample size for an ARPU core metric.

Expected:

- Use notebook-style inputs: first-week WAU, new-WAU week-2 attenuation, 14-day core metric baseline, MDE type/value, metric type, effective minimum treatment-group ratio, and ARPU/mean conversion inputs.
- Before calculating, state the sample-size source. If a company notebook / calculator / provided file is accessible, read or run it before any local formula. Known local company notebook candidates include `/Users/sequioa/Downloads/计算实验的预估样本量.ipynb`.
- If gray is 20% and the smallest experiment group is 30%, and WAU is not already deducted for gray/mutex, effective minimum group ratio is 6%.
- If WAU is already experiment-pool traffic after gray/mutex, do not multiply again.

Forbidden:

- Replace ARPU sample size with payment-conversion sample size.
- Treat `scripts/sample_size.py` output as formal company-calculator output.
- Use a local mean-difference formula, standard deviation formula, historical approximation, or AI estimate as the formal sample-size result when a company notebook / calculator / provided file is accessible.

## Case 25: Post-Document Capability Reminder

User asks the skill to finish a Feishu-ready AB plan.

Expected:

- After the document content is complete, remind that the assistant can help organize an experiment configuration launch checklist if the plan is confirmed.
- Remind that before configuration, the owner should confirm whether dual-end testing has passed.
- Remind that after the experiment ends, `$da-agents` can help with readout/retrospective.

Forbidden:

- Ask for experiment ID while the user is still writing the plan.
- Claim the assistant can continuously monitor the experiment unless such automation is explicitly available.

## Case 26: Query Workflow Is Agent-Led, Not User-Led

User:

```text
可以，火速整理。
```

Context: the prior turn said sample size or baseline needs real data.

Expected:

- Confirm the known experiment information first.
- State what the assistant / agent will check next.
- Before querying, list events or fields, filters, numerator, denominator, unit, window, and mutual-exclusion handling.
- Ask the owner to confirm the query caliber before routing to `$da-agents`.

Forbidden:

- Say `拿这份给数据/DA 查`.
- Make the user think they must query the data themselves.
- Skip the query-caliber confirmation step.

## Case 27: MDE Is Explained With Recommended Percent Options

User:

```text
MDE 按照 ARPU +5% 算行。
```

Expected:

- Treat this as owner selecting ARPU relative lift +5%.
- If explaining MDE, say it means the smallest lift the experiment should be able to detect.
- Use percent options: 5% is more sensitive but needs more sample; 10% is the general recommendation; 15% / 20% are for larger expected effect or lower flow.
- Do not ask the user to provide a decimal.

Forbidden:

- Ask `MDE 用多少`.
- Say only `至少要接受涨多少`.
- Ask the user to fill `0.1` or leave them to convert decimals.

## Case 28: ARPU Uses The Same Experiment-Scene Cohort

User questions the formula:

```text
实验场景 ARPU = 实验期间 VIP 新购收入 / 进入蓝色特权页或会员套餐页的去重实验用户数
```

Expected:

- Flag that the numerator must be revenue from the same users who entered the experiment scene and met experiment conditions.
- Correct formula: experiment-scene ARPU = target revenue from experiment-scene users during observation window / dedup experiment-scene users.
- If only all-site VIP revenue is available, mark it as proxy and not formal.

Forbidden:

- Use all-site VIP new-purchase revenue as numerator while denominator is experiment-scene users.
- Present a proxy revenue caliber as formal sample-size input.

## Case 29: Sample Size Source Must Be Declared

User asks:

```text
这里的数据是你编造的，还是参考我给的样本量计算的网址的底层逻辑来算的？
```

Expected:

- Answer directly whether the calculation used the company calculator / provided file / local rough script.
- If the calculator or file was not actually read, say it was not used.
- Explain that formal ARPU / mean sample-size needs company notebook / calculator inputs or data BP result.
- If a company calculator or notebook is accessible, do not continue defending the rough formula; rerun or restate the result using the company source.

Forbidden:

- Defend a formula without source.
- Claim the company calculator was used if it was not actually accessed.
- Hide that `scripts/sample_size.py` is only a rough initial estimate.

## Case 30: Gray Ratio Uses Planned Duration And Mutual Exclusion

User provides:

```text
每组所需样本量 96,887，近 7 天符合条件去重用户约 203,251。我们一般至少跑 14 天；预计 14 天约 300,000 人。A/B 50/50，互斥后可用比例 80%。
```

Expected:

- Use planned duration, not the shortest time to fill sample.
- Compute formal gray ratio as `96,887 / (300,000 × 80% × 50%) ≈ 81%`.
- Recommend formal gray around 80%-85% if risk permits, plus optional 10%-20% short risk-observation gray before formal start.
- Mark final gray as dependent on mutual-exclusion usable ratio.

Forbidden:

- Recommend 100% simply because 7-day flow is near the total required sample.
- Treat 1-2 day risk observation as the formal experiment period.
- Ignore mutual-exclusion loss.

## Case 31: One Question Only Under Pressure

User is being asked for missing sample-size inputs.

Expected:

- Ask only the single highest-priority confirmation, or present known inputs / planned query caliber and ask for one confirmation.
- If multiple values are needed, state that the assistant will check them after the user confirms the query caliber.

Forbidden:

- Ask for core metric, 7-day flow, 14-day baseline, MDE, and mutual exclusion all in one turn.
- Make a long checklist feel like homework for the owner.

## Case 32: Mutual Exclusion Ratio Is Not Required Before Sample Calculation

User provides:

```text
核心指标是实验期 VIP ARPU，对象和场景都清楚，A/B/C/D 四组均分。线上有一个同入口 Paywall 价格实验需要互斥，但我还没决定这个实验要占多少互斥池。你先算两周需要多少灰度。
```

Expected:

- Confirm that the mutual-exclusion relationship is known and must be respected.
- Do not ask the owner to provide the mutual-exclusion usable ratio before sample-size calculation.
- Calculate or explain that the first output should be `required effective traffic = gray ratio × mutual-exclusion usable ratio`.
- Provide combination guidance after the required effective traffic is known, such as 20% effective traffic can be achieved by `20% mutex usable × 100% gray`, `40% mutex usable × 50% gray`, or `80% mutex usable × 25% gray`.
- State that final configuration, final gray, final duration feasibility, and formal Feishu document still require the owner to choose the final gray and mutual-exclusion combination.

Forbidden:

- Block sample-size calculation only because the mutual-exclusion ratio is missing.
- Default mutual-exclusion usable ratio to 100% and output a final gray.
- Output final duration feasibility before the final combination is chosen.

## Case 33: Narrow Data Lookup Does Not Drift

User:

```text
用这个 table 查一下最近进入 Profile / Metab 的非 VIP 用户量。
```

or:

```text
唯一没定的是进入 Metab 的英文事件名和字段。你继续查，只查事件定义。
```

Expected:

- Treat the request as a narrow data lookup, not a full AB-flow continuation.
- First answer only the named table, event, field, or single metric.
- Return `查到什么`、`口径/限制`、`对当前判断的影响`、`建议下一步`.
- The business interpretation may say whether the result is enough to support the current data Gate, sample-size input, trigger-scene denominator, or field confirmation.
- Stop after the result and wait for the user to explicitly continue.

Forbidden:

- Calculate sample size, gray ratio, period feasibility, or formal document status before returning the named lookup.
- Inspect unrelated AB rules, CMS configuration, Feishu documents, or skill files.
- Expand to other tables, extra metrics, baselines, historical fluctuation, segmentation, or attribution unless the user asks to continue.
- Return only raw event names, fields, SQL, CSV paths, or logs without business meaning.

## Case 34: Korea Super Exposure Price Plan Uses Standard Fields

User:

```text
韩国 VIP 且历史购买过超级曝光的用户做价格实验。核心指标用语伴曝光产品 付费金币消耗 ARPU，key 是 partner_exp_purchase_arpu；场景是进入超级曝光；护栏看留存率。请继续。
```

Expected:

- Preserve the confirmed experiment object exactly as eligibility: `韩国 VIP 且历史购买过超级曝光的用户`.
- Preserve the scene exactly as `进入超级曝光`; do not repeat Korea, VIP, or history-purchase conditions there.
- Internally retain the confirmed AB standard-library mapping: `语伴曝光产品 付费金币消耗 ARPU` / `partner_exp_purchase_arpu`; in owner-facing or Feishu business output, display only the Chinese metric name and business-readable definition.
- Keep only one guardrail: the standard retention-rate metric. Refunds, complaints, and negative feedback are risk monitoring, not experiment metrics.
- State confirmed items, current stage, and one next action. Continue from the earliest unfinished main-flow step.

Forbidden:

- Invent a metric such as `韩国 VIP 超级曝光实验用户人均 HT 金币消耗`.
- Invent a purchase page, popup, `Click Coins`, or any other entrance/event not confirmed by the owner.
- Add multiple guardrails or put user complaints in the metric list.
- Jump to configuration, sample size, or Feishu creation merely because this local clarification is complete.

## Case 35: Feishu Creation Requires Explicit Confirmation And Permission Handling

User:

```text
方案所有 Gate 都通过了。
```

Expected:

- Ask exactly whether to create a Feishu document before creating, updating, or exporting a formal document.
- If the user agrees but the target space lacks write permission, request the minimum necessary write permission for that target space.
- After successful creation or update, read back the title and body before reporting the document link.

Forbidden:

- Automatically generate a local Markdown or XML document when Feishu write permission is missing.
- Claim that a document was created without a successful write and read-back verification.

## Case 36: Chinese Metric Names Are Primary

User:

```text
窗口付费率先不要，只看人数/金额/ARPU。过程指标看 dau_7d_lifetime_cnt、avg_user_app_active_duration_min_au，以及 D1/D3/D7 的新购人数、金额、ARPU。
```

Expected:

- Translate or map every metric to a Chinese business name before presenting it to the owner.
- Keep English keys only in internal system fields; do not display them to the owner or in Feishu business output.
- If no Chinese standard name is known, write `中文名称待确认` or `需新增标准指标`; do not expose the key in the business document.
- Do not make the English key visible in owner-facing bullets, tables, or Feishu drafts.

Forbidden:

- Output `dau_7d_lifetime_cnt` or `avg_user_app_active_duration_min_au` as the metric name.
- Treat `VIP ARPU (vip_arpu)` as unacceptable in a business document when the Chinese standard name is known; display `VIP ARPU` / `VIP 人均收入` according to the standard-library Chinese name.
- Put English keys into formal metric names, titles, tables, or Feishu business documents.

## Case 37: User Labels Come From CMS-CLI

User:

```text
不要走 MCP 探查，你查一下项目里是否有带用户标签相关材料。这个实验对象想圈长期活跃但不付费用户。
```

Expected:

- Explain that local project documents can be checked for context, but user labels should be discovered through CMS-CLI / `$cms` read-only in 推送系统-用户标签管理 or 标签管理.
- Use or propose CMS-CLI schema discovery such as `cms-cli schema search 用户标签` / `cms-cli schema search 标签管理`.
- Focus on 标签名称、备注、状态、层级，and generally prefer 三级标签.
- If CMS access or schema discovery is unavailable, stop at `标签来源待确认`; do not conclude the label library does not exist.
- State that tag existence only supports audience feasibility; traffic, baseline, and sample size still require DA validation when they matter.

Forbidden:

- Only search the local repo / Feishu index and conclude there is no user-label library.
- Use a label whose status is stopped, deleted, abnormal, or unknown as a confirmed target audience.
- Output only `label_id` / id without Chinese label name, note, status, and level.
- Treat label discovery as verified target-user scale or metric baseline.

## Case 38: External Dependency Version Reminder

User:

```text
这个实验要用 CMS 里最新的用户标签和推送配置，再用 DA agent 查样本量输入。
```

Expected:

- Remind the owner that `$cms` / CMS-CLI and `$da-agents` may update independently from `ab-experiment-agent`.
- Ask whether to check dependency update status before the latest CMS / DA read, or state clearly if continuing with the current local version.
- Do not block low-risk idea discussion, but do remind before real reads that affect formal conclusions, configuration, labels, metrics, sample size, gray release, or Feishu formal docs.
- Preserve the execution boundary in results, such as `按当前本地版本只读查询` when update status was not checked.

Forbidden:

- Silently update CMS, DA, Feishu CLI, UI/PRD agent, or any external dependency.
- Say the external capability is latest merely because it is installed.
- Treat version freshness as business verification; still read CMS / DA sources before confirming labels, metrics, traffic, baseline, or sample size.

## Case 39: Feedback Table And Private GitLab Update Boundaries

User:

```text
数据同事后面会继续给 AB agent 反馈。你把反馈放到飞书多维表格当数据库，有新增记录时机器人通知你；更新放在 GitLab 上，用临时 token 一键安装更新。
```

Expected:

- Explain that feedback table records are maintenance records, not AB experiment data sources.
- If a feedback table already exists and authorization is available, read records to understand duplicate issues, status, owner, fix version, and verification cases.
- Before creating a Feishu base, adding a bot, writing a record, changing fields, or sending a notification, ask for explicit authorization and state the target table / bot / write scope.
- Use `references/feedback-maintenance.md` to recommend fields such as feedback text, category, severity, status, owner, target version, fix commit, verification case, and release status.
- Support private GitLab update through `AB_EXPERIMENT_AGENT_REPO_URL` plus local git credentials or temporary `AB_EXPERIMENT_AGENT_GIT_TOKEN`.
- Keep token handling ephemeral: token must come from environment variables or local credential helpers and must not be printed, committed, written to feedback records, or saved in git remote URL.

Forbidden:

- Create or update a Feishu base, add a bot, send notifications, or write records without explicit owner authorization.
- Treat feedback records as verified CMS labels, metrics, traffic, sample size, experiment results, or production configuration.
- Put temporary token into README examples as a literal value, git remote URL, logs, commit message, table record, or assistant output.
- Claim one-click update is safe for outsiders if the repository is public and installable without authentication; instead explain the access boundary and recommend private repo or token-gated distribution if needed.

## Case 40: Cursor And Claude Code Compatibility

User:

```text
你这个完全是给 Codex 用的，得让它兼容 Cursor 和 Claude Code。
```

Expected:

- Add or maintain lightweight entry files for non-Codex agents, such as `AGENTS.md`, `CLAUDE.md`, and `.cursor/rules/ab-experiment-agent.mdc`.
- Keep `SKILL.md` as the canonical behavior spec instead of copying the whole skill into each tool-specific file.
- Tool-specific files should route agents to the required references for feedback maintenance, dependency version checks, user labels, and verification.
- Preserve the same safety boundaries across tools: no unauthorized external writes, no token persistence, Chinese metric names for owner-facing output, CMS-CLI for real user-label discovery.
- Update README maintenance notes so users know which files support Codex, Cursor, and Claude Code.

Forbidden:

- Maintain three divergent full rule copies for Codex, Cursor, and Claude Code.
- Put secrets, tokens, private URLs with credentials, or external system write instructions into tool-specific entry files.
- Treat Cursor / Claude compatibility as proof that external CMS / DA / Feishu abilities are available; those still depend on the user's local tools and authentication.

## Case 41: Usage Logging Init And Gate Funnels

User:

```text
帮我设计一个 Paywall 文案 AB 实验。我还没配过这个助手。
```

Expected:

- Before entering design Gates, ask only for name (`中文名 英文名`), department, and Data-ai Token when missing; reuse DA profile/token when already present.
- Persist identity and token via `scripts/ab_setup.py` into `~/.ab-experiment-agent/` only; never echo the full token.
- After init succeeds, write `event_type=setup` to `ab_experiment_agent_log`.
- When design starts, write `design_start`; on each Gate pass write `stage_pass` with the matching `stage_code` (`g1_necessity` … `g9_formal_doc`).
- Write `design_end` with `--end-status completed` / `stage_code=session_complete` after Gate9 passes and the「是否创建飞书文档？」ask is closed (yes → after create attempt result; no → immediately).
- Write `design_end` with `--end-status aborted` / `stage_code=session_abort` when the user explicitly ends mid-flow.
- Follow `references/usage-logging.md`; log write failure must be reported without blocking confirmed design progress.

Forbidden:

- Enter necessity / metric design without completed init when name, department, or Data-ai Token is missing.
- Write token into log rows, Feishu docs, git files, or assistant replies.
- Skip `design_end` after Feishu-doc ask wrap-up or explicit user end.
- Write a bare `design_end` without distinguishing `session_complete` vs `session_abort`.
- Log every intermediate clarification or named lookup as a stage event.
