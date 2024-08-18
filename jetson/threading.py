import cv2
import torch
from ultralytics import YOLO
from deepface import DeepFace



#from sort import Sort

# Load YOLOv8 model (assuming the model is pre-trained for face detection)
model = YOLO("yolov8n.pt")  # You might need to fine-tune or use a model trained on faces

# Initialize the SORT tracker
#tracker = Sort()

# Open the default camera
cap = cv2.VideoCapture(0)
fps = 0
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    fps +=1
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Perform face detection using YOLOv8
    results = model.track(frame, persist=True)


    annotated_frame = frame

    for obj in results[0].boxes:
        # Extract bounding box coordinates as individual values

        if int(obj.cls[0].item()) == 0:

            x1, y1, x2, y2 = obj.xyxy[0][0].item(), obj.xyxy[0][1].item(), obj.xyxy[0][2].item(), obj.xyxy[0][3].item()
            
            face_img = frame[int(y1):int(y2), int(x1):int(x2)]

            # Pass the face image to DeepFace for analysis

            if fps % 20 = 0:
                try:
                    analysis = DeepFace.analyze(face_img, actions=['age', 'gender', 'emotion'])

                    
                    # You can display some of the analysis results on the frame
                    age = analysis['age']
                    gender = analysis['gender']
                    emotion = analysis['dominant_emotion']

                    # Create a string with the information
                    text = f"ID: {int(obj.id[0].item())}, Age: {age}, Gender: {gender}, Emotion: {emotion}"

                    # Define the position to display the text (just above the bounding box)
                    text_position = (x1, y1 - 10)

                    # Put the text on the frame
                    cv2.putText(annotated_frame, text, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                except:
                    pass
            else:
                 # Create a string with the information
                    text = f"ID: {int(obj.id[0].item())}"

                    # Define the position to display the text (just above the bounding box)
                    text_position = (x1, y1 - 10)

                    # Put the text on the frame
                    cv2.putText(annotated_frame, text, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            
    
    # Display the frame with detections
    cv2.imshow("Face Detection and Tracking", annotated_frame)

    # Exit loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
