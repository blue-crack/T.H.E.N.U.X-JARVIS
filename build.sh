#!/bin/bash
echo "============================================"
echo "THENUX Executable Builder"
echo "============================================"
echo ""

echo "[1/3] Installing PyInstaller..."
pip3 install pyinstaller
echo ""

echo "[2/3] Cleaning previous builds..."
rm -rf build dist __pycache__
echo ""

echo "[3/3] Building THENUX..."
pyinstaller thenux.spec
echo ""

if [ -f "dist/THENUX" ]; then
    echo "============================================"
    echo "Build successful!"
    echo "Location: dist/THENUX"
    echo "============================================"
else
    echo "Build failed! Check errors above."
fi
