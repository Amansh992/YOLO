#!/usr/bin/env python3
"""
Enhanced xView GeoJSON to YOLO Format Converter
Converts xView dataset annotations from GeoJSON format to YOLO format
with comprehensive error handling, statistics, and validation.
"""

import os
import json
import cv2
import yaml
import numpy as np
import geopandas as gpd
from tqdm import tqdm
from pathlib import Path
from collections import defaultdict
import argparse


class xViewToYOLOConverter:
    def __init__(self, geojson_path, images_dir, output_dir, classes_config=None, use_simplified=True):
        """
        Initialize the converter.
        
        Args:
            geojson_path: Path to xView GeoJSON annotation file
            images_dir: Directory containing training images
            output_dir: Output directory for YOLO format dataset
            classes_config: Path to YAML file with class mappings (optional)
            use_simplified: Whether to use simplified class set
        """
        self.geojson_path = geojson_path
        self.images_dir = Path(images_dir)
        self.output_dir = Path(output_dir)
        self.use_simplified = use_simplified
        
        # Load class mappings
        self.class_map = self._load_class_mapping(classes_config)
        
        # Statistics
        self.stats = {
            'total_images': 0,
            'processed_images': 0,
            'skipped_images': 0,
            'total_objects': 0,
            'objects_by_class': defaultdict(int),
            'missing_images': [],
            'invalid_annotations': 0
        }
        
        # Create output directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.labels_dir = self.output_dir / 'labels'
        self.labels_dir.mkdir(exist_ok=True)
    
    def _load_class_mapping(self, config_path=None):
        """Load class mapping from config file or use default."""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                mapping_key = 'simplified_classes' if self.use_simplified else 'classes'
                class_dict = config.get(mapping_key, {})
        else:
            # Default simplified mapping
            class_dict = {
                11: 0,  # Fixed-Wing Aircraft
                12: 1,  # Small Vehicle
                13: 2,  # Large Vehicle
                15: 3,  # Truck
                21: 4,  # Passenger Vehicle
                37: 5,  # Ship
                52: 6,  # Building
                57: 7,  # Helipad
                58: 8,  # Storage Tank
                59: 9,  # Shipping Container
            }
        
        # Convert to integer mapping (xView ID -> YOLO class ID)
        class_map = {}
        yolo_id = 0
        for xview_id, class_name in sorted(class_dict.items()):
            class_map[int(xview_id)] = yolo_id
            yolo_id += 1
        
        return class_map
    
    def _extract_bbox_from_geometry(self, geometry):
        """Extract bounding box coordinates from GeoJSON geometry."""
        if geometry is None:
            return None
        
        try:
            if hasattr(geometry, 'bounds'):
                xmin, ymin, xmax, ymax = geometry.bounds
                return [xmin, ymin, xmax, ymax]
            elif isinstance(geometry, dict):
                if geometry.get('type') == 'Polygon':
                    coords = geometry['coordinates'][0]
                    x_coords = [c[0] for c in coords]
                    y_coords = [c[1] for c in coords]
                    return [min(x_coords), min(y_coords), max(x_coords), max(y_coords)]
        except Exception as e:
            print(f"Error extracting bbox: {e}")
            return None
        
        return None
    
    def _bbox_to_yolo_format(self, bbox, img_width, img_height):
        """Convert bounding box to YOLO format (normalized center x, center y, width, height)."""
        xmin, ymin, xmax, ymax = bbox
        
        # Clamp coordinates to image bounds
        xmin = max(0, min(xmin, img_width))
        ymin = max(0, min(ymin, img_height))
        xmax = max(0, min(xmax, img_width))
        ymax = max(0, min(ymax, img_height))
        
        # Calculate center and dimensions
        x_center = ((xmin + xmax) / 2.0) / img_width
        y_center = ((ymin + ymax) / 2.0) / img_height
        box_width = (xmax - xmin) / img_width
        box_height = (ymax - ymin) / img_height
        
        # Validate normalized coordinates
        if box_width <= 0 or box_height <= 0 or x_center < 0 or y_center < 0:
            return None
        
        return f"{x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}"
    
    def convert(self):
        """Main conversion function."""
        print(f"Loading GeoJSON annotations from: {self.geojson_path}")
        gdf = gpd.read_file(self.geojson_path)
        print(f"Loaded {len(gdf)} annotations")
        
        # Get all image files
        image_files = (list(self.images_dir.glob('*.jpg')) + 
                      list(self.images_dir.glob('*.png')) + 
                      list(self.images_dir.glob('*.tif')) + 
                      list(self.images_dir.glob('*.tiff')))
        self.stats['total_images'] = len(image_files)
        
        print(f"Found {len(image_files)} images")
        print(f"Using {len(self.class_map)} classes")
        
        # Group annotations by image_id
        annotations_by_image = defaultdict(list)
        
        for idx, row in gdf.iterrows():
            # Extract image_id from properties
            image_id = None
            if hasattr(row, 'image_id'):
                image_id = row['image_id']
            elif 'image_id' in row:
                image_id = row['image_id']
            elif 'feature_id' in row:
                # xView feature_id format: image_id.object_id
                image_id = str(row['feature_id']).split('.')[0]
            
            if image_id:
                annotations_by_image[str(image_id)].append(row)
        
        print(f"Found annotations for {len(annotations_by_image)} images")
        
        # Process each image
        for image_file in tqdm(image_files, desc="Converting annotations"):
            image_name = image_file.stem  # Without extension
            image_filename = image_file.name  # With extension
            
            # Load image to get dimensions
            img = cv2.imread(str(image_file))
            if img is None:
                self.stats['skipped_images'] += 1
                self.stats['missing_images'].append(image_name)
                continue
            
            h, w = img.shape[:2]
            
            # Get annotations for this image - try both with and without extension
            annotations = annotations_by_image.get(image_name, [])
            if not annotations:
                annotations = annotations_by_image.get(image_filename, [])
            
            if not annotations:
                # Create empty label file
                label_path = self.labels_dir / f"{image_name}.txt"
                label_path.touch()
                continue
            
            # Create label file
            label_path = self.labels_dir / f"{image_name}.txt"
            label_lines = []
            objects_count = 0
            
            for ann in annotations:
                try:
                    # Get class ID
                    class_type = None
                    if 'type' in ann:
                        class_type = int(ann['type'])
                    elif 'class_type' in ann:
                        class_type = int(ann['class_type'])
                    elif 'type_id' in ann:
                        class_type = int(ann['type_id'])
                    
                    if class_type not in self.class_map:
                        continue
                    
                    yolo_class_id = self.class_map[class_type]
                    
                    # Extract bounding box
                    bbox = None
                    if 'bounds_imcoords' in ann:
                        # xView format: "xmin,ymin,xmax,ymax"
                        coords_str = str(ann['bounds_imcoords'])
                        if coords_str and coords_str != 'nan':
                            coords = [float(x.strip()) for x in coords_str.split(',')]
                            if len(coords) == 4:
                                bbox = coords
                    elif ann.geometry is not None:
                        bbox = self._extract_bbox_from_geometry(ann.geometry)
                    
                    if not bbox:
                        self.stats['invalid_annotations'] += 1
                        continue
                    
                    # Convert to YOLO format
                    yolo_line = self._bbox_to_yolo_format(bbox, w, h)
                    if yolo_line:
                        label_lines.append(f"{yolo_class_id} {yolo_line}\n")
                        objects_count += 1
                        self.stats['objects_by_class'][class_type] += 1
                
                except Exception as e:
                    self.stats['invalid_annotations'] += 1
                    continue
            
            # Write label file
            if label_lines:
                with open(label_path, 'w') as f:
                    f.writelines(label_lines)
                self.stats['processed_images'] += 1
                self.stats['total_objects'] += objects_count
        
        self._print_statistics()
        return self.stats
    
    def _print_statistics(self):
        """Print conversion statistics."""
        print("\n" + "="*60)
        print("CONVERSION STATISTICS")
        print("="*60)
        print(f"Total images found: {self.stats['total_images']}")
        print(f"Images processed: {self.stats['processed_images']}")
        print(f"Images skipped: {self.stats['skipped_images']}")
        print(f"Total objects: {self.stats['total_objects']}")
        print(f"Invalid annotations: {self.stats['invalid_annotations']}")
        print(f"\nObjects by class:")
        for class_id, count in sorted(self.stats['objects_by_class'].items()):
            print(f"  Class {class_id}: {count}")
        if self.stats['missing_images']:
            print(f"\nMissing images (first 10): {self.stats['missing_images'][:10]}")
        print("="*60)


def main():
    parser = argparse.ArgumentParser(description='Convert xView GeoJSON to YOLO format')
    parser.add_argument('--geojson', type=str, required=True,
                        help='Path to xView GeoJSON annotation file')
    parser.add_argument('--images', type=str, required=True,
                        help='Directory containing training images')
    parser.add_argument('--output', type=str, default='dataset/labels',
                        help='Output directory for YOLO labels')
    parser.add_argument('--classes-config', type=str, default='config/xview_classes.yaml',
                        help='Path to classes configuration YAML file')
    parser.add_argument('--use-simplified', action='store_true', default=True,
                        help='Use simplified class set')
    
    args = parser.parse_args()
    
    converter = xViewToYOLOConverter(
        geojson_path=args.geojson,
        images_dir=args.images,
        output_dir=args.output,
        classes_config=args.classes_config if os.path.exists(args.classes_config) else None,
        use_simplified=args.use_simplified
    )
    
    converter.convert()


if __name__ == '__main__':
    main()

