#!/bin/bash
# Script to push YOLO project to GitHub
# Usage: ./push_to_github.sh

echo "🚀 Pushing YOLOv12 project to GitHub..."
echo "========================================"

# Navigate to project
cd /home/ar-in-u-359/Desktop/YOLO

# Check if repository is clean
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  Uncommitted changes detected!"
    echo "Committing changes..."
    git add .
    git commit -m "Update project files"
fi

# Show remote URL
echo "📍 Remote URL:"
git remote -v

echo ""
echo "📤 Attempting to push to GitHub..."
echo ""

# Try to push
git push -u origin main

echo ""
echo "========================================"
if [ $? -eq 0 ]; then
    echo "✅ Successfully pushed to GitHub!"
    echo "🔗 Repository: https://github.com/Amansh992/YOLO"
else
    echo "❌ Push failed - need authentication"
    echo ""
    echo "Please try one of these options:"
    echo ""
    echo "Option 1: Use GitHub Desktop (Easiest)"
    echo "  1. Install GitHub Desktop"
    echo "  2. Add repository: /home/ar-in-u-359/Desktop/YOLO"
    echo "  3. Click 'Publish repository'"
    echo ""
    echo "Option 2: Manual Upload via GitHub Web"
    echo "  1. Go to: https://github.com/Amansh992/YOLO"
    echo "  2. Click 'uploading an existing file'"
    echo "  3. Drag and drop your project folder"
    echo ""
    echo "Option 3: Use GitHub CLI"
    echo "  1. Run: gh auth login"
    echo "  2. Run: git push -u origin main"
fi
