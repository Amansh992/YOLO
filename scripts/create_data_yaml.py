#!/usr/bin/env python3
"""
Data Configuration Generator
Creates data.yaml file for YOLO training
"""

import yaml
import argparse
from pathlib import Path


def create_data_yaml(output_path, train_dir, val_dir, test_dir=None, num_classes=10, class_names=None, dataset_name="xView"):
    """
    Create data.yaml configuration file for YOLO training.
    
    Args:
        output_path: Path to save data.yaml
        train_dir: Training images directory
        val_dir: Validation images directory
        test_dir: Test images directory (optional)
        num_classes: Number of classes
        class_names: List of class names
        dataset_name: Name of the dataset
    """
    if class_names is None:
        class_names = [
            'Fixed-Wing Aircraft',
            'Small Vehicle',
            'Large Vehicle',
            'Truck',
            'Passenger Vehicle',
            'Ship',
            'Building',
            'Helipad',
            'Storage Tank',
            'Shipping Container'
        ]
    
    # Convert to absolute paths
    train_dir = str(Path(train_dir).absolute())
    val_dir = str(Path(val_dir).absolute())
    
    config = {
        'path': str(Path(output_path).parent.absolute()),
        'train': train_dir,
        'val': val_dir,
        'nc': num_classes,
        'names': class_names[:num_classes]
    }
    
    if test_dir:
        config['test'] = str(Path(test_dir).absolute())
    
    with open(output_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    print(f"Created data.yaml at: {output_path}")
    print(f"\nConfiguration:")
    print(f"  Dataset: {dataset_name}")
    print(f"  Classes: {num_classes}")
    print(f"  Train: {train_dir}")
    print(f"  Val: {val_dir}")
    if test_dir:
        print(f"  Test: {test_dir}")
    print(f"  Class names: {class_names[:num_classes]}")


def main():
    parser = argparse.ArgumentParser(description='Create data.yaml for YOLO training')
    parser.add_argument('--output', type=str, default='dataset/data.yaml',
                        help='Output path for data.yaml')
    parser.add_argument('--train', type=str, required=True,
                        help='Training images directory')
    parser.add_argument('--val', type=str, required=True,
                        help='Validation images directory')
    parser.add_argument('--test', type=str, default=None,
                        help='Test images directory (optional)')
    parser.add_argument('--num-classes', type=int, default=10,
                        help='Number of classes')
    parser.add_argument('--classes-config', type=str, default='config/xview_classes.yaml',
                        help='Path to classes configuration YAML file')
    
    args = parser.parse_args()
    
    # Try to load class names from config
    class_names = None
    if Path(args.classes_config).exists():
        import yaml as yaml_lib
        with open(args.classes_config, 'r') as f:
            config = yaml_lib.safe_load(f)
            simplified = config.get('simplified_classes', {})
            class_names = [name for _, name in sorted(simplified.items())]
    
    create_data_yaml(
        output_path=args.output,
        train_dir=args.train,
        val_dir=args.val,
        test_dir=args.test,
        num_classes=args.num_classes,
        class_names=class_names
    )


if __name__ == '__main__':
    main()

