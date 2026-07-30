# Business Domain Radar

Use this reference when an AB experiment plan involves metric choice, guardrail choice, business risk, strategy validity, or a cross-business side effect.

This file is not a business encyclopedia. Use it to route the experiment into the right business lens, suggest plausible metrics, and avoid confident conclusions when the needed business context is missing.

## Default Rules

- Identify the primary business domain after experiment necessity is sufficient and before proposing evaluation metrics.
- If the domain is unclear, infer it from the strategy's affected user behavior, target metric, trigger scene, and risk surface. Mark the domain as `AI 推断`.
- Do not pause only to ask for the domain unless different domain choices would lead to opposite core metrics or launch decisions.
- When one experiment affects multiple domains, use the primary domain for the core metric. The experiment metric list still has only one guardrail: revenue-related core metrics use retention rate; retention-related core metrics use revenue ARPU. Other cross-domain risks belong in risk notes or launch monitoring.
- For internal review reports or formal drafts, separate:
  - `已知事实`: facts from the user, document, data, or source material.
  - `AI 判断`: recommendations from AB methodology and this domain radar.
  - `待确认假设`: assumptions that need the owner or business side to confirm.
- In step-by-step coaching, do not print these labels. Ask the next question or give one concise recommendation instead.
- When the owner does not know how to write the metric plan, recommend 1 core metric and 2 alternatives. For each, state the reason, suitable premise, risk, and assumptions to confirm.
- Do not approve launch only because the core metric is positive. Check the single standard guardrail and the relevant risk monitoring first.

## Domain Overview

| 业务域 | 核心目标 | 常见核心指标 | 必看/观察指标 | 风险说明与上线监控 |
| --- | --- | --- | --- | --- |
| 商业化 | 提升收入、付费效率、订阅价值 | 收入、ARPU、ARPPU、付费率、订阅转化率、复购率 | 曝光、点击、下单、支付成功、SKU 分布、优惠使用 | 留存下降、退款上升、投诉、支付失败、价格感知受损、短期提收长期伤害 |
| 留存/活跃 | 提升用户持续使用和关键行为沉淀 | D1/D7/D30 留存、活跃率、回访率 | 首日关键行为、会话数、好友/关注/消息、任务完成、push 到达/点击 | 打扰上升、卸载、投诉、虚假活跃、短期激励透支长期留存 |
| 直播语聊 | 提升房间供需、互动和消费生态 | 进房率、房间停留、上麦率、互动率、送礼收入 | 开播数、主播在线时长、房间曝光、观众转主播、礼物转化 | 房间氛围变差、主播流失、低质房间增多、付费用户体验下降 |
| 风控/安全 | 降低风险损失，同时控制误伤 | 拦截率、违规率、风险损失、审核命中率 | 申诉率、解封率、审核耗时、风险用户复犯、正常用户通过率 | 误伤正常用户、转化下降、留存下降、客服压力、地区/人群偏差 |
| 课程/学习 | 提升试听、报名、完课和复购 | 试听转化、报名率、完课率、续费率、课程收入 | 老师响应、排课成功、学习时长、课后评价、学习路径完成 | 老师供给不足、低质转化、退款、完课下降、学习体验受损 |
| 社交/匹配/关系 | 提升有效连接和关系沉淀 | 打招呼率、回复率、会话建立率、关系沉淀率 | 曝光、点击、资料页访问、消息发送、好友添加、匹配成功 | 骚扰、低质消息、女性/新用户体验下降、举报拉黑上升 |
| Push/召回 | 提升触达后的回访和关键行为 | push 点击率、召回率、回访率、目标行为转化 | 到达率、展示、点击后路径、频控命中、分人群效果 | 打扰、退订、关闭通知、卸载、短期点击但长期留存下降 |

## 商业化

### 识别关键词

会员、VIP、SVIP、订阅、金币、付费、支付、价格、折扣、SKU、弹窗、收银台、订单、退款、ARPU、ARPPU、收入、复购。

### 核心目标

提升收入、付费效率、订阅价值或支付链路成功率。

### 可选核心指标

- 净收入、收入、VIP/SVIP 收入、金币收入。
- ARPU、ARPPU、付费率、订阅转化率、首购率、复购率。
- 支付成功率或关键 SKU 转化率，当实验只影响支付链路或单个 SKU。
- When an experiment may create a new paid SKU while affecting existing VIP/SVIP demand, prefer experiment-period ARPU / net revenue per experiment user as the primary judgment standard. Treat the new SKU purchase rate as demand evidence or an observation metric, not the final launch criterion.
- Do not default to a fixed `7 日` or `14 日` ARPU window. If the experiment period is unknown, write `实验周期内 ARPU/人均净收入` and ask for the planned period later.

### 观察指标

曝光、点击、下单、支付成功、支付失败、SKU 分布、优惠使用、订单金额、付费路径分布、退款原因。

### 唯一护栏与风险说明

收入类核心指标的唯一护栏是标准库中的留存率。退款、投诉、支付失败、价格感知、SKU 挤占和复购变化写入风险说明或上线监控，不作为额外实验指标。

### 常见误判

- 只看短期收入上涨，不看退款、复购和留存。
- 把支付链路实验直接用总收入判断，忽略链路曝光量和支付成功率。
- 价格或折扣实验不拆国家、平台、历史付费、价格敏感人群。
- 弹窗/入口实验只看点击率，忽略后续支付和体验损伤。

### 不确定时的回答边界

没有价格、国家、平台、历史付费层级和退款数据时，不要直接判断价格策略可上线。可以给支付漏斗、收入指标和风险说明/上线监控建议。

## 留存/活跃

### 识别关键词

新用户、活跃、留存、D1、D7、D30、任务、签到、召回、push、回访、首日行为、成长、激励。

### 核心目标

提升用户持续使用、关键行为完成和关系/内容消费沉淀。

### 可选核心指标

- D1、D7、D30 留存。
- 次日/7日活跃率、回访率、目标行为留存。
- 新用户激活率，当策略主要影响首日关键行为。

### 观察指标

首日关键行为、会话数、好友/关注/消息、内容消费、任务完成、push 到达、push 点击、回访路径。

### 唯一护栏与风险说明

留存类核心指标的唯一护栏是标准库中的收入 ARPU。卸载、通知关闭、投诉、负反馈和商业化/社交副作用写入风险说明或上线监控，不作为额外实验指标。

### 常见误判

- 只看 D1，不看 D7/D30 是否回落。
- 用激励拉高短期活跃，但没有证明关键行为沉淀。
- 不拆新用户来源、国家、语言、注册渠道和用户质量。
- 把触达点击当留存改善。

### 不确定时的回答边界

没有激活定义、用户来源、首日关键行为和长期留存窗口时，不要判断留存策略长期有效。可以先判断是否需要补关键行为和中长期护栏。

## 直播语聊

### 识别关键词

直播、语聊房、房间、开播、进房、上麦、麦位、主播、观众、送礼、礼物、公屏、连麦、房间推荐。

### 核心目标

提升房间供需匹配、互动、停留和消费生态。

### 可选核心指标

- 进房率、有效进房率、房间停留时长。
- 上麦率、互动率、送礼收入、送礼转化率。
- 主播开播数或主播在线时长，当策略主要影响供给侧。

### 观察指标

房间曝光、点击、开播数、主播在线时长、观众转主播、关注、评论、公屏、礼物转化、房间复访。

### 风险说明与上线监控

主播流失、低质房间增多、房间举报、付费用户体验下降、新用户退出、冷启动房间曝光挤占。实验指标栏仍按核心指标类型只保留一个标准护栏。

### 常见误判

- 只看送礼收入，不看房间停留和互动质量。
- 只提高观众进房，不确认主播供给能承接。
- 推荐策略提升头部房间，但伤害中长尾房间生态。
- 把曝光提升误判为体验提升。

### 不确定时的回答边界

没有区分供给侧和消费侧目标时，不要直接选核心指标。先判断策略主要影响进房、停留、上麦、送礼，还是主播供给。

## 风控/安全

### 识别关键词

风控、审核、拦截、封禁、违规、作弊、刷量、举报、申诉、误伤、风险、解封、黑产。

### 核心目标

降低风险损失、违规暴露和作弊收益，同时控制正常用户误伤。

### 可选核心指标

- 风险损失、违规率、拦截率、审核命中率。
- 高风险行为下降率、复犯率。
- 正常用户通过率或误伤率，当策略主要改变风控阈值。

### 观察指标

申诉率、解封率、审核耗时、风险用户复犯、举报率、审核队列量、正常用户转化。

### 风险说明与上线监控

误伤率、正常用户留存/转化、客服压力、申诉处理时长、地区/人群偏差、体验投诉。实验指标栏仍按核心指标类型只保留一个标准护栏。

### 常见误判

- 只看拦截变强，不看误伤和正常用户损失。
- 实验组风险用户比例不均衡，导致结果不可比。
- 风控实验没有定义风险标签、命中口径和复犯窗口。
- 把短期风险下降当成长期安全改善。

### 不确定时的回答边界

没有风险标签口径、误伤定义和申诉/解封路径时，不要判断风控策略可全量。可以建议先小流量、强护栏、人工复核抽样。

## 课程/学习

### 识别关键词

课程、学习、试听、报名、老师、排课、完课、续费、课包、评价、学习路径、作业。

### 核心目标

提升试听、报名、完课、续费和学习体验。

### 可选核心指标

- 试听转化率、报名率、完课率、续费率。
- 课程收入、课包购买率。
- 老师响应或排课成功率，当策略主要影响供给承接。

### 观察指标

老师响应、排课成功、学习时长、课后评价、作业完成、课程路径完成、退款原因。

### 风险说明与上线监控

老师供给不足、退款、差评、完课下降、学习体验下降、低质线索增加、客服压力。实验指标栏仍按核心指标类型只保留一个标准护栏。

### 常见误判

- 只看试听或报名转化，不看完课和退款。
- 前端转化提升超过老师供给承接能力。
- 把低质量报名当作有效增长。
- 没有拆课程类型、老师供给、国家和学习目标。

### 不确定时的回答边界

没有课程类型、供给能力和用户学习阶段时，不要直接判断转化提升就是有效。至少补完课、退款和老师承接的风险说明/上线监控。

## 社交/匹配/关系

### 识别关键词

匹配、推荐、打招呼、回复、消息、聊天、好友、关注、资料页、关系、互动、配对、say hi。

### 核心目标

提升有效连接、回复和长期关系沉淀。

### 可选核心指标

- 打招呼率、回复率、有效会话建立率。
- 好友添加率、关系沉淀率、消息互发率。
- 资料页到消息转化率，当策略主要影响资料页或入口。

### 观察指标

曝光、点击、资料页访问、消息发送、好友添加、匹配成功、对话轮次、次日会话回访。

### 风险说明与上线监控

举报、拉黑、骚扰、低质消息、女性/新用户体验下降、消息回复质量、留存受损。实验指标栏仍按核心指标类型只保留一个标准护栏。

### 常见误判

- 只看消息发送量，不看回复率和举报拉黑。
- 给发送侧更多机会，但伤害接收侧体验。
- 不拆性别、国家、语言、社交意图和新老用户。
- 把短期互动量当作关系质量。

### 不确定时的回答边界

没有接收侧体验和关系质量指标时，不要判断社交策略正向。必须至少补回复、举报/拉黑和留存护栏。

## Push/召回

### 识别关键词

push、通知、召回、唤醒、到达、点击、频控、退订、通知关闭、回访、提醒、触达。

### 核心目标

提升触达后的回访、目标行为转化和沉默用户唤醒。

### 可选核心指标

- push 点击率、召回率、回访率。
- 点击后目标行为转化率。
- 被召回用户 D1/D7 留存，当策略影响持续回访。

### 观察指标

到达率、展示、点击、点击后路径、频控命中、分人群效果、触达时段、文案/场景表现。

### 风险说明与上线监控

通知关闭、退订、卸载、投诉、打扰、长期留存下降、其他 push 入口挤占。实验指标栏仍按核心指标类型只保留一个标准护栏。

### 常见误判

- 只看点击率，不看点击后行为和长期影响。
- 不控制频控和触达重叠。
- 把高意愿用户自然回访当作 push 效果。
- 未拆沉默用户、活跃用户和新用户。

### 不确定时的回答边界

没有频控、触达重叠、用户活跃分层和点击后目标行为时，不要判断 push 策略值得扩大。先补回访和打扰护栏。
