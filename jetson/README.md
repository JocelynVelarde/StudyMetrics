# Jetson Orin Developer Kit 64 GB - Docker Container Setup

This guide will walk you through the process of flashing the Jetson Orin Developer Kit using the NVIDIA SDK Manager, followed by pulling and running a Docker container that includes the Ultralytics environment. Finally, you'll install the DeepFace library inside the container.

## Prerequisites

- Jetson Orin Developer Kit 64 GB
- Host computer with Ubuntu 18.04/20.04 and NVIDIA SDK Manager installed
- USB-C cable for flashing
- Internet connection

## Flashing the Jetson Orin Developer Kit

1. **Connect the Jetson Orin to the Host Computer**:
   - Power off the Jetson Orin.
   - Connect the Jetson Orin to the host computer using a USB-C cable.
   - Put the Jetson into recovery mode by pressing and holding the "REC" button while powering on the device.

2. **Install NVIDIA SDK Manager on the Host Computer**:
   - Download and install the NVIDIA SDK Manager from the [NVIDIA website](https://developer.nvidia.com/nvidia-sdk-manager).
   - Launch the SDK Manager.

3. **Flash the Jetson Orin**:
   - In the SDK Manager, select your Jetson device and choose the appropriate JetPack version (e.g., JetPack 6.x).
   - Follow the on-screen instructions to flash the Jetson Orin. This process will take some time as the SDK Manager installs the JetPack components.

4. **Reboot the Jetson Orin**:
   - Once flashing is complete, the Jetson Orin will reboot.
   - Follow any on-screen prompts to complete the initial setup.

## Running the Docker Container

1. **Open a Terminal on the Jetson Orin**:
   - Ensure that your Jetson Orin is connected to the internet.

2. **Pull the Docker Image**:
   ```bash
   t=ultralytics/ultralytics:latest-jetson-jetpack6
   sudo docker pull $t && sudo docker run -it --ipc=host --runtime=nvidia --device=/dev/video0:/dev/video0 --privileged $t

3. **Install Necessary Packages Inside the Docker Container:**:

```bash
pip install deepface boto3 streamlit

# Install vim
apt update && apt install -y vim

# Run the app
python3 main.py

