#!/usr/bin/env python3
"""
YOLOv12 Training Script with Advanced Features
Supports custom training configurations, callbacks, and monitoring
"""

import argparse
from pathlib import Path
from ultralytics import YOLO
import torch


def train_yolo(
    data_yaml,
    model_size='s',
    epochs=100,
    imgsz=640,
    batch=4,  # Reduced for low-memory GPU
    device=None,
    project='runs/detect',
    name='xview_train',
    patience=50,
    save_period=10,
    resume=False,
    pretrained=True
):
    """
    Train YOLOv12 model on xView dataset.
    
    Args:
        data_yaml: Path to data.yaml configuration file
        model_size: Model size ('n', 's', 'm', 'l', 'x')
        epochs: Number of training epochs
        imgsz: Image size for training
        batch: Batch size
        device: Device to use ('cuda', 'cpu', or None for auto)
        project: Project directory
        name: Experiment name
        patience: Early stopping patience
        save_period: Save checkpoint every N epochs
        resume: Resume training from last checkpoint
        pretrained: Use pretrained weights
    """
    # Auto-detect device
    if device is None:
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    print(f"Using device: {device}")
    if device == 'cuda':
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"CUDA Version: {torch.version.cuda}")
    
    # Load model
    model_name = f'yolo12{model_size}.pt'
    print(f"Loading model: {model_name}")
    
    if pretrained:
        model = YOLO(model_name)
    else:
        # Load from scratch
        model = YOLO('yolo12n.yaml')  # Start with nano config
    
    # Training arguments
    train_args = {
        'data': data_yaml,
        'epochs': epochs,
        'imgsz': imgsz,
        'batch': batch,
        'device': device,
        'project': project,
        'name': name,
        'patience': patience,
        'save_period': save_period,
        'plots': True,
        'val': True,
        'workers': 2,  # Reduced for low-memory GPU
        'optimizer': 'AdamW',
        'lr0': 0.01,
        'lrf': 0.01,
        'momentum': 0.937,
        'weight_decay': 0.0005,
        'warmup_epochs': 3.0,
        'warmup_momentum': 0.8,
        'box': 7.5,
        'cls': 0.5,
        'dfl': 1.5,
        'hsv_h': 0.015,
        'hsv_s': 0.7,
        'hsv_v': 0.4,
        'degrees': 0.0,
        'translate': 0.1,
        'scale': 0.5,
        'shear': 0.0,
        'perspective': 0.0,
        'flipud': 0.0,
        'fliplr': 0.5,
        'mosaic': 1.0,
        'mixup': 0.0,
        'copy_paste': 0.0,
    }
    
    if resume:
        train_args['resume'] = True
    
    print("\n" + "="*60)
    print("TRAINING CONFIGURATION")
    print("="*60)
    print(f"Model: {model_name}")
    print(f"Data: {data_yaml}")
    print(f"Epochs: {epochs}")
    print(f"Image size: {imgsz}")
    print(f"Batch size: {batch}")
    print(f"Device: {device}")
    print(f"Project: {project}/{name}")
    print("="*60 + "\n")
    
    # Start training
    results = model.train(**train_args)
    
    print("\n" + "="*60)
    print("TRAINING COMPLETE!")
    print("="*60)
    print(f"Best model saved at: {project}/{name}/weights/best.pt")
    print(f"Last model saved at: {project}/{name}/weights/last.pt")
    print("="*60)
    
    return results


def main():
    parser = argparse.ArgumentParser(description='Train YOLOv12 on xView dataset')
    parser.add_argument('--data', type=str, required=True,
                        help='Path to data.yaml')
    parser.add_argument('--model', type=str, default='s',
                        choices=['n', 's', 'm', 'l', 'x'],
                        help='Model size (default: s)')
    parser.add_argument('--epochs', type=int, default=100,
                        help='Number of epochs (default: 100)')
    parser.add_argument('--imgsz', type=int, default=640,
                        help='Image size (default: 640)')
    parser.add_argument('--batch', type=int, default=4,
                        help='Batch size (default: 4)')
    parser.add_argument('--device', type=str, default=None,
                        help='Device (cuda/cpu, default: auto)')
    parser.add_argument('--project', type=str, default='runs/detect',
                        help='Project directory')
    parser.add_argument('--name', type=str, default='xview_train',
                        help='Experiment name')
    parser.add_argument('--patience', type=int, default=50,
                        help='Early stopping patience')
    parser.add_argument('--save-period', type=int, default=10,
                        help='Save checkpoint every N epochs')
    parser.add_argument('--resume', action='store_true',
                        help='Resume training from last checkpoint')
    parser.add_argument('--from-scratch', action='store_true',
                        help='Train from scratch (no pretrained weights)')
    
    args = parser.parse_args()
    
    train_yolo(
        data_yaml=args.data,
        model_size=args.model,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        device=args.device,
        project=args.project,
        name=args.name,
        patience=args.patience,
        save_period=args.save_period,
        resume=args.resume,
        pretrained=not args.from_scratch
    )


if __name__ == '__main__':
    main()

