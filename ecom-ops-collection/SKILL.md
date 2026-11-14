---
name: ecom-ops-collection
description: "电商运营 Skill 合集入口：先建店铺档案，再根据用户说的需求路由到 9 个运营模块；不直接执行模块工作，也不替用户猜缺失资料。"
---

# 电商运营 Skill 合集

## 首次建档

1. 在用户的工作目录查找 `店铺资料/店铺档案.md`。
2. 没有档案时，按 `_shared/提问规范.md` 一次最多问 3 个问题，使用 `_shared/档案模板/店铺档案.md` 建档。
3. 有商品相关任务时，再查找对应的 `店铺资料/商品档案-<商品名>.md`，没有就先按商品模板补档。
4. 档案里的未知项保留为“暂无”或写入商品档案第 7 栏，不自行补数字和证据。

## 路由

| 用户会怎么说 | 使用分 skill |
|---|---|
| “这个商品卖给谁、怎么定位、上新前帮我分析” | `modules/01-marketing-product-analysis/` |
| “帮我定价、调价、算套餐和利润” | `modules/02-marketing-pricing/` |
| “抖店主图、SKU 图怎么做，规格怎么区分” | `modules/03-douyin-main-sku-image-composition/` |
| “宠物商品详情页怎么排，卖点和证据怎么放” | `modules/04-douyin-detail-page-structure/` |
| “帮我挑宠物商品图，判断保留还是重做” | `modules/05-pet-image-quality-review/` |
| “批量拆宠物商品套图，提炼可复用画面和提示词” | `modules/06-douyin-pet-image-distillation/` |
| “复盘发布、咨询、销售、成本数据，找下一步测试” | `modules/07-marketing-data-review/` |
| “设计商品列表、订单表格、投放计划这类业务界面” | `modules/08-business-ui/` |
| “设计 Windows 桌面运营软件的 UI、任务队列和数据边界” | `modules/09-desktop-operations-architecture/` |
| “我不知道该用哪个”或需求同时跨多个模块 | 先给 2～4 个候选，让用户选择 |

## 执行约定

先读 `_shared/底座规则.md`、`_shared/提问规范.md` 和 `_shared/输出规范.md`，再读选中的分 skill `SKILL.md`。多步、批量或需要动文件的任务先给计划，用户确认后再执行。完成时明确写出本次使用的分 skill 名称和自检结果。

入口只负责建档、路由和说明使用的模块，具体工作交给对应分 skill。
