
# 📥 Download and Run Guide

## If you deleted your local project and want to download from GitHub

### Step 1: Clone the Repository
```bash
# Clone from GitHub
git clone https://github.com/Amansh992/YOLO.git

# Navigate to project
cd YOLO
```

### Step 2: Setup Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Linux/Mac
# OR
venv\Scripts\activate  # On Windows
```

### Step 3: Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt
```

### Step 4: Prepare Dataset

**Note:** The dataset files are NOT in the GitHub repository (too large). You need to download the xView dataset separately.

1. Download xView dataset from: https://challenge.xviewdataset.org/
2. Extract to your Downloads folder: `/home/YOUR_USERNAME/Downloads/archive.zip`
3. Extract the archive

### Step 5: Run the Pipeline

```bash
# Convert xView to YOLO format
python scripts/convert_xview_to_yolo.py

# Split dataset
python scripts/split_dataset.py

# Create data config
python scripts/create_data_yaml.py

# Train the model
python scripts/train.py --data dataset/data.yaml --batch 4

# Launch dashboard
streamlit run dashboard/app.py --server.port 8501
```

### Step 6: Access Dashboard
Open your browser and go to: **http://localhost:8501**

## 🚀 Quick Summary

```bash
# Complete setup in one go
git clone https://github.com/Amansh992/YOLO.git && \
cd YOLO && \
python3 -m venv venv && \
source venv/bin/activate && \
pip install -r requirements.txt && \
python scripts/convert_xview_to_yolo.py && \
python scripts/split_dataset.py && \
python scripts/create_data_yaml.py && \
python scripts/train.py --data dataset/data.yaml --batch 4 && \
streamlit run dashboard/app.py --server.port 8501
```

## 📝 Important Notes

- **Dataset NOT included**: You must download xView dataset separately
- **Model weights NOT included**: You need to train the model first
- **Virtual environment**: Always activate before running scripts
- **GPU required**: For training, you need a CUDA-compatible GPU

## 🔧 Troubleshooting

### "Dataset not found" error
- Download xView dataset from official website
- Place files in the correct location as shown in SETUP.md

### "Model not trained" error  
- Run the training script: `python scripts/train.py --data dataset/data.yaml --batch 4`
- Training takes ~40 minutes on GPU

### CUDA out of memory
- Reduce batch size: `--batch 2` or `--batch 1`
- Your GPU needs at least 4GB VRAM

