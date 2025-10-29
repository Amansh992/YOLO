#!/usr/bin/env python3
"""
Simple runner script for YOLOv12 Satellite Detection
Run this after setting up the environment and dataset
"""

import os
import sys
import subprocess
from pathlib import Path

def check_environment():
    """Check if environment is properly set up."""
    print("🔍 Checking environment...")
    
    # Check if virtual environment is activated
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("❌ Virtual environment not activated!")
        print("   Run: source venv/bin/activate")
        return False
    
    # Check if required files exist
    required_files = [
        "dataset/data.yaml",
        "scripts/train.py",
        "dashboard/app.py",
        "requirements.txt"
    ]
    
    for file in required_files:
        if not Path(file).exists():
            print(f"❌ Missing file: {file}")
            return False
    
    print("✅ Environment check passed!")
    return True

def check_dataset():
    """Check if dataset is prepared."""
    print("🔍 Checking dataset...")
    
    train_images = len(list(Path("dataset/images/train").glob("*.tif")))
    val_images = len(list(Path("dataset/images/val").glob("*.tif")))
    
    if train_images == 0 or val_images == 0:
        print("❌ Dataset not prepared!")
        print("   Run the setup steps in SETUP.md")
        return False
    
    print(f"✅ Dataset ready: {train_images} train, {val_images} val images")
    return True

def check_model():
    """Check if model is trained."""
    print("🔍 Checking model...")
    
    model_path = Path("runs/detect/xview_train/weights/best.pt")
    if not model_path.exists():
        print("❌ Model not trained!")
        print("   Run: python scripts/train.py")
        return False
    
    print("✅ Model ready!")
    return True

def main():
    """Main runner function."""
    print("🛰️  YOLOv12 Satellite Detection Runner")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Check dataset
    if not check_dataset():
        sys.exit(1)
    
    # Check model
    if not check_model():
        print("\n🚀 Starting training...")
        print("This will take about 40 minutes...")
        subprocess.run([sys.executable, "scripts/train.py", "--data", "dataset/data.yaml"])
        
        if not check_model():
            print("❌ Training failed!")
            sys.exit(1)
    
    # Launch dashboard
    print("\n🌐 Launching dashboard...")
    print("Dashboard will open at: http://localhost:8501")
    print("Press Ctrl+C to stop")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "dashboard/app.py", 
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped!")

if __name__ == "__main__":
    main()
