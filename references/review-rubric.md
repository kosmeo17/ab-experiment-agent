# AB Experiment Agent Review Rubric

Use this rubric in the same order as the source SOP. Do not jump to metrics, dashboards, gray release, or launch checks before experiment necessity is established.

This rubric checks plan quality and the evidence the user provides. It does not authorize connecting to dashboards, TA, Doris, DA, or other data platforms. Feishu/Lark document tools may be used to read or write plan/source documents when requested, but they do not verify actual metric, event, dashboard, or data-system support. If actual system support is unknown, mark it as `待确认` or `需要新增数据需求`.

## Outcomes

- `暂不建议进入实验设计/灰度配置`: necessity is not established. Stop before grouping, metrics, gray release, configuration, or launch checks.
- `不通过，必须先补齐`: necessity is established, but a core design or readiness gate fails.
- `可引导优化后调整`: core logic is valid, but the plan needs clearer writing, structure, or collaboration detail.
- `通过`: the plan explains why the experiment should exist and gives an executable design, data path, and enough monitoring/safety context for the requested stage.

## Gate 1: Experiment Necessity

Judge necessity before all other details.

The plan must answer the SOP's necessity questions in concrete terms:

- What does the owner want to do?
- Which business goal or core metric does this experiment serve?
- What problem, opportunity, data, historical result, or observed phenomenon triggered this experiment?
- What is uncertain about the strategy, and why is it not a deterministic fix, already-validated logic, no-risk positive change, or reusable historical conclusion?
- Which business core metric can this strategy directly improve?
- Is the expected impact worth the product, operation, data, and coordination cost?
- Is the scene sample likely enough to support a meaningful conclusion?
- Why may this strategy solve the current problem?
- Why is AB better than direct launch, direct repair, or doing nothing?
Strong signals from source cases:

- Background includes current data or a concrete phenomenon, such as penetration, ARPU, conversion, paid-source contribution, historical experiment result, funnel behavior, or user distribution.
- The strategy has a visible causal chain, for example `visitor count exposed -> social proof/curiosity increases -> visitor paywall entry or purchase improves`.
- The plan explains why the current solution is insufficient and why the new strategy might change behavior.

Fail signals:

- The plan starts from a solution but cannot say what business goal or core metric it is trying to move.
- Only says "optimize", "try", "support a feature", "test a style", or starts from a solution with no problem.
- Uses a generic statement that the metric is important, but does not prove the strategy can influence it.
- No data, historical experiment, product logic, user behavior, or clear opportunity.
- The change is a deterministic bug fix or low-risk obvious improvement that should not need AB.
- Expected benefit is too small for the required cost.
- WAU/sample is likely insufficient, but the plan still expects a reliable conclusion.

Default action when this gate fails: say `暂不建议进入实验设计/灰度配置`, explain the missing evidence in one sentence, then ask exactly 1 highest-priority follow-up question.

In coaching conversations, trace necessity in this order: what the owner wants to do, what problem it is meant to solve, what business goal it serves, and why the owner believes the strategy can solve the problem. This mirrors how operators usually describe ideas and avoids forcing abstract goal wording too early.

Do not loop inside necessity after the AB rationale has been answered. Once the owner has covered action, problem, goal, causal basis, and why AB is needed, necessity is sufficient for the skill's default path. Move to evaluation metrics before experiment object, trigger scene, and grouping design.

If there is no data but the owner can describe a concrete phenomenon, ask about that phenomenon. If there is neither data nor a describable phenomenon, pause the AB path and ask for the affected scene and behavior before recommending exactly 1 low-cost evidence action.

If evidence shows the problem exists but AB is not suitable, say so directly and recommend exactly 1 better validation path with the reason. After that path is completed, first judge whether a direct launch, direct fix, or abandonment decision can already be made. Return to AB only when a real problem remains and the team still needs to compare strategy effects.

## Gate 2: Business Priority Self-Check

After necessity is established, business priority can be noted, but it is not a default blocking gate for this skill. Different business lines own their own priority rules. Only review priority when the user explicitly asks whether this experiment should be prioritized now.

Required:

- Expected impact or benefit range.
- Confidence or evidence strength.
- Product, operation, data, and coordination cost.
- Relative priority compared with other candidate experiments.

Fail signals:

- The experiment is technically possible but expected benefit is tiny.
- Cost or coordination burden is high and no matching impact is shown.
- The plan asks to proceed only because "we can try it".

Default path after necessity is established: confirm evaluation metrics, then move to experiment object, trigger scene, and grouping design.

## Gate 3: Evaluation Metrics

Before grouping design, the plan must define evaluation metrics: core metric and must-watch/observation metrics.

This is different from the business goal in necessity. The goal explains why the experiment matters; evaluation metrics explain how the experiment result will be judged and interpreted.

Identify the business domain before proposing or judging metric types. Read `business-domains.md` when metric type, guardrail risk, strategy validity, business risk, or cross-business side effects are involved. `business-domains.md` is not the standard metric library; standard experiment metric, scene, and result-dimension names/keys must come from `$cms` / CMS-CLI read-only discovery. Use the primary domain for the core metric type. Affected secondary domains go into risk notes or launch monitoring, not additional guardrail entries. If the domain is inferred rather than provided, mark it as `AI 推断` and state what assumption needs confirmation.

In coaching conversations, infer candidate metrics from the necessity context and give options. Options 1-3 should be concrete metric candidates; option 4 should let the owner provide a different metric. Keep core metric options and observation metric options separate, and state the recommended option with the reason.

When the owner does not know how to write metrics, do not only ask them to choose from a blank list. Recommend 1 core metric and 2 alternatives from the business domain. For each option, state why it fits, when it is suitable, what risk it may hide, and which assumption needs confirmation.

Core metric is single-select. Must-watch/observation metrics are multi-select. The core metric is the experiment's main judgment standard; observation metrics can include multiple funnel, module, or business-line diagnostics. Guardrail is a separate single metric, not part of the observation list.

Ask metric choices in two turns by default: core metric first, then must-watch/observation metrics. Do not mix the single-select and multi-select questions in one turn unless the user explicitly wants a compact/full review.

Required:

- One core metric that decides whether the experiment succeeds.
- The core metric directly affects the business goal, can be observed within the experiment cycle, and can be directly influenced by the strategy.
- Must-watch/observation metrics that cover business-line performance and directly affected module performance.
- One business-domain guardrail metric for the most important likely side effect. Retention or revenue ARPU can be recommended as the single guardrail by core metric type; refund, complaint, payment failure, harassment, false positive/误伤, teacher supply, or push opt-out belong in risk notes or launch monitoring unless the owner explicitly selects one as the unique guardrail.
- Each proposed metric is tied to the business goal and experiment strategy.
- Each proposed metric can plausibly be influenced by the experiment strategy.
- Each proposed metric can be observed within the experiment cycle.

Fail signals:

- The plan has a goal but no measurable core metric.
- The plan lists many metrics without saying which one decides success and which ones are must-watch/observation metrics.
- The selected core metric is too far from the strategy to reflect the experiment effect.
- The plan uses a positive domain metric but omits the domain's obvious guardrails, such as revenue without refunds/retention, risk interception without 误伤, push click without unsubscribe/uninstall, or social sends without replies/reports.

## Gate 4: Experiment Object, Trigger Scene, And Grouping Design

The plan must define who enters the experiment, when the strategy affects them, and how groups differ.

In coaching conversations, ask object and trigger scene separately. Confirm the experiment object first, then the trigger scene. Both must be clear before reviewing control/experiment group differences.

Internally, object and trigger scene are configuration prerequisites. Operator-facing wording should say they affect experiment configuration, stable grouping, exposure definition, and later data review. Do not mention unfinished automation tools such as `cml-cli`.

Trigger scene is a hard gate. If the plan cannot state the condition under which users truly see or are affected by the strategy, stop before grouping configuration because exposure definition, WAU/sample estimation, and gray calculation will be unreliable.

Required:

- Experiment object: country, version, VIP status, registration age, behavior, label, or other user range.
- Experiment scene: the exact condition where users truly receive the strategy impact, such as entering a page, seeing a banner, triggering a payment sheet, first profile visit, or push exposure.
- Number of experiment groups and the ratio mapped to each group.
- User-facing experience mapped to each group, so the operating-side plan makes the comparison clear.
- Control group current experience, written as actual user/system behavior rather than only "no adjustment".
- Experiment group descriptions that are deterministic, process-like, and parallel with the control group.
- Group ratio.
- Clear variable difference between groups; if multiple variables change, explain the comparison logic.
- Recommended configuration handoff fields when known: implementation method, configuration path, and configuration owner. For ABtest-system experiments only, also collect service switch and switch value for each group. For push-system experiments, collect push split method, send rules, group content, frequency cap, and delivery/click tracking instead.

Strong signals from source cases:

- The gender-tab case explicitly separates UI, sorting, and nickname mosaic comparisons.
- The Stripe case defines the object, payment scene, Stripe default behavior, fallback behavior, and known URL risk.
- The visitor-banner case separates new users and old users because their trigger logic and thresholds differ.

Fail signals:

- Only gives a broad object like "non-VIP users" without the exposure scene.
- Scenario and strategy impact point do not match.
- The plan describes group copywriting but does not say what users in each group actually see or experience.
- The plan gives ABtest switch values but does not explain the user-facing experience mapped to those values.
- Control group is "none" or "no adjustment" with no current-state explanation.
- Multiple variables are mixed so attribution is impossible.
- Screenshots or videos are missing for complex UI/process changes.

## Gate 5: New Data Requirements

Judge whether new data requirements are needed after grouping is clear.

The business goal should already be confirmed in necessity, and evaluation metrics should already be confirmed before grouping. This gate checks whether the experiment needs additional data work: category-level support for the experiment scene, experiment population, core metric, observation metrics, the single guardrail metric, and only then detailed event/label/dimension/dashboard support when needed.

This gate is a system-support gap check, not a place to redesign goals, metrics, or groups. In operator-facing coaching, ask whether the confirmed categories are already supported by the current system, dashboard, or push system. Do not default to a field-level checklist of group assignment, trigger events, delivery, clicks, or jump-target tracking; use those only for implementation handoff detail or launch-readiness checks. If all required support is confirmed by the user or source material, operator-facing output may say `新增数据需求：无`. If unsupported or unknown, identify the missing category and whether a new data requirement must be raised.

Required:

- Experiment scene and experiment population can be configured or have a documented substitute.
- Core metric is tied directly to the experiment goal.
- Must-watch/observation metrics and the single guardrail metric cover directly affected modules, revenue, retention, payment, push, experience, and other business lines as needed.
- The confirmed business domain's required category-level support is checked, or the missing support is raised as a new data requirement.
- Metric definitions, data source, split dimensions, and success standard are clear.
- Existing system, push system, dashboards, labels/events/dimensions where relevant, or documented substitutes are confirmed by the user, pasted material, or a data/config owner; missing categories are raised early as new data requirements.

Important placement rule:

- "核心指标是否已在看板中" is a new-data-requirement or launch-readiness check. Do not ask it as an early necessity or priority question.

Fail signals:

- Lists many metrics but no core metric.
- Core metric cannot be directly influenced by the strategy or cannot be observed within the experiment cycle.
- No guardrail for a change that may affect retention, revenue, payment, interruption, push, or other entrances.
- Missing data support for a business-domain guardrail that could reverse the launch decision.
- Needed event, scene, label, metric, dashboard, or dimension is missing and no new data requirement is raised.

## Gate 6: Sample Size And Gray Release

Estimate sample size and decide whether gray release is needed after grouping and new data requirements are clear.

Treat gray release as a calculation result, not as a percentage the owner can choose by intuition. In coaching conversations, ask for trigger-scene traffic first: WAU, daily exposure, or daily triggered users. Only after traffic is known should the reviewer classify the core metric type and ask for the corresponding sample-size inputs.

If trigger-scene traffic is clearly insufficient, do not pretend a gray percentage can fix inadequate sample volume. Separate experiment necessity from result detectability. If the owner has a valid risk-control reason, such as concern that a Push strategy may hurt retention or user experience, the AB can continue while the plan states that sample-size inputs, expected lift/MDE, and conclusion reliability are `待确认`; the result may be useful for risk observation but underpowered for proving core-metric lift. If necessity is weak or the strategy risk is low, stop before gray-release planning and give exactly one next action: enlarge the experiment object or trigger scene, extend duration, adjust the detectable-effect expectation, or use a lower-cost validation path.

Read `sample-size-gray.md` when judging this gate. Support more than conversion-rate metrics because the skill may generate an AB experiment plan and later feed a Feishu configuration document. For conversion-rate metrics, a standard two-proportion calculation is acceptable. For mean, ARPU, count, and ratio metrics, require historical variance/standard deviation, user-level aggregation logic, or a company calculator/data-owner result before approving sample sufficiency.

Required:

- Estimated scene WAU or daily sample.
- Core metric type.
- Experiment duration, usually with at least a 2-week view unless context justifies otherwise.
- Baseline value and expected lift for the primary metric.
- Historical variance/standard deviation, calculator output, or documented data-owner judgment for non-conversion-rate metrics.
- Group ratio and group count.
- Gray release or mutual-exclusion ratio, or a reason gray release is unnecessary.

Fail signals:

- Gray percentage is unrelated to available WAU or required sample.
- The plan uses a non-conversion-rate metric but has no variance, calculator output, or data-owner judgment.
- The plan treats a ratio metric as a simple conversion rate without explaining numerator, denominator, and user-level aggregation.
- Mutual exclusion or scheduling conflict is likely but not addressed.
- Sample is too small but the plan still expects a reliable conclusion without marking detectability risk.
- Group ratio changes during the experiment without a justified plan.

## Gate 7: Configuration And Launch Readiness

Check launch readiness only after the previous design gates are established.

This gate answers whether the experiment can be safely configured and launched as designed. It is separate from monitoring and retrospective. Missing launch details should block launch, but should not reopen necessity or grouping unless the missing item exposes an earlier design gap.

Distinguish plan maturity, `ready_to_config`, and `ready_to_launch`:

- An operating-side plan can be mature enough to draft when user range, trigger scene, group count, group ratio, user experience by group, and gray/mutex ratio are explicit. Implementation method, method-specific configuration fields, monitoring owner, and rollback action are recommended for later readiness checks but should not block the formal plan draft.
- `ready_to_config` means the plan can be stably handed to configuration/engineering: the mature plan fields are present, implementation method is known, and the configuration path/owner plus method-specific configuration detail are known enough to configure safely. For ABtest-system experiments this includes service switch and group values when the ABtest system needs them. For push-system experiments this includes push split method, send rules, group content, frequency cap, and delivery/click tracking.
- `ready_to_launch` means configuration readiness plus pre-launch checks are complete: dashboard/tracking, self-test population, cross-end behavior, stakeholder notification when needed, and safety monitoring/rollback preparation when relevant.
- Do not mark a plan `ready_to_config` just because it is readable or has passed necessity/metrics review. If method-specific configuration values are missing, say the plan can still be drafted but is not fully configuration-ready.
- These labels are internal. In operator-facing output, say whether the plan can continue to configuration or launch, and name the one missing next step. Avoid exposing `ready_to_config` or `ready_to_launch` unless the user explicitly asks for structured status.

Required:

- Experiment configuration is created or ready to create from the plan.
- ABtest service switch and values match the grouping design when using ABtest and already provided.
- Push split method, send rules, group content, frequency cap, and tracking match the grouping design when using push-system experiments.
- Group ratio is correct and stable.
- Gray release and mutual exclusion are configured as planned.
- Core metric dashboard, tracking, or query path is ready before launch.
- Client behavior is consistent on both ends and matches the plan.
- Test population is restricted for self-check when needed.
- Affected business stakeholders are notified when needed.
- Key tracking for core metrics is validated before launch when possible.

Fail signals:

- The plan is mature, but no one can map it into experiment configuration.
- Switch values, group ratio, or gray/mutual-exclusion settings do not match the plan.
- The experiment is ready to launch but the core metric has no dashboard, tracking, query path, or owner.
- No self-test path for a complex UI, payment, push, or cross-end change.

## Gate 8: Monitoring, Risk, And Rollback

For explicit launch-readiness checks, the plan should explain how the team will notice bad outcomes and what it will do.

This is a pre-launch boundary-setting gate, not an unlimited post-experiment diagnosis workflow. Require enough information to monitor risk and make a safety stop decision. Do not keep asking diagnostic questions after the plan has named the anomaly signals, guardrails, owner, and rollback action.

Required:

- First monitoring after 1-2 days: split, exposure, sample anomaly, SRM, and obvious negative movement.
- Ongoing monitoring during the experiment: sample, SRM, primary metric, and guardrail movement.
- Domain-specific guardrails are monitored before launch, especially when the strategy may affect revenue, retention, payment, push, social safety, risk误伤, teacher supply, or live room ecology.
- Negative risk, rollback condition, and rollback action.
- Owner for pause, gray reduction, or rollback.

Fail signals:

- Possible impact on retention, revenue, traffic entrance, payment, push, or experience but no guardrail.
- The primary metric can improve while an obvious domain guardrail can degrade, but no one has named the stop condition.
- No monitoring timing or owner.
- No rollback condition for high-risk UI, interruption, price perception, payment, or push changes.

## Gate 9: Retrospective Reminder

Retrospective and post-result actions are not default coaching questions.

For ordinary plan generation, add a reminder that final continue/stop/extend/expand decisions should be made during retrospective based on actual core metric movement, the single guardrail metric, accumulated sample size, and business context. Do not ask what the team will do under positive, negative, or flat results as a required question.

For explicit retrospective templates:

- The retrospective should compare core metric, observation metrics, guardrails, and accumulated sample size.
- Guardrails can override a positive primary metric.

Fail signals:

- A significant result is treated as automatically good without considering business cost, guardrails, or gray-release context.

## Clarity And Collaboration

Expression problems are optimization issues unless they prevent judging a core gate.

Optimization signals:

- Sections are complete but order is confusing.
- Group descriptions are not parallel.
- Screenshots and text are not clearly mapped.
- Next action, owner, or configuration path is missing.

Escalate to `不通过，必须先补齐` if unclear writing makes it impossible to identify target users, scenario, groups, metrics, data needs, or risks.
