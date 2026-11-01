#!/usr/bin/env bash
# Build ZMK firmware locally in Docker. Sources live in the zmk-workspace volume.
# Usage: scripts/build.sh [left|right|all] [extra west build args, e.g. -S zmk-usb-logging]
set -euo pipefail
cd "$(dirname "$0")/.."

target="${1:-all}"
shift || true
case "$target" in
  left|right) sides="$target" ;;
  all) sides="left right" ;;
  *) echo "usage: $0 [left|right|all] [west build args...]" >&2; exit 1 ;;
esac

mkdir -p firmware
docker run --rm \
  -v zmk-workspace:/workspace \
  -v "$PWD/config:/zmk-config/config:ro" \
  -v "$PWD/firmware:/out" \
  -w /workspace \
  zmkfirmware/zmk-build-arm:stable \
  bash -euc '
    if [ ! -d .west ]; then
      mkdir -p config && cp /zmk-config/config/west.yml config/
      west init -l config
    fi
    cp /zmk-config/config/west.yml config/
    west update --fetch-opt=--filter=tree:0
    west zephyr-export >/dev/null
    for side in '"$sides"'; do
      west build -p -s zmk/app -d build/$side -b nice_nano_v2 '"$*"' -- \
        -DSHIELD=skeletyl_$side -DZMK_CONFIG=/zmk-config/config
      cp build/$side/zephyr/zmk.uf2 /out/skeletyl_$side.uf2
    done
  '
ls -l firmware
