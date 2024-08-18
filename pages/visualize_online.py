
import streamlit as st
import boto3
import os

s3_client = boto3.client('s3')

bucket_name = st.secrets["BUCKET_NAME"]

response = s3_client.list_objects_v2(Bucket=bucket_name)
video_files = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].endswith(('mp4', 'mov', 'avi'))]

st.title("Visualize class recordings and analyze their metrics")

selected_video = st.selectbox("Choose a video file", video_files)

if selected_video:
    if st.button("Play Video"):
        st.info("Downloading and playing video...")
        
        local_file_path = os.path.join('/tmp', os.path.basename(selected_video))
        s3_client.download_file(bucket_name, selected_video, local_file_path)
        
        with open(local_file_path, 'rb') as video_file:
            video_bytes = video_file.read()
            st.video(video_bytes)