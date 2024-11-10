import sounddevice as sd
import numpy as np
import librosa
import tensorflow as tf
import socket

# Loading the trained model
model = tf.keras.models.load_model('siren_sound_classifier.h5')

label_decoder = {0: "Ambulance", 1: "Firetruck", 2: "Traffic"}

# ESP32
ESP32_IP = "192.168.0.106"
ESP32_PORT = 80

def record_audio(duration=10, sample_rate=22050):
    print("Recording...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()  # To wait until the recording is finished
    print("Recording complete.")
    return audio.flatten()  # Convert to 1D array


def extract_features_from_audio(audio, sample_rate=22050):
    if len(audio) < sample_rate * 10:
        audio = np.pad(audio, (0, sample_rate * 10 - len(audio)), mode='constant')

    # Extract MFCC features
    mfcc = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
    mfcc_scaled = np.mean(mfcc.T, axis=0)
    return mfcc_scaled

# Function to classify the recorded audio
def classify_audio(audio_features, model):
    audio_features = np.expand_dims(audio_features, axis=0)  # Reshape for model input
    prediction = model.predict(audio_features)
    predicted_label = np.argmax(prediction, axis=1)
    return predicted_label

# Function to send to ESP32
def send_command_to_esp32(command):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(100)
            s.connect((ESP32_IP, ESP32_PORT))
            s.sendall(f"{command}\n".encode())
            print("Command sent:", command)
    except socket.timeout:
        print("Connection timed out. ESP32 is not responding.")
    except Exception as e:
        print("An error occurred:", e)


def main():
    duration = 10
    sample_rate = 22050

    # Step 1: Record audio
    audio = record_audio(duration=duration, sample_rate=sample_rate)

    # Step 2: Extract features from the audio
    features = extract_features_from_audio(audio, sample_rate=sample_rate)

    # Step 3: Make a prediction
    predicted_label = classify_audio(features, model)

    # Step 4: Decode and display the result
    predicted_sound = label_decoder[predicted_label[0]]
    print(f"Predicted sound category: {predicted_sound}")

    # Step 5: If the "Ambulance" sound is detected, send a command to the ESP32
    send_command_to_esp32(predicted_label[0])

if __name__ == '__main__':
    main()
