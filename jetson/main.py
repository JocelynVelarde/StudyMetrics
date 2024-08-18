import cv2
import torch
from ultralytics import YOLO
from deepface import DeepFace
import pandas as pd
import threading
import queue
import time
from datetime import datetime
import logging
import streamlit as st

import boto3
import os
import streamlit as st


s3_client = boto3.client(
        's3',
        aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"],
        region_name=st.secrets["AWS_DEFAULT_REGION"],
    )

bucket_name = st.secrets["BUCKET_NAME"]

response = s3_client.list_objects_v2(Bucket=bucket_name)

video_formats = ['.mp4', '.avi', '.mov', '.mkv'] 

if 'Contents' in response:
    video_files = [f for f in response['Contents'] if any(f['Key'].lower().endswith(ext) for ext in video_formats)]
    
    if video_files:
        files = sorted(video_files, key=lambda x: x['LastModified'], reverse=True)
        most_recent_file = files[0]
        file_key = most_recent_file['Key']

        local_file_path = os.path.join('', os.path.basename(file_key))
        s3_client.download_file(bucket_name, file_key, local_file_path)
        print(f"Downloaded {file_key} to {local_file_path}")
    else:
        print("No video files found.")
else:
    print("No contents found in the S3 bucket.")


logging.getLogger("ultralytics").setLevel(logging.WARNING)




detection_event = threading.Event()
frame_to_process = None  


class EmotionLogger:
    def __init__(self):
        # Initialize the dictionary with emotions as keys and counts as values
        self.emotion_counts = {
            'angry': 0,
            'disgust': 0,
            'fear': 0,
            'happy': 0,
            'sad': 0,
            'surprise': 0,
            'neutral': 0,
            'attention':0,
            'distracted':0
        }
        # Initialize an empty DataFrame to store the logs
        self.emotion_log_df = pd.DataFrame(columns=list(self.emotion_counts.keys()) + ['timestamp'])

    def log_emotion(self, dominant_emotion):
        if dominant_emotion in self.emotion_counts:
            self.emotion_counts[dominant_emotion] += 1

    def to_dataframe(self):

        current_log = self.emotion_counts.copy()
        current_log['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

      
        self.emotion_log_df = pd.concat([self.emotion_log_df, pd.DataFrame([current_log])], ignore_index=True)
        
        # Reset the emotion counts for the next logging session
        self.reset_counts()

        return self.emotion_log_df

    def reset_counts(self):
        # Reset the emotion counts to zero
        for key in self.emotion_counts:
            self.emotion_counts[key] = 0


emotion_logger = EmotionLogger()

def deepface_detection():
    global frame_to_process
    while True:
      
        detection_event.wait()

        if frame_to_process is not None:
            try:
                print("Starting detection...")
   
                result = DeepFace.analyze(frame_to_process, actions=['age', 'gender', 'emotion'])

                detected_faces = len(result)

                non_attentive = 0

                for user in result:

                    print(user)
                    emotion_logger.log_emotion(user['dominant_emotion'])

                    left_eye = user['region']['left_eye']
                    right_eye = user['region']['right_eye']

                    if left_eye or right_eye == None:
                        emotion_logger.emotion_counts['distracted'] +=1
                    else:
                        gaze_direction = ((left_eye[0] + right_eye[0]) / 2, (left_eye[1] + right_eye[1]) / 2)
                        emotion_logger.emotion_counts['attention'] +=1
                        print("Detection completed:", gaze_direction)
                
                try:
                    df = emotion_logger.to_dataframe()
                    print(df)
                except  Exception as r:
                    print(f"Error: {r}")
                    pass

            except Exception as e:
                print(f"Error during detection: {e}")

            detection_event.clear()






def main_loop():
    global frame_to_process

    model = YOLO("yolov8n.pt")  

    cap = cv2.VideoCapture(local_file_path)

    fps = 0

    fps_detection_rate = 5

    if not cap.isOpened():
        print("Error: Could not open camera.")


        exit()

    while True:

        #Frame Counter
        fps +=1
        ret, frame = cap.read()


        if not ret:
            print("Error: Could not read frame.")
            break

        
        



        results = model.track(frame, persist=True)

        annotated_frame = results[0].plot()


        for obj in results[0].boxes:


            #Limit analysis to only humans
            if int(obj.cls[0].item()) == 0:


                x1 = int(obj.xyxy[0][0].item())
                y1 = int(obj.xyxy[0][1].item())
                x2 = int(obj.xyxy[0][2].item())
                y2 = int(obj.xyxy[0][3].item())
                
                face_img = [frame[y1:y2, x1:x2], x1, y1]

              

        if not detection_event.is_set():
            frame_to_process = frame.copy()  
            detection_event.set() 
        
        # Display the frame with detections
        cv2.imshow("Face Detection and Tracking", annotated_frame)

        # Exit loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera, stop queues, and close all windows

    cap.release()
    cv2.destroyAllWindows()


    frame_to_process = None
    detection_event.set()

    df = emotion_logger.emotion_log_df
    df.to_csv("emotion_log.csv", index=False)
    print("DataFrame saved to 'emotion_log.csv'.")

    csv_file_path = 'emotion_log.csv'  
    upload_file_key = os.path.basename(csv_file_path)

    try:
        s3_client.upload_file(csv_file_path, bucket_name, upload_file_key)
        print(f"Uploaded {csv_file_path} to s3://{bucket_name}/{upload_file_key}")
    except Exception as e:
        print(f"Error uploading file: {e}")


detection_thread = threading.Thread(target=deepface_detection, daemon=True)
detection_thread.start()

main_loop()
detection_thread.join() 

