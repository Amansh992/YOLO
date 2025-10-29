#!/usr/bin/env python3
"""
Quick training progress checker
"""

import os
import time
from pathlib import Path

def check_training_progress():
    """Check current training progress."""
    print("🔍 CHECKING TRAINING PROGRESS")
    print("=" * 40)
    
    # Check if training is running
    import subprocess
    result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
    if 'train.py' in result.stdout:
        print("✅ Training is running...")
    else:
        print("❌ Training is not running")
        return
    
    # Check for results file
    results_file = Path("runs/detect/xview_train/results.csv")
    if results_file.exists():
        with open(results_file, 'r') as f:
            lines = f.readlines()
            if len(lines) > 1:
                latest = lines[-1].strip().split(',')
                epoch = int(float(latest[0]))
                print(f"📊 Current epoch: {epoch}/50")
                print(f"📊 Progress: {epoch/50*100:.1f}%")
                
                if len(latest) > 6:
                    mAP50 = float(latest[6])
                    print(f"📊 Current mAP50: {mAP50:.3f}")
    else:
        print("⏳ Training just started, no results yet...")
    
    # Check for model weights
    weights_dir = Path("runs/detect/xview_train/weights")
    if weights_dir.exists():
        weight_files = list(weights_dir.glob("*.pt"))
        if weight_files:
            print(f"💾 Model weights: {len(weight_files)} files")
            for wf in weight_files:
                size_mb = wf.stat().st_size / (1024*1024)
                print(f"   • {wf.name}: {size_mb:.1f}MB")
        else:
            print("⏳ No weights saved yet...")
    
    print("\n💡 To stop training: Ctrl+C in the terminal running train.py")
    print("💡 Training will take about 40 minutes total")

if __name__ == "__main__":
    check_training_progress()
