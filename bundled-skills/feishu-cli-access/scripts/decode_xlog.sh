#!/usr/bin/env bash

set -u

usage() {
  cat <<'EOF'
Usage:
  decode_xlog.sh [-o output_dir] <xlog_file_or_dir>...

Environment:
  XLOG_PRIVATE_KEY   Override private key. By default the script reads
                     com.jerryfans.xlogDecoder flutter.KCryptPrivateKey.
  XLOG_DECODER_APP   Override XlogDecoder.app path. Default:
                     /Applications/XlogDecoder.app

Examples:
  decode_xlog.sh /tmp/bug/reporter
  decode_xlog.sh -o /tmp/bug/decoded /tmp/bug/reporter /tmp/bug/friend
EOF
}

output_dir=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    -o|--output)
      if [[ $# -lt 2 ]]; then
        echo "Missing value for $1" >&2
        exit 2
      fi
      output_dir="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
      shift
      break
      ;;
    -*)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
    *)
      break
      ;;
  esac
done

if [[ $# -eq 0 ]]; then
  usage >&2
  exit 2
fi

app_path="${XLOG_DECODER_APP:-/Applications/XlogDecoder.app}"
decoder_dir="$app_path/Contents/Frameworks/App.framework/Versions/A/Resources/flutter_assets/images/decode_mars_crypt_log_file"
decoder="$decoder_dir/decode_mars_crypt_log_file"

if [[ ! -x "$decoder" ]]; then
  echo "Xlog decoder executable not found: $decoder" >&2
  exit 1
fi

private_key="${XLOG_PRIVATE_KEY:-}"
if [[ -z "$private_key" ]]; then
  private_key="$(defaults read com.jerryfans.xlogDecoder flutter.KCryptPrivateKey 2>/dev/null | tr -d '[:space:]' || true)"
fi

if [[ -z "$private_key" ]]; then
  echo "Missing private key. Open XlogDecoder once or set XLOG_PRIVATE_KEY." >&2
  exit 1
fi

if [[ ! "$private_key" =~ ^[0-9A-Fa-f]+$ ]]; then
  echo "Invalid private key format: expected hex string." >&2
  exit 1
fi

if [[ -z "$output_dir" ]]; then
  output_dir="$(defaults read com.jerryfans.xlogDecoder flutter.KXlogSavePathKey 2>/dev/null || true)"
fi

if [[ -z "$output_dir" ]]; then
  output_dir="$PWD/xlog_decoded"
fi

mkdir -p "$output_dir"

decoded_count=0
failed_count=0

decode_one() {
  local input="$1"
  local out="$2"

  mkdir -p "$(dirname "$out")"

  (
    cd "$decoder_dir" || exit 1
    "$decoder" "$private_key" "$input" "$out"
  ) >/dev/null

  if [[ -s "$out" ]]; then
    decoded_count=$((decoded_count + 1))
    printf 'decoded: %s -> %s\n' "$input" "$out"
  else
    failed_count=$((failed_count + 1))
    printf 'failed:  %s\n' "$input" >&2
    rm -f "$out"
  fi
}

for input in "$@"; do
  if [[ -d "$input" ]]; then
    root_name="$(basename "$input")"
    while IFS= read -r -d '' file; do
      rel="${file#$input/}"
      out="$output_dir/$root_name/${rel%.xlog}.log"
      decode_one "$file" "$out"
    done < <(find "$input" -type f -name '*.xlog' -print0)
  elif [[ -f "$input" ]]; then
    parent_name="$(basename "$(dirname "$input")")"
    base_name="$(basename "$input")"
    out="$output_dir/${parent_name}_${base_name%.xlog}.log"
    decode_one "$input" "$out"
  else
    failed_count=$((failed_count + 1))
    printf 'missing: %s\n' "$input" >&2
  fi
done

printf 'done: decoded=%d failed=%d output=%s\n' "$decoded_count" "$failed_count" "$output_dir"

if [[ "$failed_count" -gt 0 ]]; then
  exit 1
fi
