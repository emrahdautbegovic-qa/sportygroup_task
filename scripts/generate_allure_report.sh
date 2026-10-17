#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RESULTS_DIR="${ALLURE_RESULTS_DIR:-$ROOT_DIR/allure-results}"
REPORT_DIR="${ALLURE_REPORT_DIR:-$ROOT_DIR/allure-report}"
ALLURE_VERSION="2.46.1"
ALLURE_HOME="$ROOT_DIR/.tools/allure-$ALLURE_VERSION"
ALLURE_BIN="$ALLURE_HOME/bin/allure"
ALLURE_ARCHIVE="$ROOT_DIR/.tools/allure-$ALLURE_VERSION.tgz"
ALLURE_SHA256="37428164f310c8d137cfdd2c3a25d049b233261ddab13e1bd4dfd7627b5cbf8d"

if [[ ! -d "$RESULTS_DIR" ]]; then
    echo "Allure results directory not found: $RESULTS_DIR" >&2
    echo "Run the tests first; pytest writes results to allure-results/." >&2
    exit 1
fi

if [[ -z "$(find "$RESULTS_DIR" -type f -name '*-result.json' -print -quit)" ]]; then
    echo "No Allure test result files found in: $RESULTS_DIR" >&2
    echo "Run the tests first; pytest writes results to allure-results/." >&2
    exit 1
fi

if [[ ! -x "$ALLURE_BIN" ]]; then
    mkdir -p "$ROOT_DIR/.tools"
    curl --fail --location --silent --show-error --retry 3 \
        "https://github.com/allure-framework/allure2/releases/download/$ALLURE_VERSION/allure-$ALLURE_VERSION.tgz" \
        --output "$ALLURE_ARCHIVE"

    if command -v shasum >/dev/null 2>&1; then
        echo "$ALLURE_SHA256  $ALLURE_ARCHIVE" | shasum --check --status
    elif command -v sha256sum >/dev/null 2>&1; then
        echo "$ALLURE_SHA256  $ALLURE_ARCHIVE" | sha256sum --check --status
    else
        echo "Cannot verify Allure download: install shasum or sha256sum." >&2
        exit 1
    fi

    tar -xzf "$ALLURE_ARCHIVE" -C "$ROOT_DIR/.tools"
    rm "$ALLURE_ARCHIVE"
fi

"$ALLURE_BIN" generate --single-file "$RESULTS_DIR" --clean --report-dir "$REPORT_DIR"

if [[ ! -f "$REPORT_DIR/index.html" ]]; then
    echo "Allure did not produce the expected standalone report: $REPORT_DIR/index.html" >&2
    exit 1
fi

echo "Standalone Allure report: $REPORT_DIR/index.html"
