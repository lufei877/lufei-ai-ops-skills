---
name: marketing-product-analysis
description: Analyze a product before marketing or sales by identifying its sales stage, narrowest credible buyer, triggering problem, value evidence, offer readiness, and material evidence gaps. Use when a product needs positioning, channel selection, a demo, listing, launch, or a new sales iteration. 产品营销前分析目标客户、销售阶段、价值证据与成交准备度。排除产品列表代码修复和已批准文案的单纯改写。
---

# Product Marketing Analysis

Establish the evidence-backed marketing baseline before choosing a channel or writing final assets.

## Inputs

- Stable `productId` and product brief with source references.
- Verified capabilities, deliverables, sales stage, service boundary, refund/support boundary, and prohibited claims.
- Current pricing record location; pricing may be pending.
- Optional customer evidence, competitor evidence, prior campaign data, and product-set relationships.

If product identity or source material is missing, return `input_gaps` and stop. Do not fill gaps from another product.

## Method

1. Classify the stage as `unsold`, `launch-ready`, `selling`, or `reactivation`.
2. Identify the narrowest credible buyer, trigger, current workaround, purchase friction, and desired progress.
3. Map verified capabilities to customer value. Label facts, source claims, inferences, and unknowns separately.
4. Check deliverable, proof, fulfillment, support, refund, conversion path, and offer readiness.
5. Propose an entry offer, core offer, bundle, upgrade, or cross-sell only when supported by the product set.
6. Produce candidate angles without selecting or publishing a channel.
7. Request competitor evidence only when it can change positioning, pricing, claims, offer composition, or channel choice.

## Pricing Handoff

Record pricing gaps, rights, duration, cost, service, and refund questions for `$marketing-pricing`. Do not calculate, approve, or rewrite a price here.

## Output Contract

Return a versioned `marketing_analysis` object containing `contractVersion`, `productId`, `sources`, `salesStage`, `targetBuyer`, `triggerProblem`, `valueEvidence`, `readiness`, `candidateAngles`, `offerLadder`, `competitorGaps`, `inputGaps`, `unknowns`, and `nextDecision`. Every claim must reference a source or be labeled as an inference or unknown.

## Exclude

Do not publish, message buyers, approve prices, create final channel assets, or present planned/unverified functionality as available.
