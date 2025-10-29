#!/usr/bin/env python3
"""
Create Sample Dataset for Demo
Creates a small sample dataset to demonstrate the complete pipeline
"""

import os
import json
import cv2
import numpy as np
from pathlib import Path
import random


def create_sample_geojson(output_path, num_images=50):
    """Create a sample GeoJSON file with annotations."""
    
    # Sample classes from xView
    classes = [
        {"id": 11, "name": "Fixed-Wing Aircraft"},
        {"id": 12, "name": "Small Vehicle"},
        {"id": 13, "name": "Large Vehicle"},
        {"id": 15, "name": "Truck"},
        {"id": 21, "name": "Passenger Vehicle"},
        {"id": 37, "name": "Ship"},
        {"id": 52, "name": "Building"},
        {"id": 57, "name": "Helipad"},
        {"id": 58, "name": "Storage Tank"},
        {"id": 59, "name": "Shipping Container"}
    ]
    
    features = []
    
    for i in range(num_images):
        image_id = f"sample_image_{i:03d}.jpg"
        
        # Create 1-5 random objects per image
        num_objects = random.randint(1, 5)
        
        for j in range(num_objects):
            # Random class
            class_info = random.choice(classes)
            
            # Random bounding box (normalized coordinates)
            x_center = random.uniform(0.1, 0.9)
            y_center = random.uniform(0.1, 0.9)
            width = random.uniform(0.05, 0.3)
            height = random.uniform(0.05, 0.3)
            
            # Convert to pixel coordinates (assuming 1024x1024 image)
            img_width, img_height = 1024, 1024
            xmin = int((x_center - width/2) * img_width)
            ymin = int((y_center - height/2) * img_height)
            xmax = int((x_center + width/2) * img_width)
            ymax = int((y_center + height/2) * img_height)
            
            # Create feature
            feature = {
                "type": "Feature",
                "properties": {
                    "image_id": image_id,
                    "class_type": class_info["id"],
                    "bounds_imcoords": f"{xmin},{ymin},{xmax},{ymax}",
                    "feature_id": f"{image_id}.{j}"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [xmin, ymin],
                        [xmax, ymin],
                        [xmax, ymax],
                        [xmin, ymax],
                        [xmin, ymin]
                    ]]
                }
            }
            features.append(feature)
    
    # Create GeoJSON
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    
    with open(output_path, 'w') as f:
        json.dump(geojson, f, indent=2)
    
    print(f"Created sample GeoJSON with {len(features)} annotations for {num_images} images")


def create_sample_images(images_dir, num_images=50):
    """Create sample satellite-like images."""
    
    images_dir = Path(images_dir)
    images_dir.mkdir(parents=True, exist_ok=True)
    
    for i in range(num_images):
        # Create a 1024x1024 image with random satellite-like appearance
        img = np.random.randint(50, 200, (1024, 1024, 3), dtype=np.uint8)
        
        # Add some texture
        noise = np.random.randint(-20, 20, (1024, 1024, 3), dtype=np.int16)
        img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        
        # Add some random rectangular "objects" to make it look more realistic
        for _ in range(random.randint(2, 8)):
            x1 = random.randint(0, 900)
            y1 = random.randint(0, 900)
            x2 = x1 + random.randint(50, 200)
            y2 = y1 + random.randint(50, 200)
            x2 = min(x2, 1023)
            y2 = min(y2, 1023)
            
            color = [random.randint(100, 255) for _ in range(3)]
            cv2.rectangle(img, (x1, y1), (x2, y2), color, -1)
        
        # Save image
        image_path = images_dir / f"sample_image_{i:03d}.jpg"
        cv2.imwrite(str(image_path), img)
    
    print(f"Created {num_images} sample images in {images_dir}")


def main():
    # Create sample data directory
    sample_dir = Path("sample_data")
    sample_dir.mkdir(exist_ok=True)
    
    # Create sample GeoJSON
    geojson_path = sample_dir / "sample_xview.geojson"
    create_sample_geojson(geojson_path, num_images=50)
    
    # Create sample images
    images_dir = sample_dir / "images"
    create_sample_images(images_dir, num_images=50)
    
    print("\n" + "="*60)
    print("SAMPLE DATASET CREATED!")
    print("="*60)
    print(f"GeoJSON: {geojson_path}")
    print(f"Images: {images_dir}")
    print(f"Total images: 50")
    print(f"Total annotations: ~150-250")
    print("="*60)


if __name__ == '__main__':
    main()
