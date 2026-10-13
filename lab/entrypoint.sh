#!/usr/bin/env bash
set -euo pipefail

if [[ -x /opt/ats/bin/traffic_server ]]; then
  PREFIX="/opt/ats"
elif [[ -x /usr/local/trafficserver/bin/traffic_server ]]; then
  PREFIX="/usr/local/trafficserver"
else
  echo "FAIL traffic_server-not-found" >&2
  ls -la /opt/ats/bin /usr/local/trafficserver/bin >&2 || true
  exit 1
fi

ETC="${PREFIX}/etc/trafficserver"
VAR="${PREFIX}/var"
export PATH="${PREFIX}/bin:${PATH}"

if [[ -d /lab/etc-common ]]; then
  cp -a /lab/etc-common/. "${ETC}/"
fi
if [[ -d /lab/etc-overlay ]]; then
  cp -a /lab/etc-overlay/. "${ETC}/"
fi

mkdir -p "${VAR}/trafficserver" "${VAR}/log/trafficserver"
chown -R nobody:nogroup "${VAR}/trafficserver" "${VAR}/log/trafficserver" || true

exec "${PREFIX}/bin/traffic_server"
