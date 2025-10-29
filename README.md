# 🛰️ YOLOv12 Satellite Object Detection

A complete satellite object detection system using YOLOv12 trained on the xView dataset.

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Prepare Dataset

```bash
# Extract xView dataset to Downloads folder
# Then run data preparation
python scripts/convert_xview_to_yolo.py
python scripts/split_dataset.py
python scripts/create_data_yaml.py
```

### 3. Train Model

```bash
python scripts/train.py
```

### 4. Run Dashboard

```bash
streamlit run dashboard/app.py --server.port 8501
```

## 📁 Project Structure

```
YOLO/
├── dataset/                 # Dataset (images + labels)
├── config/                  # Configuration files
├── scripts/                 # Training and data processing scripts
├── dashboard/               # Streamlit web interface
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🎯 Features

- **YOLOv12** object detection model
- **xView dataset** support (satellite imagery)
- **Interactive dashboard** for testing
- **9 object classes**: Aircraft, Vehicles, Ships, Buildings, etc.
- **Real-time inference** with confidence scoring

## 📊 Model Performance

- **mAP50**: 8.6% (overall)
- **Large Vehicles**: 50.5% mAP50
- **Training time**: ~40 minutes (50 epochs)
- **Model size**: 5.5MB

## 🔧 Usage

1. **Upload images** through the web dashboard
2. **Adjust confidence threshold** (default: 0.1)
3. **View detections** with bounding boxes
4. **Download results** as annotated images

## 📝 Notes

- Model works best with satellite imagery containing vehicles
- Lower confidence thresholds show more detections
- Training requires GPU for best performance
- Dashboard runs on `http://localhost:8501`

## 🛠️ Requirements

- Python 3.8+
- CUDA-capable GPU (recommended)
- 8GB+ RAM
- 10GB+ disk space

## 📄 License

This project is for educational and research purposes.
