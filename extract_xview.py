#!/usr/bin/env python3
"""
Extract and Setup xView Dataset from ZIP
"""

import os
import zipfile
import shutil
from pathlib import Path


def find_xview_zip():
    """Find xView zip file in common download locations."""
    
    print("🔍 Looking for xView dataset ZIP file...")
    
    # Common download locations
    search_paths = [
        "/home/ar-in-u-359/Downloads",
        "/home/ar-in-u-359/Desktop",
        "/home/ar-in-u-359",
    ]
    
    zip_files = []
    
    for search_path in search_paths:
        if os.path.exists(search_path):
            for file in os.listdir(search_path):
                if file.lower().endswith('.zip') and ('xview' in file.lower() or 'x-view' in file.lower()):
                    full_path = os.path.join(search_path, file)
                    zip_files.append(full_path)
                    print(f"  Found: {full_path}")
    
    return zip_files


def extract_xview_zip(zip_path, extract_to=None):
    """Extract xView dataset zip file."""
    
    if extract_to is None:
        extract_to = "/home/ar-in-u-359/Desktop/YOLO/xview_dataset"
    
    extract_to = Path(extract_to)
    extract_to.mkdir(parents=True, exist_ok=True)
    
    print(f"\n📦 Extracting {zip_path} to {extract_to}...")
    print("   This may take a while for large files...")
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Get list of files
            file_list = zip_ref.namelist()
            total_files = len(file_list)
            
            print(f"   Found {total_files} files in ZIP")
            
            # Extract all files
            zip_ref.extractall(extract_to)
            
            print(f"✅ Extraction complete!")
            
            # Check what was extracted
            check_extracted_files(extract_to)
            
            return str(extract_to)
            
    except zipfile.BadZipFile:
        print(f"❌ Error: {zip_path} is not a valid ZIP file")
        return None
    except Exception as e:
        print(f"❌ Error extracting: {e}")
        return None


def check_extracted_files(extract_path):
    """Check what files were extracted."""
    
    extract_path = Path(extract_path)
    
    print(f"\n📁 Checking extracted files in {extract_path}...")
    
    # Look for GeoJSON file
    geojson_files = list(extract_path.rglob("*.geojson"))
    if geojson_files:
        print(f"  ✅ Found GeoJSON: {geojson_files[0]}")
        geojson_path = geojson_files[0]
    else:
        print(f"  ⚠️  No GeoJSON file found")
        geojson_path = None
    
    # Look for images folder
    image_folders = []
    for folder in extract_path.rglob("train_images"):
        if folder.is_dir():
            image_folders.append(folder)
    
    if image_folders:
        images_path = image_folders[0]
        image_count = len(list(images_path.glob("*.jpg"))) + len(list(images_path.glob("*.png")))
        print(f"  ✅ Found images folder: {images_path}")
        print(f"  ✅ Found {image_count} images")
    else:
        # Maybe images are in root or different structure
        jpg_files = list(extract_path.rglob("*.jpg"))
        png_files = list(extract_path.rglob("*.png"))
        if jpg_files or png_files:
            print(f"  ✅ Found {len(jpg_files) + len(png_files)} image files")
            images_path = extract_path
        else:
            print(f"  ⚠️  No images found")
            images_path = None
    
    # Organize files if needed
    if geojson_path and images_path:
        # Check if they're in the same directory
        if geojson_path.parent == images_path.parent or geojson_path.parent == extract_path:
            print(f"\n✅ Files are organized correctly!")
            return str(geojson_path), str(images_path)
    
    # Try to reorganize
    print(f"\n📋 Organizing files...")
    return organize_extracted_files(extract_path, geojson_path, images_path)


def organize_extracted_files(base_path, geojson_path, images_path):
    """Organize extracted files into proper structure."""
    
    base_path = Path(base_path)
    organized_path = base_path / "organized"
    organized_path.mkdir(exist_ok=True)
    
    # Move/copy GeoJSON
    if geojson_path:
        geojson_src = Path(geojson_path)
        geojson_dst = organized_path / "xView_train.geojson"
        if not geojson_dst.exists():
            shutil.copy2(geojson_src, geojson_dst)
            print(f"  ✅ Copied GeoJSON to {geojson_dst}")
    
    # Move/copy images
    if images_path:
        images_src = Path(images_path)
        if images_src.is_dir():
            images_dst = organized_path / "train_images"
            if not images_dst.exists():
                shutil.copytree(images_src, images_dst)
                print(f"  ✅ Copied images to {images_dst}")
        else:
            # Images might be individual files
            images_dst = organized_path / "train_images"
            images_dst.mkdir(exist_ok=True)
            for img_file in base_path.rglob("*.jpg"):
                shutil.copy2(img_file, images_dst / img_file.name)
            for img_file in base_path.rglob("*.png"):
                shutil.copy2(img_file, images_dst / img_file.name)
            print(f"  ✅ Organized images to {images_dst}")
    
    geojson_final = organized_path / "xView_train.geojson"
    images_final = organized_path / "train_images"
    
    if geojson_final.exists() and images_final.exists():
        print(f"\n✅ Files organized at: {organized_path}")
        return str(geojson_final), str(images_final)
    
    return str(geojson_final) if geojson_final.exists() else None, str(images_final) if images_final.exists() else None


def main():
    print("🛰️  xView Dataset ZIP Extractor")
    print("=" * 50)
    
    # Find ZIP files
    zip_files = find_xview_zip()
    
    if not zip_files:
        print("\n❌ No xView ZIP file found in common locations")
        print("\nPlease provide the path to your ZIP file:")
        zip_path = input("Enter ZIP file path: ").strip()
        if zip_path and os.path.exists(zip_path):
            zip_files = [zip_path]
        else:
            print("❌ ZIP file not found. Please check the path.")
            return
    
    # Use first found ZIP
    zip_path = zip_files[0]
    print(f"\n📦 Using ZIP file: {zip_path}")
    
    # Extract
    extract_path = extract_xview_zip(zip_path)
    
    if extract_path:
        print(f"\n🎉 Dataset extracted successfully!")
        print(f"   Location: {extract_path}")
        print(f"\n✅ Ready to proceed with conversion!")


if __name__ == '__main__':
    main()
