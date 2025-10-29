"""
Interactive Streamlit Dashboard for YOLOv12 Satellite Object Detection
Visualize predictions, analyze model performance, and interact with results
"""

import streamlit as st
import cv2
import numpy as np
from pathlib import Path
from ultralytics import YOLO
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import yaml
import io


# Page configuration
st.set_page_config(
    page_title="YOLOv12 Satellite Detection Dashboard",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border-radius: 5px;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f5f7fa 0%, #c3cfe2 100%);
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model(model_path):
    """Load YOLO model with caching."""
    try:
        model = YOLO(model_path)
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None


def load_config(config_path):
    """Load configuration file."""
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        st.warning(f"Could not load config: {e}")
        return None


def main():
    st.markdown('<div class="main-header">🛰️ YOLOv12 Satellite Object Detection Dashboard</div>', 
                unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("Configuration")
    
    # Model selection
    model_path = st.sidebar.text_input(
        "Model Path",
        value="runs/detect/xview_train/weights/best.pt",
        help="Path to trained YOLO model weights"
    )
    
    data_yaml_path = st.sidebar.text_input(
        "Data Config (YAML)",
        value="dataset/data.yaml",
        help="Path to data.yaml configuration file"
    )
    
    conf_threshold = st.sidebar.slider(
        "Confidence Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.1,
        step=0.05,
        help="Minimum confidence for detections (try 0.1 for more detections)"
    )
    
    iou_threshold = st.sidebar.slider(
        "IoU Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.45,
        step=0.05,
        help="IoU threshold for NMS"
    )
    
    # Auto-load model on startup
    if 'model' not in st.session_state:
        if Path(model_path).exists():
            with st.sidebar:
                with st.spinner("Loading model..."):
                    model = load_model(model_path)
                    if model:
                        st.session_state['model'] = model
                        st.success("✅ Model loaded!")
    else:
        st.sidebar.success("✅ Model ready!")
    
    # Manual reload button
    if st.sidebar.button("🔄 Reload Model", type="secondary"):
        if Path(model_path).exists():
            with st.spinner("Loading model..."):
                model = load_model(model_path)
                if model:
                    st.session_state['model'] = model
                    st.sidebar.success("Model reloaded successfully!")
        else:
            st.sidebar.error("Model file not found!")
    
    # Load config
    config = None
    if Path(data_yaml_path).exists():
        config = load_config(data_yaml_path)
        if config:
            st.session_state['config'] = config
            st.session_state['class_names'] = config.get('names', [])
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📸 Image Prediction",
        "📊 Model Metrics",
        "📁 Batch Processing",
        "📈 Analysis"
    ])
    
    # Tab 1: Image Prediction
    with tab1:
        st.header("Single Image Prediction")
        
        uploaded_file = st.file_uploader(
            "Upload Satellite Image",
            type=['jpg', 'jpeg', 'png', 'tif', 'tiff'],
            help="Upload a satellite image to detect objects"
        )
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            image_np = np.array(image)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Original Image")
                st.image(image, width='stretch')
            
            if 'model' in st.session_state:
                model = st.session_state['model']
                
                with st.spinner("Detecting objects..."):
                    # Save uploaded image temporarily for prediction
                    temp_path = f"/tmp/temp_upload_{uploaded_file.name}"
                    image.save(temp_path)
                    
                    results = model.predict(
                        source=temp_path,
                        conf=conf_threshold,
                        iou=iou_threshold,
                        imgsz=640
                    )
                    
                    # Get annotated image
                    annotated_image = results[0].plot()
                    annotated_image_rgb = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
                    
                    with col2:
                        st.subheader("Predictions")
                        st.image(annotated_image_rgb, width='stretch')
                    
                    # Display detection statistics
                    if len(results) > 0 and results[0].boxes is not None and len(results[0].boxes) > 0:
                        boxes = results[0].boxes
                        detections = []
                        
                        for i in range(len(boxes)):
                            box = boxes[i]
                            cls = int(box.cls[0])
                            conf = float(box.conf[0])
                            class_name = st.session_state.get('class_names', [])[cls] if cls < len(st.session_state.get('class_names', [])) else f"Class {cls}"
                            
                            detections.append({
                                'Class': class_name,
                                'Confidence': f"{conf:.2f}",
                                'Class ID': cls
                            })
                        
                        if detections:
                            st.subheader("Detection Details")
                            df = pd.DataFrame(detections)
                            st.dataframe(df, width='stretch')
                            
                            # Plot detections
                            if 'class_names' in st.session_state:
                                fig = px.bar(
                                    df.groupby('Class').size().reset_index(name='Count'),
                                    x='Class',
                                    y='Count',
                                    title='Detections by Class',
                                    color='Count',
                                    color_continuous_scale='Viridis'
                                )
                                st.plotly_chart(fig, width='stretch')
                    else:
                        st.info("No objects detected in this image. Try lowering the confidence threshold to 0.1 or lower.")
            else:
                col2.warning("Please load a model first using the sidebar.")
    
    # Tab 2: Model Metrics
    with tab2:
        st.header("Model Performance Metrics")
        
        if 'model' in st.session_state and config:
            model = st.session_state['model']
            
            # Get validation results
            if st.button("Run Validation"):
                with st.spinner("Running validation..."):
                    try:
                        results = model.val(data=data_yaml_path)
                        
                        # Display metrics
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("mAP50", f"{results.box.map50:.4f}")
                        with col2:
                            st.metric("mAP50-95", f"{results.box.map:.4f}")
                        with col3:
                            st.metric("Precision", f"{results.box.mp:.4f}")
                        with col4:
                            st.metric("Recall", f"{results.box.mr:.4f}")
                        
                        # Per-class metrics
                        if hasattr(results.box, 'maps'):
                            st.subheader("Per-Class mAP50")
                            class_maps = results.box.maps
                            class_names = st.session_state.get('class_names', [])
                            
                            class_metrics = pd.DataFrame({
                                'Class': [class_names[i] if i < len(class_names) else f"Class {i}" 
                                         for i in range(len(class_maps))],
                                'mAP50': class_maps
                            })
                            
                            fig = px.bar(
                                class_metrics,
                                x='Class',
                                y='mAP50',
                                title='mAP50 by Class',
                                color='mAP50',
                                color_continuous_scale='RdYlGn'
                            )
                            st.plotly_chart(fig, use_container_width=True)
                    except Exception as e:
                        st.error(f"Error running validation: {e}")
        else:
            st.info("Please load a model and data config first.")
    
    # Tab 3: Batch Processing
    with tab3:
        st.header("Batch Image Processing")
        
        uploaded_file_batch = st.file_uploader(
            "Upload Image (Repeat to process multiple)",
            type=['jpg', 'jpeg', 'png', 'tif', 'tiff'],
            help="Upload a satellite image for batch processing. Upload one at a time or refresh to process again."
        )
        
        if uploaded_file_batch and 'model' in st.session_state:
            # Handle single file as batch
            uploaded_files = [uploaded_file_batch]
            model = st.session_state['model']
            
            if st.button("Process All Images"):
                progress_bar = st.progress(0)
                results_summary = []
                
                for idx, uploaded_file in enumerate(uploaded_files):
                    image = Image.open(uploaded_file)
                    image_np = np.array(image)
                    
                    results = model.predict(
                        source=image_np,
                        conf=conf_threshold,
                        iou=iou_threshold,
                        imgsz=640,
                        verbose=False
                    )
                    
                    if len(results) > 0 and results[0].boxes is not None:
                        num_detections = len(results[0].boxes)
                        results_summary.append({
                            'Image': uploaded_file.name,
                            'Detections': num_detections
                        })
                    
                    progress_bar.progress((idx + 1) / len(uploaded_files))
                
                if results_summary:
                    df_summary = pd.DataFrame(results_summary)
                    st.subheader("Processing Summary")
                    st.dataframe(df_summary, width='stretch')
                    
                    fig = px.bar(
                        df_summary,
                        x='Image',
                        y='Detections',
                        title='Detections per Image',
                        color='Detections',
                        color_continuous_scale='Blues'
                    )
                    st.plotly_chart(fig, width='stretch')
        elif uploaded_file_batch:
            st.warning("Please load a model first.")
    
    # Tab 4: Analysis
    with tab4:
        st.header("Dataset & Model Analysis")
        
        if config:
            st.subheader("Dataset Information")
            st.json(config)
            
            if 'class_names' in st.session_state:
                class_names = st.session_state['class_names']
                st.subheader(f"Classes ({len(class_names)})")
                
                # Create class distribution visualization
                class_df = pd.DataFrame({
                    'Class': class_names,
                    'Index': range(len(class_names))
                })
                st.dataframe(class_df, width='stretch')


if __name__ == '__main__':
    main()

