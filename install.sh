#!/usr/bin/env bash

set -e

echo "=== Python Virtual Environment Setup Script ==="

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: python3 not found. Please install Python 3."
    exit 1
fi

echo "[1/4] Creating virtual environment (.venv)…"
python3 -m venv .venv

echo "[2/4] Activating virtual environment…"
# shellcheck disable=SC1091
source .venv/bin/activate

echo "[3/4] Upgrading pip…"
pip install --upgrade pip

echo "[4/4] Installing dependencies from requirements.txt…"
pip install -r requirements.txt

echo "Installation complete!"
echo "To activate the environment, run:"
echo "   source .venv/bin/activate"