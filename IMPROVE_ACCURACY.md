# 🎯 How to Improve Model Accuracy

## Current Training Setup

Your current model uses **YOLOv12** with these settings:
- **Algorithm**: AdamW optimizer
- **Learning Rate**: 0.01
- **Epochs**: 100
- **Batch Size**: 4
- **Image Size**: 640×640
- **Current Accuracy**: ~8.6% mAP50

## 🚀 Ways to Improve Accuracy

### 1. **Use a Larger Model**
Smaller models are fast but less accurate. Try larger models:

```bash
# Current: YOLOv12s (small) - 8.6% mAP
# Better: YOLOv12m (medium) - ~15% mAP expected
# Best: YOLOv12l (large) - ~20% mAP expected

python scripts/train.py --data dataset/data.yaml --model m --batch 2
```

**Trade-off**: Slower training, more GPU memory needed

### 2. **Increase Training Epochs**
More epochs = better convergence:

```bash
# Train for 200-300 epochs instead of 100
python scripts/train.py --data dataset/data.yaml --epochs 200 --batch 4
```

### 3. **Larger Image Resolution**
Bigger images = more detail:

```bash
# Use 1280×1280 instead of 640×640
python scripts/train.py --data dataset/data.yaml --imgsz 1280 --batch 1
```

**Note**: Requires 4× more GPU memory

### 4. **Better Data Augmentation**
Enable stronger augmentation:

```bash
# Edit scripts/train.py and increase:
'mixup': 0.15,        # Current: 0.0
'copy_paste': 0.3,    # Current: 0.0
'mosaic': 1.0,        # Already enabled
```

### 5. **Transfer Learning from Better Pretrained Models**
YOLOv12 pretrained on COCO is good, but you could:
- Use models trained on satellite imagery
- Fine-tune from YOLOv8 or YOLOv9
- Use domain-specific pretraining

### 6. **Fix Dataset Issues**
Your dataset has corruption:
- 19 corrupt images with class 9 (not in your 0-8 range)
- This reduces your effective dataset size

**Fix**: Clean your dataset labels before training

### 7. **Curriculum Learning**
Start with large objects, then add small ones:
- Stage 1: Train on only "Large Vehicle" and "Building" classes
- Stage 2: Add other classes progressively

### 8. **Hyperparameter Tuning**

**Better learning rate schedule**:
```python
'lr0': 0.001,         # Start lower (was 0.01)
'lrf': 0.1,           # End higher (was 0.01)
'warmup_epochs': 10,  # More warmup (was 3)
```

**Better loss weights**:
```python
'box': 7.5,          # Keep
'cls': 0.5,          # Increase to 1.0 for better classification
'dfl': 1.5,          # Keep
```

## 📊 Expected Accuracy Improvements

| Change | Expected mAP50 | Training Time |
|--------|---------------|---------------|
| Current | 8.6% | ~40 min |
| Medium model (m) | ~15% | ~1.5 hours |
| Large model (l) | ~20% | ~3 hours |
| + More epochs (200) | +2-3% | 2× time |
| + Larger images (1280) | +3-5% | 4× time |
| + Better hyperparams | +1-2% | Same time |

## 🎯 Recommended Training Command for Best Accuracy

```bash
# Maximum accuracy (slow but best):
python scripts/train.py \
  --data dataset/data.yaml \
  --model l \
  --epochs 300 \
  --imgsz 1280 \
  --batch 1
```

**Expected**: ~25% mAP50
**Training Time**: ~12 hours on RTX 500

## ⚡ Quick Win - Medium Accuracy

```bash
# Good balance (recommended):
python scripts/train.py \
  --data dataset/data.yaml \
  --model m \
  --epochs 200 \
  --imgsz 640 \
  --batch 2
```

**Expected**: ~18% mAP50
**Training Time**: ~2 hours

## 🔍 Why Your Current Model is 8.6%

1. **Small model**: YOLOv12s is optimized for speed, not accuracy
2. **Limited epochs**: 100 epochs may not be enough
3. **Small images**: 640×640 loses detail for small objects
4. **Dataset issues**: 19 corrupt images hurting training
5. **Basic augmentation**: Not using mixup/copy-paste
6. **Limited GPU**: Can't use larger models/batches

## 📈 Priority Actions (Do These First!)

1. **Clean dataset** (fix class 9 errors)
2. **Use medium model** (`--model m`)
3. **More epochs** (`--epochs 200`)
4. **Enable mixup** (edit train.py)

This should get you from 8.6% to ~18% mAP50 with minimal extra effort!

