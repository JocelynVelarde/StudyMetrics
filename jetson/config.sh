#!/bin/bash

# Clone the GitHub repository (if not already cloned)
if [ ! -d "/workspace/StudyMetrics" ]; then
    git clone https://github.com/JocelynVelarde/StudyMetrics.git /workspace/StudyMetrics
fi

# Install necessary Python packages
pip install deepface boto3 streamlit

# Install vim
apt update && apt install -y vim

python3 main.py