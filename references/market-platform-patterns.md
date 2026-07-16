# Market Platform Patterns

Use this reference to calibrate AB experiment review against mature experimentation platforms. Do not turn it into an operator checklist. The purpose is to improve judgment about whether a plan is scientifically valid, operationally safe, and ready for later configuration.

Sources checked on 2026-07-06:

- GrowthBook: https://www.growthbook.io/products/experimentation
- Statsig: https://www.statsig.com/experimentation
- LaunchDarkly: https://launchdarkly.com/docs/home/experimentation
- Optimizely Feature Management: https://www.optimizely.com/products/feature-management
- VWO Testing: https://vwo.com/testing/

## Common Chain

Mature platforms generally shape experimentation as:

`idea -> hypothesis -> feature flag/config carrier -> target population and randomization unit -> split/mutex/gray rollout -> metric system -> sample size and duration -> health checks -> statistical analysis -> ship/rollback/continue -> retrospective`

For this skill, the durable lesson is:

- Market platforms solve how to run experiments scientifically and safely.
- This skill should first solve whether the proposed experiment deserves to be run.

## Platform Takeaways

### GrowthBook

Observed pattern:

- Connects experimentation with feature flags, warehouse-native analysis, SQL-defined metrics, shared metric libraries, approval flows, checklists, guardrails, SRM detection, CUPED, sequential tests, Bayesian/frequentist engines, and decision frameworks.

Review implication:

- Ask for metric definition and guardrails before launch details. Treat result-success rules and post-result actions as retrospective reminders, not default operator questions.
- Treat SRM, guardrail alerts, and metric ownership as launch-readiness checks, not as early necessity blockers.
- Preserve a retrospective reminder that later continue, stop, expand, or gather-more-evidence decisions depend on actual results and guardrails.

### Statsig

Observed pattern:

- Combines assignment, analysis, insights, advanced experiment types, variance reduction, sequential methods, switchback/bandit-style experimentation, meta analysis, and team learning.

Review implication:

- Ask what unit is randomized and what behavior is triggered. Do not ask the owner to predefine positive/negative/flat post-result actions in ordinary plan generation.
- If the strategy affects marketplaces, cyclic traffic, or supply/demand balance, standard user-level AB may be insufficient; suggest switchback or lower-cost validation when appropriate.
- Retrospective learning matters: result interpretation should feed the next experiment, not just decide pass/fail.

### LaunchDarkly

Observed pattern:

- Places experimentation close to feature flags, targeting, randomization units, metric events, experiment health, guarded/progressive rollout, and shipping winning variations.

Review implication:

- Separate plan maturity from configuration readiness.
- Do not require switch names in the operating-side plan, but recommend collecting them for later configuration reuse.
- Guarded rollout and rollback owner/action belong to pre-launch safety.

### Optimizely

Observed pattern:

- Emphasizes feature management, targeted delivery, progressive rollout, permissions/approvals, kill switch, dynamic configuration, flag governance, and experimentation governance.

Review implication:

- Ask whether risky changes have an owner, rollback condition, and rollback action before launch.
- Treat permissions, approvals, and kill switch as operational safety boundaries.
- If a plan changes pricing, payment, safety, or user trust, require stronger guardrails.

### VWO

Observed pattern:

- Strong in CRO/web conversion optimization. Its chain is close to target, track, decide, with behavior analytics, heatmaps, session recordings, funnels, Bayesian decisioning, and calculators.

Review implication:

- When background evidence is weak, do not simply reject; propose one low-cost evidence action such as funnel check, click analysis, qualitative sample review, or small observation.
- Evidence gathering supports the necessity gate. It does not automatically approve AB design.

## Reusable Review Rules

- Necessity first: do not optimize split ratio, dashboard, copy, or switch values before the business problem, causal hypothesis, and AB uncertainty are clear.
- Metrics before launch: require one core metric, relevant observation metrics, and guardrails for likely side effects.
- Randomization and exposure: distinguish user range from trigger scene. The trigger scene is where users truly receive the strategy impact.
- Configuration is a later layer: implementation method, config path, and method-specific fields are recommended for handoff but should not block the operating-side plan from maturing. Service switch and group values apply only to ABtest-system experiments; push-system experiments need push split, send-rule, content, frequency, and tracking fields instead.
- Safety boundary: launch-readiness checks can include monitoring owner, day 1-2 anomaly checks, and rollback condition/action when relevant. Positive/negative/flat post-result actions remain retrospective context, not default questions.
- Alternative path: if AB is not the right method, provide exactly one better validation path and explain why it is cheaper or more valid.
