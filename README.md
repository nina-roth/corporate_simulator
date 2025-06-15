## Introduction
Simulate climbing the corporate ladder by completing stressful, semi-randomized tasks while managing performance stats and surviving office politics. Or just slack off and avoid getting fired.

## Create installer
pyinstaller --onefile --windowed --icon=src/resources/images/app_icon.png --add-data "src/resources;resources" src/app.py

-> Start app.exe in "dist" folder

## Setup
pip install -r requirements.txt

## Run locally
python src/app.py