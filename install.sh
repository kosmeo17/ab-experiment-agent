#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${AB_EXPERIMENT_AGENT_REPO_URL:-}"
TARGET="${CODEX_HOME:-$HOME/.codex}/skills/ab-experiment-agent"

if [[ -z "$REPO_URL" ]]; then
  cat >&2 <<'MSG'
请先提供仓库地址，例如：

AB_EXPERIMENT_AGENT_REPO_URL="https://github.com/你的用户名/ab-experiment-agent.git" bash install.sh

或者直接运行：

mkdir -p ~/.codex/skills
git clone https://github.com/你的用户名/ab-experiment-agent.git ~/.codex/skills/ab-experiment-agent
MSG
  exit 1
fi

mkdir -p "$(dirname "$TARGET")"

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

echo "请重启 Codex 后使用：\$ab-experiment-agent 帮我看一个 AB 实验"
