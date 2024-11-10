import cv2
import cvzone
import math
import numpy as np
from ultralytics import YOLO
from sort import *
import time
import socket

# Configuration for the ESP32 IP address and port
ESP32_IP = '192.168.0.106'  # Replace with your ESP32's actual IP address
ESP32_PORT = 80  # Replace with your chosen port number

# Function to send data to ESP32 over WiFi
def send_to_esp32(message):
    try:
        # Create a socket connection
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ESP32_IP, ESP32_PORT))
            s.sendall(message.encode('utf-8'))
            print(f"Sent message: {message}")
    except Exception as e:
        print(f"Failed to send message to ESP32: {e}")

# Function to check vehicle count and send corresponding code
def check_and_send_code(video_index, vehicle_count):
    if vehicle_count > 50:
        message_map = {
            0: "yes1",
            1: "yes2",
            2: "yes3",
            3: "yes4"
        }
        message = message_map.get(video_index, "")
        if message:
            send_to_esp32(message)

# Paths to videos and canvas image
video_paths = [
    r'C:\Users\danie\PycharmProjects\Intelligent_Traffic_Light_System\videos\video1.mp4',
    r'C:\Users\danie\PycharmProjects\Intelligent_Traffic_Light_System\videos\video2.mp4',
    r'C:\Users\danie\PycharmProjects\Intelligent_Traffic_Light_System\videos\video3.mp4',
    r'C:\Users\danie\PycharmProjects\Intelligent_Traffic_Light_System\videos\video4.mp4'
]
canvas_image_path = r'C:\Users\danie\PycharmProjects\Intelligent_Traffic_Light_System\videos\background.png'

# Load canvas image
canvas = cv2.imread(canvas_image_path)
canvas = cv2.resize(canvas, (1800, 1800))  # Resize canvas to desired dimensions

model = YOLO('yolov8n.pt')
classnames = []
with open('classes.txt', 'r') as f:
    classnames = f.read().splitlines()

tracker = Sort()
current_video_index = 0  # Start with the first video

# Main video processing loop
while True:
    # Open the current video
    cap = cv2.VideoCapture(video_paths[current_video_index])
    start_time = time.time()  # Reset start time for counting
    vehicle_counter = []  # List to count unique vehicles
    unique_number = 1  # Unique counting number for vehicles

    # Process each frame in the video
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Resize the frame and detect vehicles
        frame = cv2.resize(frame, (1000, 700))  # Resize video frame to fit on canvas
        results = model(frame)
        current_detections = np.empty([0, 5])

        # Detect and process vehicles in the frame
        for info in results:
            parameters = info.boxes
            for box in parameters:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                confidence = box.conf[0]
                class_detect = box.cls[0]
                class_detect = int(class_detect)
                class_detect = classnames[class_detect]
                conf = math.ceil(confidence * 100)
                cvzone.putTextRect(frame, f'{class_detect}', [x1 + 8, y1 - 12], thickness=2, scale=1)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Filter only 'car', 'truck', 'bus' with confidence over 60
                if class_detect in ['car', 'truck', 'bus'] and conf > 60:
                    detections = np.array([x1, y1, x2, y2, conf])
                    current_detections = np.vstack([current_detections, detections])

        # Track vehicles and update counts
        track_results = tracker.update(current_detections)
        for result in track_results:
            x1, y1, x2, y2, id = result
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            cx, cy = x1 + (x2 - x1) // 2, y1 + (y2 - y1) // 2

            # Only count if the vehicle hasn't been counted yet
            if id not in vehicle_counter:
                vehicle_counter.append(id)

                # Annotate the vehicle with a unique sequential number
                cvzone.putTextRect(frame, f'Count: {unique_number}', [cx - 20, cy - 10], thickness=2, scale=1)
                unique_number += 1  # Increment the unique number for the next vehicle

        # Overlay video frame onto the canvas in the center
        canvas_copy = canvas.copy()  # Make a copy to avoid overwriting
        x_offset, y_offset = 20, 20  # Position the frame in the center of the canvas
        canvas_copy[y_offset:y_offset+frame.shape[0], x_offset:x_offset+frame.shape[1]] = frame

        # Display the total count for the current frame on the canvas
        cvzone.putTextRect(canvas_copy, f'Total Vehicles = {len(vehicle_counter)}', [50, 100], thickness=4, scale=2.3, border=2)

        # Check if 100 seconds have passed
        elapsed_time = time.time() - start_time
        if elapsed_time >= 100:
            vehicle_count = len(vehicle_counter)
            print(f"Number of vehicles counted in video {current_video_index + 1}: {vehicle_count}")
            check_and_send_code(current_video_index, vehicle_count)  # Check count and send code if needed

            # Move to the next video
            current_video_index = (current_video_index + 1) % len(video_paths)
            cap.release()  # Close the current video
            break  # Exit the inner loop to open the next video

        # Show the frame with canvas
        cv2.imshow('Canvas with Video', canvas_copy)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            exit()  # Exit the program

    # Release resources and prepare for the next video
    cap.release()

cv2.destroyAllWindows()
