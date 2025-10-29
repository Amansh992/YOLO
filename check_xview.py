#!/usr/bin/env python3
"""
xView Dataset Setup - Non-interactive
"""

import os
from pathlib import Path


def check_xview_dataset():
    """Check if xView dataset exists in common locations."""
    
    print("🔍 Checking for xView dataset...")
    
    # Common locations to check
    possible_paths = [
        "/home/ar-in-u-359/Downloads/xview",
        "/home/ar-in-u-359/Desktop/xview", 
        "/home/ar-in-u-359/xview",
        "/home/ar-in-u-359/Desktop/YOLO/xview_dataset",
        "/home/ar-in-u-359/Desktop/YOLO/sample_data"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            geojson_path = os.path.join(path, "xView_train.geojson")
            images_path = os.path.join(path, "train_images")
            
            if os.path.exists(geojson_path) and os.path.exists(images_path):
                print(f"✅ Found xView dataset at: {path}")
                return path
            elif os.path.exists(geojson_path):
                print(f"⚠️  Found GeoJSON but no images folder at: {path}")
            elif os.path.exists(images_path):
                print(f"⚠️  Found images but no GeoJSON at: {path}")
    
    print("❌ xView dataset not found in common locations")
    return None


def create_download_instructions():
    """Create instructions for downloading xView dataset."""
    
    instructions = """
# 🛰️ xView Dataset Download Instructions

## Step 1: Register and Download
1. Go to: https://challenge.xviewdataset.org
2. Click "Register" or "Sign Up" (it's free)
3. After registration, download:
   - `xView_train.geojson` (annotations file)
   - `train_images.zip` (satellite images - ~100GB)

## Step 2: Extract and Organize
1. Extract `train_images.zip` to get `train_images/` folder
2. Place both files in a folder like `/home/ar-in-u-359/Downloads/xview/`

Expected structure:
```
/home/ar-in-u-359/Downloads/xview/
├── xView_train.geojson
└── train_images/
    ├── 0000000.jpg
    ├── 0000001.jpg
    └── ... (thousands of images)
```

## Step 3: Run the Pipeline
Once you have the dataset, run:
```bash
cd /home/ar-in-u-359/Desktop/YOLO
source venv/bin/activate
python scripts/convert_xview_to_yolo.py --geojson /path/to/xView_train.geojson --images /path/to/train_images --output dataset/labels
```

## Alternative: Use Sample Data
If you want to test the pipeline first, I can create sample data:
```bash
python create_sample_data.py
```
"""
    
    with open("XVIEW_DOWNLOAD_INSTRUCTIONS.md", "w") as f:
        f.write(instructions)
    
    print("📄 Created XVIEW_DOWNLOAD_INSTRUCTIONS.md")
    return instructions


def main():
    print("🚀 xView Dataset Checker")
    print("=" * 30)
    
    # Check if dataset exists
    dataset_path = check_xview_dataset()
    
    if dataset_path:
        print(f"\n✅ Dataset found! Ready to proceed with conversion.")
        print(f"   Path: {dataset_path}")
        return dataset_path
    else:
        print("\n📋 Dataset not found. Creating download instructions...")
        create_download_instructions()
        print("\n📖 Please follow the instructions in XVIEW_DOWNLOAD_INSTRUCTIONS.md")
        print("   Or let me know if you want to use sample data for testing.")
        return None


if __name__ == '__main__':
    main()
