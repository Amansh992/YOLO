@echo off
REM Setup script for YOLOv12 xView project (Windows)

echo 🛰️  YOLOv12 Satellite Detection Setup
echo ======================================

REM Check Python version
python --version

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo.
echo Installing dependencies...
pip install -r requirements.txt

REM Create necessary directories
echo.
echo Creating project directories...
if not exist dataset\images\train mkdir dataset\images\train
if not exist dataset\images\val mkdir dataset\images\val
if not exist dataset\images\test mkdir dataset\images\test
if not exist dataset\labels\train mkdir dataset\labels\train
if not exist dataset\labels\val mkdir dataset\labels\val
if not exist dataset\labels\test mkdir dataset\labels\test
if not exist runs\detect mkdir runs\detect
if not exist results mkdir results
if not exist test_images mkdir test_images

echo.
echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Download xView dataset from https://xviewdataset.org
echo 2. Run: python scripts\convert_xview_to_yolo.py --geojson ^<path^> --images ^<path^>
echo 3. Run: python scripts\split_dataset.py --images ^<path^> --labels dataset\labels
echo 4. Run: python scripts\create_data_yaml.py --train dataset\images\train --val dataset\images\val
echo 5. Run: python scripts\train.py --data dataset\data.yaml
echo.
echo To activate the virtual environment later:
echo   venv\Scripts\activate

