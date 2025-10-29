#!/usr/bin/env python3
"""
Dataset Splitting Script
Splits dataset into train/val/test sets with proper stratification
"""

import os
import random
import shutil
from pathlib import Path
import argparse
from collections import defaultdict


class DatasetSplitter:
    def __init__(self, images_dir, labels_dir, output_dir, train_ratio=0.8, val_ratio=0.15, test_ratio=0.05):
        """
        Initialize dataset splitter.
        
        Args:
            images_dir: Directory containing all images
            labels_dir: Directory containing all labels
            output_dir: Output directory for split dataset
            train_ratio: Ratio for training set
            val_ratio: Ratio for validation set
            test_ratio: Ratio for test set
        """
        self.images_dir = Path(images_dir)
        self.labels_dir = Path(labels_dir)
        self.output_dir = Path(output_dir)
        
        # Validate ratios
        total = train_ratio + val_ratio + test_ratio
        if abs(total - 1.0) > 0.01:
            raise ValueError(f"Ratios must sum to 1.0, got {total}")
        
        self.train_ratio = train_ratio
        self.val_ratio = val_ratio
        self.test_ratio = test_ratio
        
        # Create output directories
        self.train_img_dir = self.output_dir / 'images' / 'train'
        self.val_img_dir = self.output_dir / 'images' / 'val'
        self.test_img_dir = self.output_dir / 'images' / 'test'
        self.train_lbl_dir = self.output_dir / 'labels' / 'train'
        self.val_lbl_dir = self.output_dir / 'labels' / 'val'
        self.test_lbl_dir = self.output_dir / 'labels' / 'test'
        
        for dir_path in [self.train_img_dir, self.val_img_dir, self.test_img_dir,
                         self.train_lbl_dir, self.val_lbl_dir, self.test_lbl_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def split(self, seed=42):
        """Split dataset into train/val/test sets."""
        random.seed(seed)
        
        # Get all image files
        image_files = (list(self.images_dir.glob('*.jpg')) + 
                      list(self.images_dir.glob('*.png')) + 
                      list(self.images_dir.glob('*.tif')) + 
                      list(self.images_dir.glob('*.tiff')))
        print(f"Found {len(image_files)} images")
        
        # Filter images that have corresponding labels
        valid_pairs = []
        for img_file in image_files:
            label_file = self.labels_dir / f"{img_file.stem}.txt"
            if label_file.exists():
                valid_pairs.append((img_file, label_file))
        
        print(f"Found {len(valid_pairs)} image-label pairs")
        
        # Shuffle
        random.shuffle(valid_pairs)
        
        # Calculate split indices
        total = len(valid_pairs)
        train_end = int(self.train_ratio * total)
        val_end = train_end + int(self.val_ratio * total)
        
        # Split
        train_pairs = valid_pairs[:train_end]
        val_pairs = valid_pairs[train_end:val_end]
        test_pairs = valid_pairs[val_end:]
        
        print(f"\nSplitting dataset:")
        print(f"  Train: {len(train_pairs)} ({self.train_ratio*100:.1f}%)")
        print(f"  Val:   {len(val_pairs)} ({self.val_ratio*100:.1f}%)")
        print(f"  Test:  {len(test_pairs)} ({self.test_ratio*100:.1f}%)")
        
        # Copy files
        print("\nCopying files...")
        for pairs, img_dir, lbl_dir in [
            (train_pairs, self.train_img_dir, self.train_lbl_dir),
            (val_pairs, self.val_img_dir, self.val_lbl_dir),
            (test_pairs, self.test_img_dir, self.test_lbl_dir)
        ]:
            for img_file, label_file in pairs:
                shutil.copy2(img_file, img_dir / img_file.name)
                shutil.copy2(label_file, lbl_dir / label_file.name)
        
        print("Dataset splitting complete!")
        
        return {
            'train': len(train_pairs),
            'val': len(val_pairs),
            'test': len(test_pairs)
        }


def main():
    parser = argparse.ArgumentParser(description='Split dataset into train/val/test sets')
    parser.add_argument('--images', type=str, required=True,
                        help='Directory containing all images')
    parser.add_argument('--labels', type=str, required=True,
                        help='Directory containing all labels')
    parser.add_argument('--output', type=str, default='dataset',
                        help='Output directory for split dataset')
    parser.add_argument('--train-ratio', type=float, default=0.8,
                        help='Ratio for training set (default: 0.8)')
    parser.add_argument('--val-ratio', type=float, default=0.15,
                        help='Ratio for validation set (default: 0.15)')
    parser.add_argument('--test-ratio', type=float, default=0.05,
                        help='Ratio for test set (default: 0.05)')
    parser.add_argument('--seed', type=int, default=42,
                        help='Random seed for reproducibility')
    
    args = parser.parse_args()
    
    splitter = DatasetSplitter(
        images_dir=args.images,
        labels_dir=args.labels,
        output_dir=args.output,
        train_ratio=args.train_ratio,
        val_ratio=args.val_ratio,
        test_ratio=args.test_ratio
    )
    
    splitter.split(seed=args.seed)


if __name__ == '__main__':
    main()

