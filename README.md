# AB 实验助手

用于 Codex 的本地 skill，帮助运营、商业化、增长和产品同事处理 AB 实验设计与评审。

它不会直接把想法包装成完整方案，而是先判断实验是否应该存在，再按顺序补齐标准指标、对象、触发场景、数据支持、分组、互斥、样本量和灰度。

## 安装

复制下面命令到终端执行。它会安装 AB 实验助手，并同步安装 DA、CMS、飞书文档相关入口 skill：

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/kosmeo17/ab-experiment-agent/main/install.sh)
```

首次安装和后续更新使用同一条命令：

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/kosmeo17/ab-experiment-agent/main/install.sh)
```

执行完成后重启 Codex，让新版本生效。

安装脚本只安装或更新 skill 入口并检查本机环境，不会复制个人登录态或权限。飞书、CMS、数据查询仍需要使用者本人在本机授权。

## 本次更新

- 评估指标必须映射 AB 系统标准库，核心指标和护栏指标保留标准名称与 key；找不到时明确标记为`需新增标准指标`，不再临时自造指标名。
- 实验指标只保留一个核心指标和一个护栏指标。收入类核心指标的护栏是留存率；留存类核心指标的护栏是收入 ARPU。投诉、退款、负反馈等改为风险说明或上线监控。
- 实验对象只描述分组资格，实验场景只描述实际受影响的产品行为或位置，避免重复人群条件或补造入口。
- 每轮会说明当前已确认内容、所在阶段和唯一下一步；局部问题确认后会回到主流程最早未完成步骤。
- 所有 Gate 通过后会先询问是否创建飞书文档；如果没有目标空间写权限，会请求最小必要授权，不会默认生成本地 Markdown 替代飞书文档。

## 使用

推荐直接用自然语言说 AB 实验相关问题：

```text
帮我看一个 AB 实验
```

只要问题里提到 AB 实验、实验方案、指标、分组、灰度、样本量或实验复盘，Codex 会优先自动匹配到 AB 实验助手。

如果没有自动命中，或者想明确指定这个能力，再使用显式调用：

```text
$ab-experiment-agent 帮我 review 一个 Paywall 文案 AB 实验
```

`/` 菜单是否展示本地 skill 取决于 Codex 当前客户端能力，不作为安装成功的唯一判断。

## 适合场景

- 判断一个 AB 实验是否有必要做。
- 检查已有 AB 初稿的阻塞问题。
- 一步步补齐运营侧 AB 实验方案。
- 判断样本量、实验周期和灰度是否需要查数。
- 准备飞书方案草稿、DA 交接或 CMS 配置交接。

## 安装校验

重启 Codex 后，新开一个对话输入：

```text
帮我看一个 AB 实验
```

如果助手展示 AB 实验入口，或开始追问实验必要性、指标、对象、触发场景等问题，说明安装成功。若没有自动命中，再用 `$ab-experiment-agent 帮我看一个 AB 实验` 兜底验证。

需要确认依赖 skill 时，也可以分别输入：

```text
$da-agents
$cms
```

## 维护说明

- 主规则：`SKILL.md`
- 追问规则：`references/question-bank.md`
- 输出结构：`references/output-structures.md`
- 飞书文档边界：`references/feishu-export.md`
- 样本量与灰度：`references/sample-size-gray.md`

修改规则后，建议同步跑对话回归测试，避免老问题回退。
