
# Intelligent Traffic Light System with ESP32 and Sound Classification

This project leverages computer vision, deep learning, and IoT communication to create an intelligent traffic light system that adapts to real-time traffic and emergency vehicle detection. Using YOLO for vehicle detection, SORT for tracking, and an ESP32 microcontroller for remote signaling, this system aims to improve traffic management and ensure a smooth passage for emergency vehicles.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Hardware Requirements](#hardware-requirements)
5. [Software Requirements](#software-requirements)
6. [Installation](#installation)
7. [Usage](#usage)
8. [File Structure](#file-structure)
9. [Troubleshooting](#troubleshooting)
10. [Contributing](#contributing)
11. [License](#license)

---

## Project Overview

This project focuses on an intelligent traffic light system that:

- Monitors traffic density using YOLO object detection.
- Communicates with an ESP32 microcontroller to control traffic lights based on vehicle count.
- Detects emergency vehicle sirens (ambulance, firetruck) using a trained deep learning model and modifies traffic light behavior accordingly.

The goal is to alleviate congestion, prioritize emergency vehicles, and optimize traffic flow.

---

## Features

- **Real-Time Vehicle Detection:** Uses YOLO for detecting cars, trucks, and buses.
- **Traffic Density Monitoring:** Counts vehicles and adjusts traffic light timing.
- **Emergency Vehicle Detection:** Identifies ambulance sounds using a neural network model and alters traffic light signals.
- **Remote Communication:** Communicates with an ESP32 microcontroller over WiFi to control LED traffic lights.

---

## Technologies Used

- **Python Libraries:**
  - OpenCV
  - cvzone
  - numpy
  - TensorFlow
  - librosa
  - sounddevice
- **Deep Learning Model:**
  - YOLOv8 for object detection
  - Custom trained model for sound classification
- **Hardware:**
  - ESP32 microcontroller
  - LEDs to simulate traffic lights
  - Microphone for sound detection

---

## Hardware Requirements

- ESP32 microcontroller
- LEDs and resistors
- Microphone for sound detection
- WiFi network for communication
- Computer with a webcam for video input

---

## Software Requirements

- Python 3.8 or higher
- Pycharm or any other IDE (optional)
- OpenCV, TensorFlow, librosa, sounddevice libraries (install with `pip`)
- Arduino IDE for ESP32 setup

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup ESP32:**
   - Use the Arduino IDE to upload the provided ESP32 code to your microcontroller.
   - Ensure the ESP32 is connected to the specified WiFi network.

4. **Configure IP and Port:**
   - Update `ESP32_IP` and `ESP32_PORT` in your Python scripts with your actual ESP32 details.

---

## Usage

1. **Run the main vehicle counting code:**
   ```bash
   python traffic_light_system.py
   ```

2. **Run the emergency vehicle detection code:**
   ```bash
   python sound_detection.py
   ```

3. **View traffic light behavior using ESP32:**
   - The ESP32 will receive commands based on detected vehicle density or emergency vehicle sounds and adjust LED states accordingly.

---

## File Structure

```
.
├── README.md
├── traffic_light_system.py   # Main script for vehicle detection and counting
├── sound_detection.py        # Script for sound classification
├── requirements.txt          # Python dependencies
├── classes.txt               # Classes used by YOLO
├── siren_sound_classifier.h5 # Trained sound classification model
├── videos/                   # Directory containing video files
├── canvas_image.png          # Canvas image for display
└── ESP32_traffic_light.ino   # ESP32 code for controlling LEDs
```

---

## Troubleshooting

- **ESP32 Connection Issues:** Ensure the correct WiFi credentials and IP address are used.
- **Model Loading Errors:** Verify the trained model file `siren_sound_classifier.h5` is in the correct directory.
- **Performance:** Ensure your hardware meets the requirements for smooth operation.

---

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request.

---

## License

This project is licensed under the [MIT License](LICENSE).

---
