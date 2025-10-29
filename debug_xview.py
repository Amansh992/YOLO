#!/usr/bin/env python3
"""
Debug xView data structure
"""

import json
import os
from pathlib import Path

# Load GeoJSON
with open('/home/ar-in-u-359/Desktop/YOLO/xview_dataset/train_labels/xView_train.geojson', 'r') as f:
    data = json.load(f)

print("=== GeoJSON Structure ===")
print(f"Total features: {len(data['features'])}")

# Check first few features
for i in range(3):
    feature = data['features'][i]
    props = feature['properties']
    print(f"\nFeature {i}:")
    print(f"  Keys: {list(props.keys())}")
    print(f"  image_id: {props.get('image_id', 'NOT FOUND')}")
    print(f"  class_type: {props.get('class_type', 'NOT FOUND')}")
    print(f"  bounds_imcoords: {props.get('bounds_imcoords', 'NOT FOUND')}")

# Check image files
images_dir = Path('/home/ar-in-u-359/Desktop/YOLO/xview_dataset/train_images/train_images')
image_files = list(images_dir.glob('*.tif'))
print(f"\n=== Images ===")
print(f"Found {len(image_files)} .tif files")
print(f"First 5: {[f.name for f in image_files[:5]]}")

# Check overlap
image_ids = set()
for feature in data['features']:
    image_id = feature['properties'].get('image_id')
    if image_id:
        image_ids.add(image_id)

actual_files = {f.name for f in image_files}
overlap = image_ids.intersection(actual_files)

print(f"\n=== Overlap Analysis ===")
print(f"Unique image_ids in annotations: {len(image_ids)}")
print(f"Actual image files: {len(actual_files)}")
print(f"Overlap: {len(overlap)}")

# Test a specific file
test_file = list(overlap)[0]
print(f"\n=== Testing {test_file} ===")
print(f"File exists: {(images_dir / test_file).exists()}")

# Find annotations for this file
annotations_for_test = [f for f in data['features'] if f['properties'].get('image_id') == test_file]
print(f"Annotations for {test_file}: {len(annotations_for_test)}")

if annotations_for_test:
    ann = annotations_for_test[0]
    print(f"  Class type: {ann['properties'].get('class_type')}")
    print(f"  Bounds: {ann['properties'].get('bounds_imcoords')}")
