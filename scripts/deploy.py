#!/usr/bin/env python3
"""
Model Deployment Script
Export trained YOLO models to various formats for deployment
"""

import argparse
from pathlib import Path
from ultralytics import YOLO
import torch


def export_model(
    model_path,
    formats=['onnx', 'torchscript'],
    imgsz=640,
    simplify=True,
    optimize=False
):
    """
    Export YOLO model to various formats.
    
    Args:
        model_path: Path to trained model weights
        formats: List of formats to export ('onnx', 'torchscript', 'tensorrt', 'openvino', 'coreml', 'paddle')
        imgsz: Image size for export
        simplify: Simplify ONNX model
        optimize: Optimize model
    """
    print(f"Loading model from: {model_path}")
    model = YOLO(model_path)
    
    output_dir = Path(model_path).parent.parent / 'exports'
    output_dir.mkdir(exist_ok=True)
    
    supported_formats = {
        'onnx': 'ONNX Runtime',
        'torchscript': 'TorchScript',
        'tensorrt': 'TensorRT',
        'openvino': 'OpenVINO',
        'coreml': 'CoreML',
        'paddle': 'PaddlePaddle'
    }
    
    print(f"\nExporting model to: {output_dir}")
    print(f"Image size: {imgsz}")
    print(f"Formats: {formats}")
    
    exported_files = []
    
    for fmt in formats:
        if fmt not in supported_formats:
            print(f"Warning: Unsupported format '{fmt}', skipping...")
            continue
        
        print(f"\nExporting to {supported_formats[fmt]}...")
        try:
            exported_path = model.export(
                format=fmt,
                imgsz=imgsz,
                simplify=simplify,
                optimize=optimize
            )
            exported_files.append(exported_path)
            print(f"✅ Exported to: {exported_path}")
        except Exception as e:
            print(f"❌ Error exporting to {fmt}: {e}")
    
    print("\n" + "="*60)
    print("EXPORT SUMMARY")
    print("="*60)
    print(f"Model: {model_path}")
    print(f"Output directory: {output_dir}")
    print(f"Successfully exported formats: {len(exported_files)}")
    for path in exported_files:
        print(f"  - {path}")
    print("="*60)
    
    return exported_files


def test_exported_model(exported_path, test_image=None):
    """Test exported model with a sample image."""
    print(f"\nTesting exported model: {exported_path}")
    
    try:
        model = YOLO(exported_path)
        
        if test_image:
            results = model.predict(source=test_image, verbose=False)
            print(f"✅ Model loaded and tested successfully!")
            print(f"   Detections: {len(results[0].boxes) if results[0].boxes is not None else 0}")
        else:
            print(f"✅ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Error testing model: {e}")


def main():
    parser = argparse.ArgumentParser(description='Export YOLO model for deployment')
    parser.add_argument('--model', type=str, required=True,
                        help='Path to model weights (.pt file)')
    parser.add_argument('--formats', type=str, nargs='+',
                        default=['onnx', 'torchscript'],
                        choices=['onnx', 'torchscript', 'tensorrt', 'openvino', 'coreml', 'paddle'],
                        help='Export formats')
    parser.add_argument('--imgsz', type=int, default=640,
                        help='Image size for export')
    parser.add_argument('--simplify', action='store_true',
                        help='Simplify ONNX model')
    parser.add_argument('--optimize', action='store_true',
                        help='Optimize model')
    parser.add_argument('--test', type=str, default=None,
                        help='Test exported model with image')
    
    args = parser.parse_args()
    
    if not Path(args.model).exists():
        print(f"Error: Model file not found: {args.model}")
        return
    
    exported_files = export_model(
        model_path=args.model,
        formats=args.formats,
        imgsz=args.imgsz,
        simplify=args.simplify,
        optimize=args.optimize
    )
    
    if args.test and exported_files:
        test_exported_model(exported_files[0], args.test)


if __name__ == '__main__':
    main()

