#!/usr/bin/env python3
"""
xView Dataset Download Helper
Helps download and prepare the xView dataset
"""

import os
import requests
import zipfile
from pathlib import Path
import subprocess


def download_xview_dataset():
    """Guide user through xView dataset download."""
    
    print("🛰️  xView Dataset Download Guide")
    print("=" * 50)
    print()
    print("The xView dataset requires registration. Here's how to get it:")
    print()
    print("1. Go to: https://challenge.xviewdataset.org")
    print("2. Click 'Register' or 'Sign Up' (it's free)")
    print("3. After registration, you'll get access to download:")
    print("   - xView_train.geojson (annotations)")
    print("   - train_images.zip (satellite images)")
    print()
    print("4. Download both files to your computer")
    print("5. Extract train_images.zip to get the train_images/ folder")
    print()
    print("Expected file structure:")
    print("xview_data/")
    print("├── xView_train.geojson")
    print("└── train_images/")
    print("    ├── 0000000.jpg")
    print("    ├── 0000001.jpg")
    print("    └── ...")
    print()
    
    # Check if user has the dataset
    dataset_path = input("Enter the path to your xView dataset folder (or press Enter to skip): ").strip()
    
    if dataset_path and os.path.exists(dataset_path):
        geojson_path = os.path.join(dataset_path, "xView_train.geojson")
        images_path = os.path.join(dataset_path, "train_images")
        
        if os.path.exists(geojson_path) and os.path.exists(images_path):
            print(f"✅ Found xView dataset at: {dataset_path}")
            return dataset_path
        else:
            print("❌ Dataset files not found. Please check the path.")
            return None
    else:
        print("⚠️  No dataset path provided. You'll need to download it manually.")
        print("   After downloading, run this script again with the correct path.")
        return None


def setup_dataset_structure(dataset_path):
    """Set up the dataset structure for our pipeline."""
    
    if not dataset_path:
        return False
    
    print(f"\n📁 Setting up dataset structure from: {dataset_path}")
    
    # Create symlinks or copy files to our project
    project_dir = Path("/home/ar-in-u-359/Desktop/YOLO")
    dataset_dir = project_dir / "xview_dataset"
    dataset_dir.mkdir(exist_ok=True)
    
    # Create symlinks to avoid copying large files
    geojson_src = Path(dataset_path) / "xView_train.geojson"
    images_src = Path(dataset_path) / "train_images"
    
    geojson_dst = dataset_dir / "xView_train.geojson"
    images_dst = dataset_dir / "train_images"
    
    try:
        if not geojson_dst.exists():
            if geojson_src.exists():
                geojson_dst.symlink_to(geojson_src.absolute())
                print(f"✅ Linked GeoJSON: {geojson_dst}")
            else:
                print(f"❌ GeoJSON not found: {geojson_src}")
                return False
        
        if not images_dst.exists():
            if images_src.exists():
                images_dst.symlink_to(images_src.absolute())
                print(f"✅ Linked images: {images_dst}")
            else:
                print(f"❌ Images folder not found: {images_src}")
                return False
        
        print(f"\n✅ Dataset ready at: {dataset_dir}")
        return str(dataset_dir)
        
    except Exception as e:
        print(f"❌ Error setting up dataset: {e}")
        return False


def main():
    print("🚀 xView Dataset Setup")
    print("=" * 30)
    
    # Try to find existing dataset
    dataset_path = download_xview_dataset()
    
    if dataset_path:
        # Set up the dataset structure
        final_path = setup_dataset_structure(dataset_path)
        if final_path:
            print(f"\n🎉 Dataset is ready!")
            print(f"   GeoJSON: {final_path}/xView_train.geojson")
            print(f"   Images: {final_path}/train_images/")
            print(f"\nNext step: Run the conversion script")
            return final_path
    
    print("\n📋 Manual Setup Required:")
    print("1. Download xView dataset from https://challenge.xviewdataset.org")
    print("2. Extract it to a folder")
    print("3. Run this script again with the path")
    return None


if __name__ == '__main__':
    main()
