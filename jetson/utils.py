
import queue
import threading
from deepface import DeepFace

def worker(input_queue, output_queue):
    while True:
        item = input_queue.get()

        if item is None:  # Stop signal
            break

        try:
            analysis = DeepFace.analyze(face_img[0], actions=['age', 'gender', 'emotion'])

            
            # You can display some of the analysis results on the frame
            age = analysis['age']
            gender = analysis['gender']
            emotion = analysis['dominant_emotion']

            # Create a string with the information
            text = f"ID: {int(obj.id[0].item())}, Age: {age}, Gender: {gender}, Emotion: {emotion}"

            text_position = (face_img[1], face_img[2] - 10)

            result = [text, text_position]

            output_queue.put(result)
            input_queue.task_done()
        
        except:
            print("no jalaaa")
            pass

        result = 2

        output_queue.put(result)
        input_queue.task_done()

def create_queues():
    input_queue = queue.Queue()
    output_queue = queue.Queue()
    return input_queue, output_queue

def start_worker_thread(input_queue, output_queue):
    thread = threading.Thread(target=worker, args=(input_queue, output_queue))
    thread.start()
    return thread
