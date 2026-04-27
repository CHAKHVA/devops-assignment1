#!/usr/bin/env bash
#
# Smoke-test a deployed Render service.
#
# Usage: scripts/smoke.sh <base-url> <expected-color> <expected-sha>
#
#   base-url        e.g. https://app-green.onrender.com
#   expected-color  "blue" or "green"
#   expected-sha    full git SHA of the commit that should be live
#                   (the script compares the first 7 chars)
#
# Behaviour:
#   * Polls <base-url>/version every 15s for up to 10 minutes, waiting
#     until it reports the expected short SHA. This handles cold starts
#     and ongoing Render builds on the free tier.
#   * Verifies /health returns {"status":"ok"} with HTTP 200.
#   * Verifies /version reports the expected color.
#
# Exits non-zero on any failure so the GitHub Actions job fails and the
# pipeline halts before promoting a bad build to production.

set -euo pipefail

if [ "$#" -ne 3 ]; then
    echo "usage: $0 <base-url> <expected-color> <expected-sha>" >&2
    exit 2
fi

BASE_URL="${1%/}"
EXPECTED_COLOR="$2"
EXPECTED_SHA_FULL="$3"
EXPECTED_SHA="${EXPECTED_SHA_FULL:0:7}"

DEADLINE=$((SECONDS + 600))
REPORTED_SHA=""

echo "Smoke test against ${BASE_URL}"
echo "  expected color: ${EXPECTED_COLOR}"
echo "  expected sha  : ${EXPECTED_SHA}"
echo

while [ "${SECONDS}" -lt "${DEADLINE}" ]; do
    if BODY=$(curl -fsSL --max-time 20 "${BASE_URL}/version" 2>/dev/null); then
        REPORTED_SHA=$(printf '%s' "${BODY}" | python3 -c \
            'import json,sys; print(json.load(sys.stdin).get("version",""))' \
            2>/dev/null || echo "")
        if [ "${REPORTED_SHA}" = "${EXPECTED_SHA}" ]; then
            echo "OK: service reports sha=${REPORTED_SHA}"
            break
        fi
        echo "  waiting... reported=${REPORTED_SHA:-<none>} expected=${EXPECTED_SHA}"
    else
        echo "  waiting... /version not reachable yet"
    fi
    sleep 15
done

if [ "${REPORTED_SHA}" != "${EXPECTED_SHA}" ]; then
    echo "::error::Timed out waiting for ${BASE_URL} to report sha ${EXPECTED_SHA} (last seen: ${REPORTED_SHA:-<none>})" >&2
    exit 1
fi

echo
echo "Checking /health ..."
HEALTH=$(curl -fsSL --max-time 20 "${BASE_URL}/health")
echo "  ${HEALTH}"
echo "${HEALTH}" | python3 -c \
    'import json,sys; d=json.load(sys.stdin); assert d=={"status":"ok"}, d'

echo
echo "Checking /version color ..."
COLOR=$(curl -fsSL --max-time 20 "${BASE_URL}/version" | python3 -c \
    'import json,sys; print(json.load(sys.stdin).get("color",""))')
echo "  reported color: ${COLOR}"
if [ "${COLOR}" != "${EXPECTED_COLOR}" ]; then
    echo "::error::Expected color ${EXPECTED_COLOR} but service reported ${COLOR}" >&2
    exit 1
fi

echo
echo "Smoke test PASSED for ${BASE_URL}"
