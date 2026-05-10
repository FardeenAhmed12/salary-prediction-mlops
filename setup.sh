#!/bin/bash
# Setup script
pip install -r requirements.txt
python src/data_preprocessing.py
python src/train.py