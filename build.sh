#!/bin/bash
set -e

echo "Creating Flask app ZIP..."
mkdir -p build
zip -r build/app.zip app.py requirements.txt
echo "Build complete: build/app.zip"
