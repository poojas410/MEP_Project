from keras.models import load_model
from time import sleep
from tensorflow.keras.utils import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np
import statistics

# Load Haar Cascade classifier for face detection
face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load the emotion detection model
classifier = load_model(r'C:\Users\Aditya\em 2\Emotion_Detection_CNN-main\model.h5')

# Initialize an empty list to store detected emotions
detected_emotions = []

# List of emotion labels
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

# Open the webcam
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the webcam
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = face_classifier.detectMultiScale(gray)

    for (x, y, w, h) in faces:
        # Draw a rectangle around each detected face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

        if np.sum([roi_gray]) != 0:
            # Preprocess the ROI for emotion classification
            roi = roi_gray.astype('float') / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            # Predict the emotion using the classifier
            prediction = classifier.predict(roi)[0]
            label = emotion_labels[prediction.argmax()]

            # Display the detected emotion on the frame
            label_position = (x, y)
            cv2.putText(frame, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Store the detected emotion in the list
            detected_emotions.append(label)
        else:
            cv2.putText(frame, 'No Faces', (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frame with detected faces and emotions
    cv2.imshow('Emotion Detector', frame)

    # Exit the loop if Enter key (ASCII 13) is pressed
    if cv2.waitKey(1) & 0xFF == 13:
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
print("__________________________________________________________")

try:
    # Calculate and display the mode of detected emotions
    mode_emotion = statistics.mode(detected_emotions)
    print("Mode of Detected Emotions:", mode_emotion)

    # Create a new window to display the mode value
    mode_window = np.zeros((200, 800, 3), np.uint8)
    cv2.putText(mode_window, "Resultant of Detected Emotions: " + mode_emotion, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow('Mode Emotion', mode_window)

    # Wait for Enter key (ASCII 13) to close the mode window
    while cv2.waitKey(1) & 0xFF != 13:
        pass

    cv2.destroyAllWindows()

except statistics.StatisticsError as e:
    print("No unique mode found:", e)
