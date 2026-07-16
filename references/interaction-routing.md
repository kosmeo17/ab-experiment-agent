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

If the user only says a short trigger such as `AB实验`, `帮我看个AB`, `review ab`, or `怎么写AB方案`, show a compact ability panel:

```text
你可以把 AB 实验方案发我，我能帮你做这些事：

1. Review 现有方案：判断是否值得做、指标/分组/样本量/风险是否过关
2. 从一个想法开始补方案：我每次只问一个最关键问题
3. 检查样本量和灰度：判断还缺哪些输入
4. 准备/写入飞书文档：先整理结构化内容；如你给链接或明确要求，我可以走飞书文档工具

你直接发方案或回数字都可以。
```

If the user replies only with a number, enter the corresponding mode and ask for the minimum source material needed.

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
