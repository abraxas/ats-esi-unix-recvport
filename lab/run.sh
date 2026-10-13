#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

export COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-ats-esi-unix-recvport}"
export PYTHONUNBUFFERED=1
export CONTROL_URL="${CONTROL_URL:-http://127.0.0.1:18751}"
export POC_URL="${POC_URL:-http://127.0.0.1:18750}"

LABEL="ats-esi-unix-recvport"
WITNESS="ATS-ESI-UNIX-RECVPORT-WITNESS"
IMAGE="ats-10.2.0-lab:local"
LOCK="/tmp/ats-10.2.0-lab.lock"
ATS_SRC="$(cd ../../client-reviews/trafficserver/src && pwd)"

down() {
  echo "== docker compose down -v =="
  docker compose -p "${COMPOSE_PROJECT_NAME}" down -v --remove-orphans || true
}

trap down EXIT

fail_setup() {
  local reason="$1"
  echo "FAIL ${LABEL} ${reason} ${WITNESS}" | tee poc-last-run.txt
  exit 1
}

echo "== docker compose down (clean) =="
down

if ! docker image inspect python:3.13-slim >/dev/null 2>&1; then
  echo "== docker pull python:3.13-slim =="
  docker pull python:3.13-slim || fail_setup "python-image-pull-failed"
fi

# macOS has no flock(1); use fcntl so sibling labs can share the image lock.
pyflock() {
  local mode="$1"
  shift
  python3 - "${LOCK}" "${mode}" "$@" <<'PY'
import fcntl
import os
import subprocess
import sys

lock_path, mode, cmd = sys.argv[1], sys.argv[2], sys.argv[3:]
fd = os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o644)
flags = fcntl.LOCK_EX
if mode == "-n":
    flags |= fcntl.LOCK_NB
try:
    fcntl.flock(fd, flags)
except BlockingIOError:
    raise SystemExit(2)
raise SystemExit(subprocess.call(cmd))
PY
}

ensure_ats_image() {
  if docker image inspect "${IMAGE}" >/dev/null 2>&1; then
    echo "== ${IMAGE} present =="
    return 0
  fi
  echo "== wait for sibling ${IMAGE} (do not start a parallel compile) =="
  local i
  for i in $(seq 1 180); do
    if docker image inspect "${IMAGE}" >/dev/null 2>&1; then
      echo "== ${IMAGE} present after wait attempt=${i} =="
      return 0
    fi
    echo "shared-image-wait attempt=${i}"
    sleep 10
  done
  echo "== flock ${LOCK} docker build ${IMAGE} =="
  pyflock -w bash -c '
    docker image inspect "'"${IMAGE}"'" >/dev/null 2>&1 && exit 0
    docker build -t "'"${IMAGE}"'" -f Dockerfile "'"${ATS_SRC}"'"
  '
}

ensure_ats_image || fail_setup "ats-image-build-failed"

echo "== docker compose up =="
up_ok=0
for attempt in $(seq 1 6); do
  if docker compose -p "${COMPOSE_PROJECT_NAME}" up -d; then
    up_ok=1
    break
  fi
  echo "compose-up-retry attempt=${attempt}"
  sleep 12
  down
done
if [[ "${up_ok}" != 1 ]]; then
  fail_setup "compose-up-failed"
fi

echo "== wait ats-control ${CONTROL_URL}/health =="
ok=0
sleep 3
for i in $(seq 1 40); do
  code="$(curl -sS -o /dev/null -w '%{http_code}' --max-time 3 \
    -H 'Host: www.example.com' "${CONTROL_URL}/health" || true)"
  if [[ "${code}" == "200" ]]; then
    ok=1
    echo "control-ready attempt=${i}"
    break
  fi
  echo "control-wait attempt=${i} http=${code}"
  sleep 2
done
if [[ "${ok}" != 1 ]]; then
  echo "== compose logs (control not ready) =="
  docker compose -p "${COMPOSE_PROJECT_NAME}" logs --no-color --tail=80 || true
  fail_setup "control-ats-not-ready"
fi

echo "== wait ats-poc ${POC_URL}/health =="
ok=0
for i in $(seq 1 40); do
  code="$(curl -sS -o /dev/null -w '%{http_code}' --max-time 3 \
    -H 'Host: www.example.com' "${POC_URL}/health" || true)"
  if [[ "${code}" == "200" ]]; then
    ok=1
    echo "poc-ready attempt=${i}"
    break
  fi
  echo "poc-wait attempt=${i} http=${code}"
  sleep 2
done
if [[ "${ok}" != 1 ]]; then
  echo "== compose logs (poc not ready) =="
  docker compose -p "${COMPOSE_PROJECT_NAME}" logs --no-color --tail=80 || true
  fail_setup "poc-ats-not-ready"
fi

echo "== poc.py =="
set +e
python3 ./poc.py | tee poc-last-run.txt
rc=${PIPESTATUS[0]}
set -e

if ! tail -n1 poc-last-run.txt 2>/dev/null | grep -qE '^(SUCCESS|FAIL) '; then
  echo "FAIL ${LABEL} poc-exit=${rc} ${WITNESS}" >> poc-last-run.txt
  rc=1
fi

exit "${rc}"
