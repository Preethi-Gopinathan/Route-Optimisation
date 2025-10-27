#!/bin/bash
# -------------------------------
# Build script for Flask app (Elastic Beanstalk)
# -------------------------------

set -e  # stop on errors

ZIP_NAME="app.zip"

echo "🧹 Cleaning old build..."
rm -f cdk/$ZIP_NAME || true
rm -f $ZIP_NAME || true

echo "📦 Creating deployment zip..."
zip -r $ZIP_NAME app.py requirements.txt .ebextensions/ > /dev/null

echo "📂 Moving zip to CDK folder..."
mv $ZIP_NAME cdk/

echo "✅ Build complete: cdk/$ZIP_NAME"
