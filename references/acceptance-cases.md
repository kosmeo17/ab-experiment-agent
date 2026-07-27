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
- If gray is 20% and the smallest experiment group is 30%, and WAU is not already deducted for gray/mutex, effective minimum group ratio is 6%.
- If WAU is already experiment-pool traffic after gray/mutex, do not multiply again.

Forbidden:

- Replace ARPU sample size with payment-conversion sample size.
- Treat `scripts/sample_size.py` output as formal company-calculator output.

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
