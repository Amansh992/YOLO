#!/usr/bin/env python3
"""
Data Augmentation Utilities
Provides custom augmentation functions for satellite imagery
"""

import cv2
import numpy as np
from pathlib import Path
import argparse
from tqdm import tqdm
import random


class SatelliteAugmenter:
    """Custom augmentation class for satellite imagery."""
    
    def __init__(self):
        self.augmentations = []
    
    def add_rotation(self, max_angle=15):
        """Add rotation augmentation."""
        self.augmentations.append(('rotation', max_angle))
    
    def add_brightness(self, factor_range=(0.7, 1.3)):
        """Add brightness adjustment."""
        self.augmentations.append(('brightness', factor_range))
    
    def add_contrast(self, factor_range=(0.8, 1.2)):
        """Add contrast adjustment."""
        self.augmentations.append(('contrast', factor_range))
    
    def add_noise(self, noise_level=0.01):
        """Add Gaussian noise."""
        self.augmentations.append(('noise', noise_level))
    
    def apply(self, image, bboxes=None):
        """
        Apply augmentations to image and adjust bounding boxes.
        
        Args:
            image: Input image (numpy array)
            bboxes: List of bounding boxes in YOLO format [class, x, y, w, h]
        
        Returns:
            Augmented image and adjusted bounding boxes
        """
        aug_image = image.copy()
        aug_bboxes = bboxes.copy() if bboxes is not None else None
        
        for aug_type, params in self.augmentations:
            if aug_type == 'rotation':
                aug_image, aug_bboxes = self._rotate(aug_image, params, aug_bboxes)
            elif aug_type == 'brightness':
                aug_image = self._adjust_brightness(aug_image, params)
            elif aug_type == 'contrast':
                aug_image = self._adjust_contrast(aug_image, params)
            elif aug_type == 'noise':
                aug_image = self._add_noise(aug_image, params)
        
        return aug_image, aug_bboxes
    
    def _rotate(self, image, max_angle, bboxes=None):
        """Rotate image and adjust bounding boxes."""
        angle = random.uniform(-max_angle, max_angle)
        h, w = image.shape[:2]
        center = (w // 2, h // 2)
        
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), borderMode=cv2.BORDER_REPLICATE)
        
        # Adjust bounding boxes (simplified - for complex rotation, use a proper library)
        if bboxes is not None:
            # Note: Full rotation adjustment requires more complex math
            # This is a simplified version
            pass
        
        return rotated, bboxes
    
    def _adjust_brightness(self, image, factor_range):
        """Adjust image brightness."""
        factor = random.uniform(factor_range[0], factor_range[1])
        adjusted = cv2.convertScaleAbs(image, alpha=1, beta=int(255 * (factor - 1)))
        return adjusted
    
    def _adjust_contrast(self, image, factor_range):
        """Adjust image contrast."""
        factor = random.uniform(factor_range[0], factor_range[1])
        adjusted = cv2.convertScaleAbs(image, alpha=factor, beta=0)
        return adjusted
    
    def _add_noise(self, image, noise_level):
        """Add Gaussian noise."""
        noise = np.random.normal(0, noise_level * 255, image.shape).astype(np.uint8)
        noisy = cv2.add(image, noise)
        return noisy


def augment_dataset(images_dir, labels_dir, output_dir, num_augmentations=2):
    """
    Augment dataset by creating additional training examples.
    
    Args:
        images_dir: Directory containing original images
        labels_dir: Directory containing original labels
        output_dir: Output directory for augmented data
        num_augmentations: Number of augmented versions per image
    """
    images_dir = Path(images_dir)
    labels_dir = Path(labels_dir)
    output_dir = Path(output_dir)
    
    output_images_dir = output_dir / 'images'
    output_labels_dir = output_dir / 'labels'
    output_images_dir.mkdir(parents=True, exist_ok=True)
    output_labels_dir.mkdir(parents=True, exist_ok=True)
    
    # Create augmenter
    augmenter = SatelliteAugmenter()
    augmenter.add_brightness(factor_range=(0.8, 1.2))
    augmenter.add_contrast(factor_range=(0.9, 1.1))
    augmenter.add_noise(noise_level=0.005)
    
    image_files = list(images_dir.glob('*.jpg')) + list(images_dir.glob('*.png'))
    
    print(f"Augmenting {len(image_files)} images...")
    
    for image_file in tqdm(image_files):
        # Load image
        image = cv2.imread(str(image_file))
        if image is None:
            continue
        
        # Load labels
        label_file = labels_dir / f"{image_file.stem}.txt"
        bboxes = []
        if label_file.exists():
            with open(label_file, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 5:
                        bboxes.append([float(x) for x in parts])
        
        # Create augmented versions
        for i in range(num_augmentations):
            aug_image, aug_bboxes = augmenter.apply(image.copy(), bboxes)
            
            # Save augmented image
            aug_image_name = f"{image_file.stem}_aug{i}.jpg"
            cv2.imwrite(str(output_images_dir / aug_image_name), aug_image)
            
            # Save augmented labels
            if aug_bboxes:
                aug_label_file = output_labels_dir / f"{image_file.stem}_aug{i}.txt"
                with open(aug_label_file, 'w') as f:
                    for bbox in aug_bboxes:
                        f.write(f"{' '.join(map(str, bbox))}\n")
    
    print(f"Augmentation complete! Output saved to: {output_dir}")


def main():
    parser = argparse.ArgumentParser(description='Augment dataset')
    parser.add_argument('--images', type=str, required=True,
                        help='Directory containing images')
    parser.add_argument('--labels', type=str, required=True,
                        help='Directory containing labels')
    parser.add_argument('--output', type=str, required=True,
                        help='Output directory')
    parser.add_argument('--num-aug', type=int, default=2,
                        help='Number of augmentations per image')
    
    args = parser.parse_args()
    
    augment_dataset(
        images_dir=args.images,
        labels_dir=args.labels,
        output_dir=args.output,
        num_augmentations=args.num_aug
    )


if __name__ == '__main__':
    main()

