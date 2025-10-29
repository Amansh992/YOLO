#!/usr/bin/env python3
"""
Quick Extract xView ZIP - Just provide the path as argument
Usage: python extract_xview.py /path/to/xview.zip
"""

import sys
import os
import zipfile
from pathlib import Path


def extract_xview(zip_path, output_dir=None):
    """Extract xView dataset zip to organized structure."""
    
    if output_dir is None:
        output_dir = "/home/ar-in-u-359/Desktop/YOLO/xview_dataset"
    
    zip_path = Path(zip_path)
    output_dir = Path(output_dir)
    
    if not zip_path.exists():
        print(f"❌ ZIP file not found: {zip_path}")
        return False
    
    print(f"📦 Extracting {zip_path.name}...")
    print(f"   To: {output_dir}")
    print("   This may take 10-30 minutes for large files...\n")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            members = zip_ref.namelist()
            total = len(members)
            
            print(f"   Found {total} files in ZIP")
            print(f"   Extracting (this will take a while)...\n")
            
            # Extract all
            zip_ref.extractall(output_dir)
            
            print(f"\n✅ Extraction complete!")
            print(f"\n📁 Checking extracted files...")
            
            # Find GeoJSON
            geojson_files = list(output_dir.rglob("*.geojson"))
            if geojson_files:
                print(f"   ✅ GeoJSON: {geojson_files[0]}")
            
            # Count images
            jpg_count = len(list(output_dir.rglob("*.jpg")))
            png_count = len(list(output_dir.rglob("*.png")))
            
            if jpg_count > 0:
                print(f"   ✅ Found {jpg_count} JPG images")
            if png_count > 0:
                print(f"   ✅ Found {png_count} PNG images")
            
            # Find train_images folder
            train_img_dirs = [d for d in output_dir.rglob("train_images") if d.is_dir()]
            if train_img_dirs:
                print(f"   ✅ Images folder: {train_img_dirs[0]}")
            
            print(f"\n✅ Dataset ready at: {output_dir}")
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python extract_xview.py <path_to_zip_file>")
        print("\nExample:")
        print("  python extract_xview.py /home/ar-in-u-359/Downloads/xview.zip")
        sys.exit(1)
    
    zip_path = sys.argv[1]
    extract_xview(zip_path)
