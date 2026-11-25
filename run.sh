#! /usr/bin/env bash

## This script runs the server using the configured environment made with the setup.sh script.
## It feeds all arguments from the CLI to the script

set -euo pipefail

cd "$(dirname "$0")"
exec .venv/bin/python src/main.py "$@"
