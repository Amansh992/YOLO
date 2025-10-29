#!/usr/bin/env python3
"""
Advanced Evaluation and Visualization Script
Provides comprehensive metrics, confusion matrices, and visualizations
"""

import argparse
import cv2
import numpy as np
from pathlib import Path
from ultralytics import YOLO
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
import json


class YOLOEvaluator:
    def __init__(self, model_path, data_yaml, conf_threshold=0.25, iou_threshold=0.45):
        """
        Initialize evaluator.
        
        Args:
            model_path: Path to trained YOLO model weights
            data_yaml: Path to data.yaml configuration file
            conf_threshold: Confidence threshold for predictions
            iou_threshold: IoU threshold for NMS
        """
        self.model = YOLO(model_path)
        self.data_yaml = data_yaml
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        
        # Load class names
        import yaml
        with open(data_yaml, 'r') as f:
            self.config = yaml.safe_load(f)
            self.class_names = self.config.get('names', [])
    
    def validate(self, save_json=False, save_hybrid=False):
        """Run validation and return metrics."""
        print("Running validation...")
        results = self.model.val(
            data=self.data_yaml,
            conf=self.conf_threshold,
            iou=self.iou_threshold,
            save_json=save_json,
            save_hybrid=save_hybrid
        )
        
        print("\n" + "="*60)
        print("VALIDATION RESULTS")
        print("="*60)
        print(f"mAP50: {results.box.map50:.4f}")
        print(f"mAP50-95: {results.box.map:.4f}")
        print(f"Precision: {results.box.mp:.4f}")
        print(f"Recall: {results.box.mr:.4f}")
        print("="*60)
        
        return results
    
    def predict_images(self, image_dir, output_dir, save_txt=False, save_conf=True):
        """
        Run predictions on images and save results.
        
        Args:
            image_dir: Directory containing images to predict
            output_dir: Directory to save predictions
            save_txt: Save prediction text files
            save_conf: Include confidence in output
        """
        image_dir = Path(image_dir)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        image_files = list(image_dir.glob('*.jpg')) + list(image_dir.glob('*.png'))
        print(f"Predicting on {len(image_files)} images...")
        
        results = self.model.predict(
            source=str(image_dir),
            conf=self.conf_threshold,
            iou=self.iou_threshold,
            save=True,
            save_txt=save_txt,
            save_conf=save_conf,
            project=str(output_dir.parent),
            name=output_dir.name
        )
        
        print(f"Predictions saved to: {output_dir}")
        return results
    
    def analyze_predictions(self, predictions_dir):
        """Analyze predictions and generate statistics."""
        predictions_dir = Path(predictions_dir)
        
        stats = {
            'total_images': 0,
            'total_detections': 0,
            'detections_by_class': defaultdict(int),
            'confidence_distribution': [],
            'objects_per_image': []
        }
        
        label_files = list(predictions_dir.glob('*.txt'))
        stats['total_images'] = len(label_files)
        
        for label_file in label_files:
            with open(label_file, 'r') as f:
                lines = f.readlines()
                stats['total_detections'] += len(lines)
                stats['objects_per_image'].append(len(lines))
                
                for line in lines:
                    parts = line.strip().split()
                    if len(parts) >= 6:  # class x y w h conf
                        class_id = int(parts[0])
                        conf = float(parts[5])
                        stats['detections_by_class'][class_id] += 1
                        stats['confidence_distribution'].append(conf)
        
        return stats
    
    def visualize_statistics(self, stats, output_path):
        """Create visualization plots for statistics."""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Detections by class
        classes = list(stats['detections_by_class'].keys())
        counts = [stats['detections_by_class'][c] for c in classes]
        class_names_plot = [self.class_names[c] if c < len(self.class_names) else f'Class {c}' for c in classes]
        
        axes[0, 0].barh(class_names_plot, counts)
        axes[0, 0].set_title('Detections by Class')
        axes[0, 0].set_xlabel('Count')
        
        # Confidence distribution
        if stats['confidence_distribution']:
            axes[0, 1].hist(stats['confidence_distribution'], bins=50, edgecolor='black')
            axes[0, 1].set_title('Confidence Distribution')
            axes[0, 1].set_xlabel('Confidence')
            axes[0, 1].set_ylabel('Frequency')
        
        # Objects per image
        axes[1, 0].hist(stats['objects_per_image'], bins=30, edgecolor='black')
        axes[1, 0].set_title('Objects per Image')
        axes[1, 0].set_xlabel('Number of Objects')
        axes[1, 0].set_ylabel('Frequency')
        
        # Summary statistics
        axes[1, 1].axis('off')
        summary_text = f"""
        Summary Statistics:
        
        Total Images: {stats['total_images']}
        Total Detections: {stats['total_detections']}
        Avg Detections/Image: {np.mean(stats['objects_per_image']):.2f}
        Median Detections/Image: {np.median(stats['objects_per_image']):.2f}
        Avg Confidence: {np.mean(stats['confidence_distribution']):.4f}
        """
        axes[1, 1].text(0.1, 0.5, summary_text, fontsize=12, verticalalignment='center')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Statistics visualization saved to: {output_path}")
        plt.close()


def main():
    parser = argparse.ArgumentParser(description='Evaluate YOLO model')
    parser.add_argument('--model', type=str, required=True,
                        help='Path to model weights')
    parser.add_argument('--data', type=str, required=True,
                        help='Path to data.yaml')
    parser.add_argument('--mode', type=str, default='val',
                        choices=['val', 'predict', 'both'],
                        help='Evaluation mode')
    parser.add_argument('--source', type=str, default=None,
                        help='Source directory for predictions')
    parser.add_argument('--output', type=str, default='results',
                        help='Output directory for predictions')
    parser.add_argument('--conf', type=float, default=0.25,
                        help='Confidence threshold')
    parser.add_argument('--iou', type=float, default=0.45,
                        help='IoU threshold')
    
    args = parser.parse_args()
    
    evaluator = YOLOEvaluator(
        model_path=args.model,
        data_yaml=args.data,
        conf_threshold=args.conf,
        iou_threshold=args.iou
    )
    
    if args.mode in ['val', 'both']:
        evaluator.validate(save_json=True)
    
    if args.mode in ['predict', 'both']:
        if args.source:
            results = evaluator.predict_images(
                image_dir=args.source,
                output_dir=args.output,
                save_txt=True
            )
            
            # Analyze predictions
            stats = evaluator.analyze_predictions(args.output)
            evaluator.visualize_statistics(stats, f"{args.output}/statistics.png")
        else:
            print("Warning: --source required for prediction mode")


if __name__ == '__main__':
    main()

