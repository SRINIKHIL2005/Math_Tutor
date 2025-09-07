#!/bin/bash
# Render build script - Python 3.11 optimized
echo "🚀 Starting Render build..."
pip install --upgrade pip
pip install --no-cache-dir -r requirements-minimal.txt
echo "✅ Build completed successfully!"
