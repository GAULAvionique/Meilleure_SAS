#! /usr/bin/env bash

## This script setups the environment.

# Makes it stop on fails and errors
set -euo pipefail

# sets CWD to repo root
cd "$(dirname "$0")"


dev=false
check=false
for arg in "$@"; do
	case "$arg" in
		--dev)     		dev=true ;;
		-C|--check)   check=true;;
		-h|--help) echo "usage: $0 [--dev]"; exit 0 ;;
		*)         echo "unknown option: $arg" >&2; exit 2 ;;
	esac
done

pin=$(tr -d '[:space:]' < .python-version)

## checks the venv
# checks if venv exists
if [[ -d .venv ]]; then

	# the python binary at the pinned version is in the venv
	if [[ -x ".venv/bin/python$pin" ]]; then

		# the python binary sucessfully runs
		if ".venv/bin/python$pin" -c 'pass' 2>/dev/null; then
			echo "python$pin is properly installed"
		else
			echo "python$pin fails to start properly"
			exit 78   # not sure of the exit code to put here
		fi

	# the pinned version of the binary is not found
	else
		echo "python$pin not found in .venv"

		if $check; then
			echo "--check flag detected, skipping venv installation"
			exit 78
		fi

		echo "removing current venv..."
		rm -rf .venv
	fi

fi


# sets the venv
if "python$pin" -c 'pass' >/dev/null 2>&1; then
	"python$pin" -m venv .venv
elif command -v mise >/dev/null 2>&1; then
  mise install "python@$pin"
	mise exec "python@$pin" -- python3 -m venv .venv
fi

if $dev; then
	echo "Installing dev dependencies..."
	.venv/bin/python -m pip install -r requirements-dev.txt
else
	# Installs basic stuff
	.venv/bin/python -m pip install -r requirements.txt
fi
