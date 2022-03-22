#!/usr/bin/env bash
# Setups the repository.

# Stop on errors
set -e

cd "$(dirname "$0")/.."

# Add default vscode settings if not existing
SETTINGS_FILE=./.vscode/settings.json
SETTINGS_TEMPLATE_FILE=./.vscode/settings.default.json
if [ ! -f "$SETTINGS_FILE" ]; then
    echo "Copy $SETTINGS_TEMPLATE_FILE to $SETTINGS_FILE."
    cp "$SETTINGS_TEMPLATE_FILE" "$SETTINGS_FILE"
fi

mkdir -p config

if [ ! -n "$DEVCONTAINER" ];then
  python3 -m venv venv
  source venv/bin/activate
fi

python3 -m pip install tox tox-pip-version colorlog pre-commit

pre-commit install
python3 -m pip install -e . --constraint requirements.txt --use-deprecated=legacy-resolver
