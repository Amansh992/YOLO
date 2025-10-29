#!/bin/bash
# Setup script for YOLOv12 xView project

set -e

echo "🛰️  YOLOv12 Satellite Detection Setup"
echo "======================================"

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo ""
echo "Creating project directories..."
mkdir -p dataset/images/{train,val,test}
mkdir -p dataset/labels/{train,val,test}
mkdir -p runs/detect
mkdir -p results
mkdir -p test_images

# Make scripts executable
echo ""
echo "Making scripts executable..."
chmod +x scripts/*.py
chmod +x dashboard/app.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Download xView dataset from https://xviewdataset.org"
echo "2. Run: python scripts/convert_xview_to_yolo.py --geojson <path> --images <path>"
echo "3. Run: python scripts/split_dataset.py --images <path> --labels dataset/labels"
echo "4. Run: python scripts/create_data_yaml.py --train dataset/images/train --val dataset/images/val"
echo "5. Run: python scripts/train.py --data dataset/data.yaml"
echo ""
echo "To activate the virtual environment later:"
echo "  source venv/bin/activate"

