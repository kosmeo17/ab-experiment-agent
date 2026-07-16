#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${AB_EXPERIMENT_AGENT_REPO_URL:-https://github.com/kosmeo17/ab-experiment-agent.git}"
CODEX_ROOT="${CODEX_HOME:-$HOME/.codex}"
SKILLS_DIR="$CODEX_ROOT/skills"
TARGET="$SKILLS_DIR/ab-experiment-agent"
DA_HOME="${DA_AGENTS_HOME:-$HOME/Projects/da_agents_v2}"

mkdir -p "$SKILLS_DIR"

if [[ -d "$TARGET/.git" ]]; then
  git -C "$TARGET" pull --ff-only
  echo "已更新：$TARGET"
elif [[ -e "$TARGET" ]]; then
  echo "目标路径已存在但不是 git 仓库：$TARGET" >&2
  echo "请先手动备份或删除该目录，再重新安装。" >&2
  exit 1
else
  git clone "$REPO_URL" "$TARGET"
  echo "已安装：$TARGET"
fi

if [[ -d "$TARGET/bundled-skills" ]]; then
  for src in "$TARGET"/bundled-skills/*; do
    [[ -d "$src" ]] || continue
    name="$(basename "$src")"
    dest="$SKILLS_DIR/$name"
    mkdir -p "$dest"
    cp -R "$src"/. "$dest"/
    echo "已安装/更新依赖 skill：$name"
  done
fi

echo
echo "安装完成。请重启 Codex 后使用："
echo "  \$ab-experiment-agent 帮我看一个 AB 实验"
echo
echo "能力状态检查："
if command -v lark-cli >/dev/null 2>&1; then
  echo "  ✓ lark-cli 已安装；如需读写飞书，请使用者本人完成 lark-cli auth login"
else
  echo "  ! lark-cli 未检测到；飞书文档读写需要另行安装并授权"
fi

if command -v cms-cli >/dev/null 2>&1; then
  echo "  ✓ cms-cli 已安装；如需 CMS 操作，请使用者本人完成 cms-cli auth login"
else
  echo "  ! cms-cli 未检测到；CMS 查询/配置检查需要另行安装并授权"
fi

if [[ -d "$DA_HOME" ]]; then
  echo "  ✓ DA Agents v2 项目存在：$DA_HOME"
else
  echo "  ! 未检测到 DA Agents v2 项目：$DA_HOME"
  echo "    如需 \$da-agents 查数，请先安装该项目，或设置 DA_AGENTS_HOME 指向实际路径"
fi
