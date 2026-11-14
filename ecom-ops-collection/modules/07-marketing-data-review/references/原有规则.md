---
name: marketing-data-review
description: Review time-based publication, inquiry, sales, cost, retention, and average-order-value evidence; locate the active funnel constraint; and define the next focused test. Use after real campaign or sales data returns from approved public, community, owned, or marketplace channels. 根据实际营销数据复盘漏斗约束、转化、成本与下一版实验。排除无数据的效果断言及代码性能分析。
---

# Marketing Data Review

Use publication evidence, the approved measurement plan, and immutable metric snapshots. A missing publication record or incomparable data is a gap, not a result.

## Inputs

- Stable `productId`, objective, publication evidence, asset and price versions, and measurement plan.
- Raw snapshots with platform/channel, item ID, collection time, window, metric definition, denominator, source, and identity/deduplication rules.
- Reach, meaningful engagement or inquiry, conversion, revenue, and cost data where available; mark unavailable fields.

## Review

1. Verify each snapshot's ID, time window, source, definition, and comparability.
2. Compare with the objective and baseline; do not infer causality from one weak signal.
3. Locate the active constraint: reach, attention, intent, handoff, conversion, offer, fulfillment, retention, or upsell.
4. Separate facts, hypotheses, unknowns, and external factors.
5. Choose the smallest useful next change. Preserve retained elements and change one primary variable unless the campaign is invalid or unsafe.

Use thresholds and minimum sample rules from the measurement plan. If they are absent, return `review_gaps` and avoid a confident winner declaration.

## Output Contract

Return `review_report` and `next_iteration_brief` with `contractVersion`, `productId`, evidence references, channel observations, funnel diagnosis, confidence rationale, revenue/AOV/cost/retention impact where available, review gaps, primary variable, retained elements, new version, success measure, schedule, and stop condition. Never overwrite raw snapshots.

## Exclude

Do not invent attribution, merge incomparable windows, call intent a conversion, edit/delete published items, or declare campaign completion without publication and comparable data evidence.
