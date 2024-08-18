#!/bin/bash

# Define the Docker image tag
t="ultralytics/ultralytics:latest-jetson-jetpack6"

# Define the directory path within the repository
repo_dir="/workspace/StudyMetrics/jetson"

# Pull the Docker image
sudo docker pull $t

# Run the Docker container with volume mounting and execute the config.sh inside the container
sudo docker run -it --ipc=host --runtime=nvidia --device=/dev/video0:/dev/video0 --privileged -v $(pwd):/workspace $t bash -c "
    # Inside Docker container: Change to the correct directory
    cd $repo_dir &&
    
    # Make config.sh executable
    chmod +x config.sh &&
    
    # Execute the script config.sh
    ./config.sh
"
