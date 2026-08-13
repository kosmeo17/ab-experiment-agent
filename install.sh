#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${AB_EXPERIMENT_AGENT_REPO_URL:-https://github.com/kosmeo17/ab-experiment-agent.git}"
CODEX_ROOT="${CODEX_HOME:-$HOME/.codex}"
SKILLS_DIR="$CODEX_ROOT/skills"
TARGET="$SKILLS_DIR/ab-experiment-agent"
DA_HOME="${DA_AGENTS_HOME:-$HOME/Projects/da_agents_v2}"
GIT_USERNAME="${AB_EXPERIMENT_AGENT_GIT_USERNAME:-oauth2}"
GIT_TOKEN="${AB_EXPERIMENT_AGENT_GIT_TOKEN:-}"
ASKPASS_FILE=""

mkdir -p "$SKILLS_DIR"

cleanup() {
  if [[ -n "$ASKPASS_FILE" && -f "$ASKPASS_FILE" ]]; then
    rm -f "$ASKPASS_FILE"
  fi
}
trap cleanup EXIT

setup_git_auth() {
  if [[ "$REPO_URL" =~ ^https?://[^/]+@ ]]; then
    echo "AB_EXPERIMENT_AGENT_REPO_URL 不能包含账号、token 或密码。" >&2
    echo "请使用干净仓库地址，并通过 AB_EXPERIMENT_AGENT_GIT_TOKEN 或本机 git 凭据提供认证。" >&2
    exit 1
  fi

  if [[ -z "$GIT_TOKEN" ]]; then
    return
  fi

  ASKPASS_FILE="$(mktemp "${TMPDIR:-/tmp}/ab-agent-git-askpass.XXXXXX")"
  chmod 700 "$ASKPASS_FILE"
  cat >"$ASKPASS_FILE" <<'EOF'
#!/usr/bin/env bash
case "$1" in
  *Username*) printf '%s\n' "${AB_EXPERIMENT_AGENT_GIT_USERNAME:-oauth2}" ;;
  *Password*) printf '%s\n' "${AB_EXPERIMENT_AGENT_GIT_TOKEN:-}" ;;
  *) printf '\n' ;;
esac
EOF

  export GIT_ASKPASS="$ASKPASS_FILE"
  export GIT_TERMINAL_PROMPT=0
}

set_target_remote_if_needed() {
  if [[ -n "${AB_EXPERIMENT_AGENT_REPO_URL:-}" && -d "$TARGET/.git" ]]; then
    git -C "$TARGET" remote set-url origin "$REPO_URL"
  fi
}

print_tool_version() {
  local bin="$1"
  if command -v "$bin" >/dev/null 2>&1; then
    local version
    version="$("$bin" --version 2>/dev/null || true)"
    if [[ -n "$version" ]]; then
      echo "  ✓ $bin 已安装：$version"
    else
      echo "  ✓ $bin 已安装"
    fi
  else
    echo "  ! $bin 未检测到"
  fi
}

check_git_remote_update() {
  local name="$1"
  local repo="$2"

  if [[ ! -d "$repo" ]]; then
    echo "  ! $name 未检测到：$repo"
    return
  fi

  if ! git -C "$repo" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "  ✓ $name 存在：$repo（非 git 仓库，无法检查远端更新）"
    return
  fi

  local branch current remote_url remote_head
  branch="$(git -C "$repo" rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
  current="$(git -C "$repo" rev-parse --short HEAD 2>/dev/null || true)"
  remote_url="$(git -C "$repo" remote get-url origin 2>/dev/null || true)"

  if [[ -z "$remote_url" || "$branch" == "HEAD" || -z "$branch" ]]; then
    echo "  ✓ $name 当前版本：${current:-unknown}（未配置可检查的 origin/branch）"
    return
  fi

  remote_head="$( (git -C "$repo" ls-remote --heads origin "$branch" 2>/dev/null || true) | awk 'NR==1 {print $1}')"
  if [[ -z "$remote_head" ]]; then
    echo "  ✓ $name 当前版本：${current:-unknown}（远端更新状态未确认）"
    return
  fi

  local local_head
  local_head="$(git -C "$repo" rev-parse HEAD 2>/dev/null || true)"
  if [[ "$local_head" == "$remote_head" ]]; then
    echo "  ✓ $name 当前分支 $branch 已是远端最新：${current:-unknown}"
  else
    echo "  ! $name 检测到远端可能有新版本：本地 ${current:-unknown}，远端 ${remote_head:0:7}"
    echo "    如需更新，请先确认后在对应仓库执行更新。安装脚本不会自动更新外部依赖。"
  fi
}

setup_git_auth

if [[ -d "$TARGET/.git" ]]; then
  set_target_remote_if_needed
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
print_tool_version "lark-cli"
echo "    如需读写飞书，请使用者本人完成 lark-cli auth login"

print_tool_version "cms-cli"
echo "    如需 CMS 操作，请使用者本人完成 cms-cli auth login"

echo
echo "依赖版本提醒："
check_git_remote_update "AB 实验助手" "$TARGET"
check_git_remote_update "DA Agents v2" "$DA_HOME"
echo "  ! CMS-CLI、lark-cli 和其他外部 agent 可能独立更新；正式查数、CMS 配置、用户标签、指标库读取前，建议先检查对应工具是否有新版本。"

echo
echo "使用日志初始化检查："
if [[ -f "$TARGET/scripts/ab_setup.py" ]]; then
  if python3 "$TARGET/scripts/ab_setup.py" --show >/dev/null 2>&1; then
    python3 "$TARGET/scripts/ab_setup.py" --mark-needs-setup >/dev/null 2>&1 || true
    echo "  ✓ 日志初始化已完整（身份字段 + 已成功写过 setup 日志）"
  else
    python3 "$TARGET/scripts/ab_setup.py" --mark-needs-setup || true
    echo "  ! 检测到尚未完成日志初始化（老用户更新后常见）。"
    echo "    完整条件：姓名 / 部门 / Data-ai Token，并且成功写入一条 setup 日志。"
    echo "    重启 Codex 后，下一次 AB 设计请求会先补初始化；身份已齐时会自动写 setup，不重复追问。"
    echo "    也可手动检查：python3 \"$TARGET/scripts/ab_setup.py\" --show"
    echo "    未完成前不会进入正式实验设计，也无法按新规则上传使用日志。"
  fi
else
  echo "  ! 未找到 scripts/ab_setup.py，跳过初始化检查"
fi

if [[ -n "$GIT_TOKEN" ]]; then
  echo
  echo "Git 认证：已使用临时环境变量读取 token；脚本不会输出 token，也不会把 token 写入仓库。"
fi
