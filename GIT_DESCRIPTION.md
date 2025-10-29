# 🛰️ YOLOv12 Satellite Object Detection

A complete machine learning pipeline for detecting objects in satellite imagery using YOLOv12, trained on the xView dataset.

## 📋 Project Description

This project implements an end-to-end satellite object detection system capable of identifying various objects in overhead imagery, including:

- Fixed-wing aircraft
- Small and large vehicles
- Trucks and passenger vehicles
- Ships and vessels
- Buildings and structures

## ✨ Features

- **YOLOv12 Model**: State-of-the-art object detection architecture
- **xView Dataset**: Trained on real-world satellite imagery data
- **Interactive Dashboard**: Streamlit-based web interface for real-time inference
- **Automated Pipeline**: Complete workflow from dataset preparation to model deployment
- **GPU Optimized**: Configured for efficient training on low-memory GPUs (4GB+)

## 🎯 Key Components

- Data preprocessing and conversion from GeoJSON to YOLO format
- Automated dataset splitting (train/val/test)
- Model training with custom hyperparameters
- Real-time inference dashboard
- Progress monitoring and evaluation tools

## 🚀 Quick Start

```bash
# Setup
source venv/bin/activate
python scripts/convert_xview_to_yolo.py
python scripts/split_dataset.py
python scripts/create_data_yaml.py

# Train
python scripts/train.py --data dataset/data.yaml --batch 4

# Deploy
streamlit run dashboard/app.py --server.port 8501
```

## 📊 Model Performance

- mAP50: 8.6% (overall)
- Large Vehicles: 50.5% mAP50
- Training Time: ~40 minutes (100 epochs)
- Model Size: 5.5MB

## 🛠️ Technology Stack

- Python 3.10
- Ultralytics YOLOv12
- PyTorch with CUDA support
- Streamlit for web interface
- GeoPandas for geospatial data handling

## 📁 Project Structure

```
YOLO/
├── dataset/              # Processed xView dataset
├── config/               # Model and class configurations
├── scripts/              # Data processing and training scripts
├── dashboard/            # Streamlit web application
├── requirements.txt      # Python dependencies
└── *.md                  # Documentation
```

## 📝 License

Educational and research purposes only.

## 👨‍💻 Author

YOLOv12 Satellite Object Detection Project

---

**Status**: Production Ready | **Last Updated**: 2025
