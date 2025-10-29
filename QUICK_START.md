# 🚀 QUICK START - YOLOv12 Satellite Detection

## ⚡ One-Command Setup

```bash
# 1. Setup environment
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 2. Prepare dataset (after downloading xView to Downloads/)
python scripts/convert_xview_to_yolo.py
python scripts/split_dataset.py
python scripts/create_data_yaml.py

# 3. Train model
python scripts/train.py --data dataset/data.yaml

# 4. Launch dashboard
streamlit run dashboard/app.py --server.port 8501
```

# Quick start

python run.py

## 📁 What You Get

- **Trained Model**: `runs/detect/xview_train/weights/best.pt`
- **Web Dashboard**: `http://localhost:8501`
- **9 Object Classes**: Aircraft, Vehicles, Ships, Buildings, etc.
- **Real-time Detection**: Upload images and see results instantly

## 🎯 Expected Performance

- **mAP50**: ~8.6% (overall)
- **Large Vehicles**: ~50% mAP50
- **Training Time**: ~40 minutes
- **Model Size**: 5.5MB

## 🔧 Troubleshooting

**No detections?** → Lower confidence threshold to 0.05
**Training fails?** → Check GPU memory (need 4GB+ VRAM)
**Dashboard won't start?** → Ensure virtual environment is activated

## 📞 Need Help?

1. Check `SETUP.md` for detailed instructions
2. Verify all files are in correct locations
3. Ensure Python environment is activated
4. Check GPU memory and disk space

---

**Ready to detect satellites! 🛰️**
