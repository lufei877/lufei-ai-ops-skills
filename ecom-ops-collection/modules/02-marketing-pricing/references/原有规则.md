---
name: marketing-pricing
description: Design, approve, record, and synchronize evidence-backed product pricing with plan rights, duration, market references, cost constraints, supplier margin, exceptions, and versioned source updates. Use for trial, monthly, quarterly, annual, batch, supplier, or post-approval pricing work. 制定或调整产品定价、套餐权益、成本和利润约束。排除只介绍现有价格与未授权修改支付系统。
---

# Marketing Pricing

Keep one approved product-price record as the source for demos, listings, final assets, reviews, and workbench views.

## Inputs

- Stable `productId`, confirmed product brief, current price source, and writeback path.
- Plan rights, duration, device/account limits, fulfillment, support, refund boundary, and eligibility.
- Cost or supplier price when applicable, margin constraints, and immutable price conditions.
- Comparable-market references with plan, duration, rights, source, and observation date.

Without explicit approval evidence, stay in candidate mode and do not modify a customer-facing price source.

## Candidate Design

1. Separate facts, formulas, assumptions, candidates, approved values, exceptions, and unknowns.
2. Reject comparisons whose rights or duration are materially different.
3. Define trial eligibility, duration, rights, exclusions, success action, repeat limit, and expiry per product.
4. Add monthly, quarterly, and annual plans only when applicable. Compute `daily_rate = plan_price / duration_days`.
5. Require `daily_rate.monthly > daily_rate.quarterly > daily_rate.annual` when all three exist. Do not apply this ordering to total plan prices.
6. When the approved strategy calls for market positioning, price slightly below a comparable reference only after the reference and discount approach are approved. Consider value, cost-to-serve, acquisition cost, and segment constraints before recommending.
7. Compute `supplier_margin = (customer_quote - supplier_price) / customer_quote` and check the approved 30%-50% range when supplier pricing applies. Treat fees, refunds, taxes, and fulfillment costs as separate constraints when known.

## Approval And Sync

Competitor prices are evidence, not automatic recommendations. Approval requires rights, duration, limits, service/refund boundary, comparable evidence, and supplier cost when applicable. Never silently overwrite an approved price or resolve an exception.

After approval, write a versioned `approved_pricing_record` to the declared canonical source, verify product isolation, daily-rate order, margin bounds, customer/supplier separation, references, and syntax, then emit a `workbench_sync_receipt`.

## Output Contract

Candidate mode returns `pricing_architecture` and `pricing_exceptions`, each with `contractVersion`, `productId`, `pricingVersion`, sources, plan rights, durations, prices, daily rates, formulas, assumptions, unknowns, and approval status. Post-approval mode additionally returns `approved_pricing_record`, `pricing_learning_feedback`, and `workbench_sync_receipt`.

## Exclude

Do not publish, message customers, expose supplier prices, change a live platform price, or infer missing quarterly, annual, supplier, or refund terms.
