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
