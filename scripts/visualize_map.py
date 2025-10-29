#!/usr/bin/env python3
"""
GeoJSON Visualization Script
Visualize detections on maps using Folium
"""

import argparse
import json
import folium
from pathlib import Path
import geopandas as gpd
from shapely.geometry import box, Polygon
import pandas as pd
from ultralytics import YOLO
import cv2
import numpy as np
import yaml


def yolo_to_geo_coords(yolo_bbox, img_width, img_height, geo_bounds):
    """
    Convert YOLO bounding box to geographic coordinates.
    
    Args:
        yolo_bbox: [x_center, y_center, width, height] in normalized coordinates
        img_width: Image width in pixels
        img_height: Image height in pixels
        geo_bounds: [min_lon, min_lat, max_lon, max_lat] for the image
    
    Returns:
        GeoJSON polygon
    """
    x_center, y_center, width, height = yolo_bbox
    
    # Convert to pixel coordinates
    x_center_px = x_center * img_width
    y_center_px = y_center * img_height
    width_px = width * img_width
    height_px = height * img_height
    
    # Calculate corners
    xmin = x_center_px - width_px / 2
    ymin = y_center_px - height_px / 2
    xmax = x_center_px + width_px / 2
    ymax = y_center_px + height_px / 2
    
    # Convert to geographic coordinates
    min_lon, min_lat, max_lon, max_lat = geo_bounds
    
    lon_min = min_lon + (xmin / img_width) * (max_lon - min_lon)
    lon_max = min_lon + (xmax / img_width) * (max_lon - min_lon)
    lat_min = max_lat - (ymax / img_height) * (max_lat - min_lat)
    lat_max = max_lat - (ymin / img_height) * (max_lat - min_lat)
    
    # Create polygon
    polygon = Polygon([
        [lon_min, lat_min],
        [lon_max, lat_min],
        [lon_max, lat_max],
        [lon_min, lat_max],
        [lon_min, lat_min]
    ])
    
    return polygon


def create_detection_map(predictions_dir, output_html, class_names=None, geo_bounds=None):
    """
    Create interactive map visualization of detections.
    
    Args:
        predictions_dir: Directory containing prediction results
        output_html: Output HTML file path
        class_names: List of class names
        geo_bounds: Geographic bounds for images (optional)
    """
    predictions_dir = Path(predictions_dir)
    
    # Find all prediction files
    label_files = list(predictions_dir.glob('*.txt'))
    
    if not label_files:
        print("No prediction files found!")
        return
    
    # Create base map
    if geo_bounds:
        center_lat = (geo_bounds[1] + geo_bounds[3]) / 2
        center_lon = (geo_bounds[0] + geo_bounds[2]) / 2
    else:
        center_lat, center_lon = 0, 0
    
    m = folium.Map(location=[center_lat, center_lon], zoom_start=2)
    
    # Color map for classes
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 
              'lightred', 'beige', 'darkblue', 'darkgreen']
    
    # Process predictions
    detection_count = 0
    for label_file in label_files:
        image_file = label_file.parent.parent / 'images' / (label_file.stem + '.jpg')
        if not image_file.exists():
            image_file = label_file.parent.parent / (label_file.stem + '.jpg')
        
        if image_file.exists():
            img = cv2.imread(str(image_file))
            if img is not None:
                h, w = img.shape[:2]
                
                with open(label_file, 'r') as f:
                    for line in f:
                        parts = line.strip().split()
                        if len(parts) >= 5:
                            class_id = int(parts[0])
                            yolo_bbox = [float(x) for x in parts[1:5]]
                            
                            if geo_bounds:
                                polygon = yolo_to_geo_coords(yolo_bbox, w, h, geo_bounds)
                            else:
                                # Use dummy coordinates (you should provide actual geo bounds)
                                polygon = box(0, 0, 1, 1)
                            
                            class_name = class_names[class_id] if class_names and class_id < len(class_names) else f"Class {class_id}"
                            color = colors[class_id % len(colors)]
                            
                            # Add to map
                            folium.GeoJson(
                                gpd.GeoSeries([polygon]).to_json(),
                                style_function=lambda feature, c=color: {
                                    'fillColor': c,
                                    'color': c,
                                    'weight': 2,
                                    'fillOpacity': 0.5,
                                },
                                tooltip=f"{class_name}",
                                popup=folium.Popup(f"Class: {class_name}<br>Confidence: {parts[5] if len(parts) > 5 else 'N/A'}")
                            ).add_to(m)
                            
                            detection_count += 1
    
    print(f"Added {detection_count} detections to map")
    m.save(output_html)
    print(f"Map saved to: {output_html}")


def main():
    parser = argparse.ArgumentParser(description='Visualize detections on map')
    parser.add_argument('--predictions', type=str, required=True,
                        help='Directory containing prediction results')
    parser.add_argument('--output', type=str, default='detections_map.html',
                        help='Output HTML file')
    parser.add_argument('--data-yaml', type=str, default='dataset/data.yaml',
                        help='Path to data.yaml for class names')
    parser.add_argument('--bounds', type=float, nargs=4, default=None,
                        metavar=('MIN_LON', 'MIN_LAT', 'MAX_LON', 'MAX_LAT'),
                        help='Geographic bounds of images')
    
    args = parser.parse_args()
    
    # Load class names
    class_names = None
    if Path(args.data_yaml).exists():
        with open(args.data_yaml, 'r') as f:
            config = yaml.safe_load(f)
            class_names = config.get('names', [])
    
    create_detection_map(
        predictions_dir=args.predictions,
        output_html=args.output,
        class_names=class_names,
        geo_bounds=args.bounds
    )


if __name__ == '__main__':
    main()

