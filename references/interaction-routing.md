# Interaction Routing

Use this reference when the user intent is ambiguous, the user provides only a short idea, or the conversation needs guided next-step choices.

## Modes

Choose one mode from the user's request:

| Mode | Trigger | Output contract |
| --- | --- | --- |
| Idea coaching | A rough idea, one-line strategy, or "帮我看看能不能做 AB" | Ask the next highest-impact question only. Do not output a review conclusion. |
| Existing plan review | A plan, outline, pasted proposal, or "review/检查/过一下方案" | Lead with conclusion, blockers, next action. Use `review-rubric.md`. |
| Plan generation | User wants to write or complete an AB plan | Ask missing hard-gate fields first. Draft after necessity, metrics, user range, trigger scene, grouping, data support, and sample/gray evidence or an explicit sample-risk note are known. Result-success rules and post-result actions are reminders, not required questions. |
| Sample/gray check | User asks about sample size, duration, gray, or mutual exclusion | Check traffic first, then metric type, then calculation inputs. Use `sample-size-gray.md`. |
| Configuration/readiness check | User asks whether the plan can configure or launch | Check the readiness boundary only after the design fields are clear. Do not reopen necessity unless the readiness gap exposes a design flaw. |
| Feishu document workflow | User asks to read, prepare, create, or update a Feishu document | Use Feishu/Lark as document I/O only. Do not treat document access as data-platform verification. |

## Short-Summon Behavior

If the user only says a short trigger such as `AB实验`, `帮我看个AB`, `review ab`, or `怎么写AB方案`, output the following compact ability panel as a complete unit. Do not summarize, reorder, or omit any of the six main capabilities or the `需要时，我也可以联动` section:

```text
你可以把 AB 实验想法、方案草稿或飞书链接发我，我可以帮你推进这些事：

1. 判断这个想法适不适合做 AB
   先看这个问题是否真的需要实验验证，还是更适合直接上线、先观察或先补数据。

2. 检查现有 AB 方案
   看目标、指标、人群、分组、周期和风险是否说清楚，哪里还会影响结论。

3. 从想法补成完整 AB 方案
   我会一步步追问关键信息，整理成运营、产品、数据、开发都能看懂的方案。

4. 判断要跑多少人、跑多久、怎么小流量验证
   帮你估算实验需要的用户量和时间，并判断是否适合先小范围上线。

5. 准备实验配置和上线前检查
   整理分组配置、进入人群、双端测试、数据回收和出问题后的恢复方案。

6. 实验结束后做复盘
   看结果是否可信，指标有没有变好，是否建议上线、停止、扩大或重做。

需要时，我也可以联动：
- DA / TA：分析数据、查看实验结果和分层表现
- CMS：检查并准备实验配置；涉及上线、停用或恢复原方案前，会先让你确认
- 飞书 / Lark：读取需求、整理方案或写入实验文档

你直接发方案、想法、链接，或者回数字都可以。
```

If the user replies only with a number, enter the corresponding mode and ask for the minimum source material needed.

Do not append a separate `已确认项`、`当前阶段`、`建议下一步` status block after this short-summon panel. The panel's final line already tells the user how to continue.

## Guided Next-Step Menus

At a meaningful stage boundary, offer 2-4 valid next steps instead of ending with an open prompt. Keep the choices on the same stage and include one custom-answer option.

Use menus only after answering the current request. Do not use menus when the correct next action is a single blocking question.

Examples:

```text
下一步可以继续：
1. 继续补实验必要性
2. 先确认核心指标
3. 生成当前待补齐版方案
4. 其他：你直接说想怎么继续
```

```text
现在方案可以继续往下走。下一步建议先定核心指标：
1. 用我推荐的核心指标
2. 你补业务侧已有指标
3. 先看观察/护栏指标
4. 其他：你直接说明
```

## Question Style

- Ask exactly one question by default.
- Provide choices only when choices reduce answer burden.
- Keep all choices on the same dimension.
- Mark at most one option as `（推荐）`.
- Always allow a custom answer when presenting options.
- Do not mix business value, causal validity, metric choice, implementation method, and launch checks in one option set.

## Output Boundaries

- Idea coaching: no conclusion labels, no full report, no long checklist.
- Formal review: conclusion first, then blockers and one next action.
- Plan generation: no polished full plan while hard-gate fields are absent.
- Feishu document workflow: produce content that can be pasted, or use Feishu/Lark document tooling when explicitly requested; do not claim data systems were checked through the document.
