# 🚀 SETUP GUIDE - YOLOv12 Satellite Detection

## Step-by-Step Instructions

### 1. 📥 Download xView Dataset

- Download xView dataset from: https://challenge.xviewdataset.org/
- Extract to: `/home/ar-in-u-359/Downloads/archive.zip`
- The dataset should contain:
  - `xView_train.geojson` (annotations)
  - `train_images/` folder (satellite images)

### 2. 🐍 Setup Python Environment

```bash
# Navigate to project
cd /home/ar-in-u-359/Desktop/YOLO

# Create virtual environment
python3 -m venv venv

# Activate environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. 📊 Prepare Dataset

```bash
# Convert xView annotations to YOLO format
python scripts/convert_xview_to_yolo.py

# Split dataset into train/val/test
python scripts/split_dataset.py

# Create data configuration file
python scripts/create_data_yaml.py
```

### 4. 🏋️ Train Model

```bash
# Start training (takes ~40 minutes)
python scripts/train.py

# Monitor progress in terminal
# Model saves to: runs/detect/xview_train/weights/best.pt
```

### 5. 🌐 Launch Dashboard

```bash
# Start web interface
streamlit run dashboard/app.py --server.port 8501

# Open browser to: http://localhost:8501
```

### 6. 🧪 Test Model

1. Upload satellite images through dashboard
2. Set confidence threshold to 0.1
3. View detections with bounding boxes
4. Check detection details table

## 🔧 Troubleshooting

### If training fails:

- Check GPU memory (need 4GB+ VRAM)
- Reduce batch size in `scripts/train.py`
- Ensure dataset is properly prepared

### If dashboard shows no detections:

- Lower confidence threshold to 0.05
- Use satellite images with vehicles
- Check model loaded successfully

### If dataset preparation fails:

- Verify xView dataset is in Downloads folder
- Check file permissions
- Ensure enough disk space (10GB+)

## 📁 Expected File Structure After Setup

```
YOLO/
├── dataset/
│   ├── images/train/     # Training images
│   ├── images/val/       # Validation images
│   ├── labels/train/     # Training labels
│   └── labels/val/       # Validation labels
├── runs/detect/xview_train/
│   └── weights/best.pt   # Trained model
├── dashboard/app.py      # Web interface
└── requirements.txt      # Dependencies
```

## ⚡ Quick Commands

```bash
# Full setup (run in order)
source venv/bin/activate
python scripts/convert_xview_to_yolo.py
python scripts/split_dataset.py
python scripts/create_data_yaml.py
python scripts/train.py
streamlit run dashboard/app.py --server.port 8501
```

## 🎯 Success Indicators

- ✅ Dataset: ~800 images with labels
- ✅ Training: mAP50 > 5%
- ✅ Dashboard: Shows detections with boxes
- ✅ Model: 5.5MB file size

## 📞 Support

If you encounter issues:

1. Check the terminal output for errors
2. Verify all files are in correct locations
3. Ensure Python environment is activated
4. Check GPU memory and disk space
