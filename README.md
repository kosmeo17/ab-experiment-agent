# AB 实验助手

用于 Codex 的本地 skill，帮助运营、商业化、增长和产品同事处理 AB 实验设计与评审。

它不会直接把想法包装成完整方案，而是先判断实验是否应该存在，再按顺序补齐指标、对象、触发场景、数据支持、分组、互斥、样本量和灰度。

## 安装

把本仓库克隆到 Codex skills 目录：

```bash
mkdir -p ~/.codex/skills
git clone <你的 GitHub 仓库地址> ~/.codex/skills/ab-experiment-agent
```

安装后重启 Codex。

如果已经安装过，更新方式是：

```bash
cd ~/.codex/skills/ab-experiment-agent
git pull
```

## 使用

推荐显式调用：

```text
$ab-experiment-agent 帮我看一个 AB 实验
```

也可以直接用自然语言：

```text
帮我 review 一个 Paywall 文案 AB 实验
```

如果 Codex 已正确加载本 skill，它会根据 `SKILL.md` 的 description 自动识别 AB 实验相关问题。`/` 菜单是否展示本地 skill 取决于 Codex 当前客户端能力，不作为安装成功的唯一判断。

## 适合场景

- 判断一个 AB 实验是否有必要做。
- 检查已有 AB 初稿的阻塞问题。
- 一步步补齐运营侧 AB 实验方案。
- 判断样本量、实验周期和灰度是否需要查数。
- 准备飞书方案草稿、DA 交接或 CMS 配置交接。

## 安装校验

重启 Codex 后，新开一个对话输入：

```text
$ab-experiment-agent 帮我看一个 AB 实验
```

如果助手展示 AB 实验入口，或开始追问实验必要性、指标、对象、触发场景等问题，说明安装成功。

## 维护说明

- 主规则：`SKILL.md`
- 追问规则：`references/question-bank.md`
- 输出结构：`references/output-structures.md`
- 飞书文档边界：`references/feishu-export.md`
- 样本量与灰度：`references/sample-size-gray.md`

修改规则后，建议同步跑对话回归测试，避免老问题回退。
