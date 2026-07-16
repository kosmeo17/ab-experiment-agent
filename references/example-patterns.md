# AB Experiment Example Patterns

Use these patterns to calibrate review judgment. Do not quote or dump full source examples into review output unless the user asks.

## Good Case Patterns

### Stripe Native Payment

Good signals:

- Background names a real business cost: App Store fee is high, third-party payment fee is lower.
- Uses prior H5 experiment evidence, including both the disappointing overall result and the signal from users who clicked the operation entry.
- Core metric is revenue-aligned: VIP ARPU net revenue.
- Experiment object and scene are precise: non-VIP, US App Store country, version threshold, entering the payment-method page.
- Data need is stated: new experiment scene.
- Group design describes exact payment flow, default selection, fallback path, and known URL risk.

Review heuristic:

- Reward plans that explain "why now" and "why this strategy may still work despite prior mixed evidence".
- Ask for risk/guardrail when price perception, payment flow, or platform switching may affect conversion.

### Gender Tab Sorting And Clear Avatar

Good signals:

- Explains the prerequisite: sorting only matters if users can perceive clear avatars.
- Identifies two switches and separates comparisons across groups.
- Defines why VIP does not need a separate experiment and can reuse non-VIP results for consistency.
- Group descriptions make attribution possible: old UI vs new UI, old sorting vs new sorting, no nickname mosaic vs mosaic.

Review heuristic:

- Reward plans that isolate variables instead of merging every idea into one experiment group.
- If multiple variables change, ask what each group comparison is meant to prove.

### Hamburger Popup SKU And New UI

Good signals:

- Background starts from observed purchase behavior: users tend to buy the SKU they originally triggered.
- Explains why the old popup may no longer fit the new UI and current purchase intent.
- Group descriptions are process-like by trigger source, SKU shown, image, copy, and group ratio.

Review heuristic:

- A UI or copy change can be valid when tied to a behavior observation and purchase intent, not merely because the new style looks better.

### Nearby Say-Hi Opportunity

Good signals:

- Builds on prior experiment learning: sorting stimulated paywall exposure but paid conversion was weaker than expected.
- States the strategic uncertainty: whether a small free experience can improve the "experience before payment" conversion path.
- The experiment scene and group differences are explicit: one free say-hi, button copy visible or hidden, and what happens after the chance is used.

Review heuristic:

- Reward plans that use previous experiment conclusions to motivate the next strategy.
- Ask for guardrails when a free benefit may cannibalize paid conversion.

### Visitor Banner

Good signals:

- Background includes penetration, paid-source contribution, visitor distribution, and existing strategy context.
- Causal chain is explicit: externalize visitor information -> increase social achievement/curiosity -> improve visitor paywall entry and VIP payment.
- Separates new users and old users because trigger timing, thresholds, and sample behavior differ.
- Mentions negative interaction: visitor banner may cover streak check-in, so click and retention should be watched.

Review heuristic:

- Reward threshold or trigger choices that are justified by user distribution, not arbitrary numbers.
- Ask for separate designs when different user cohorts have different behavior or risk.

## Problem Case Pattern

### Flexible Promotion Banner Style

Risk signals:

- Background only says the version supports carousel style; it does not show a current problem or opportunity.
- Experiment purpose says it will improve payment and retention, but the strategy is only banner background style.
- No evidence explains why style difference should affect ARPU or retention.
- Data need says a new experiment scene is needed, but necessity is not established.
- Group design changes image style only, while the value of testing the style itself is not defended.

Review heuristic:

- Do not start by optimizing group ratio, data needs, or dashboard readiness.
- First stop at necessity: ask what current behavior or data suggests banner style is limiting click, payment, or retention.
- If the owner can only say "new style might look better", recommend a low-cost evidence action before AB design.

## Cross-Case Review Rules

- A strong background contains at least one of: current data, user behavior observation, historical experiment result, product logic, competitor/localization reasoning, or a concrete operational opportunity.
- A strong experiment scene is where users truly receive the strategy impact, not just the broad user group.
- A strong group design makes the tested difference obvious and keeps descriptions parallel.
- A strong metric design has one success-deciding primary metric plus must-watch guardrails tied to the affected module and possible negative side effects.
- A weak plan often looks complete in template sections but still fails because the first question, "why should this experiment exist?", is unanswered.
