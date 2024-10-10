import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from suggestions import SuggestionsApp
from keras.models import load_model
from tensorflow.keras.utils import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np
import pygame
import os
import random
from collections import Counter

class EmotionDetector(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Emotion Detector")
        self.setGeometry(100, 100, 1200, 600)

        # Background image
        bg_label = QLabel(self)
        bg_label.setGeometry(0, 0, 1200, 600)  # Set geometry to cover the entire window
        pixmap = QPixmap("background_image.jpg")  # Replace "background_image.jpg" with the path to your image
        bg_label.setPixmap(pixmap)

        self.start_button = QPushButton('Start Detection', self)
        self.start_button.setGeometry(100, 100, 150, 50)
        self.start_button.clicked.connect(self.start_detection)
        self.start_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 18px; font-family: Arial; font-style: italic; border-radius: 10px;")

        self.stop_button = QPushButton('Stop Detection', self)
        self.stop_button.setGeometry(300, 100, 150, 50)
        self.stop_button.clicked.connect(self.stop_detection)
        self.stop_button.setEnabled(False)
        self.stop_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 18px; font-family: Arial; font-style: italic; border-radius: 10px;")

        self.detected_emotion_label = QLabel("", self)
        self.detected_emotion_label.setGeometry(100, 200, 200, 30)
        self.detected_emotion_label.setStyleSheet("QLabel { color: red; font-weight: bold; font-size: 18px; font-family: Arial; }")

        self.video_label = QLabel(self)
        self.video_label.setGeometry(300, 250, 400, 231)

        self.play_music_button = QPushButton('Play Music', self)
        self.play_music_button.setGeometry(500, 100, 150, 50)
        self.play_music_button.clicked.connect(self.play_music)
        self.play_music_button.setEnabled(False)
        self.play_music_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 18px; font-family: Arial; font-style: italic; border-radius: 10px;")

        self.open_suggestions_button = QPushButton('Open Suggestions', self)
        self.open_suggestions_button.setGeometry(700, 100, 150, 50)
        self.open_suggestions_button.clicked.connect(self.open_suggestions_window)
        self.open_suggestions_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 18px; font-family: Arial; font-style: italic; border-radius: 10px;")

        self.mode_emotion_label = QLabel("", self)
        self.mode_emotion_label.setGeometry(300, 500, 400, 30)
        self.mode_emotion_label.setStyleSheet("QLabel { color: red; font-weight: bold; font-size: 18px; font-family: Arial; font-style: italic; }")


        self.timer = QTimer(self)
        self.timer.timeout.connect(self.detect_emotion)

        self.face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.classifier = load_model(r'model.h5')
        self.detected_emotions = []
        self.emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Calm', 'Sad', 'Shocked']
        self.myemo = None
        self.cap = cv2.VideoCapture(0)

        # Directory where the folders are located
        self.base_directory = r'C:\Users\pooja\EMOTION - PROJECT\Music-moods'

        self.your_gallery_button = QPushButton('Your Gallery', self)
        self.your_gallery_button.setGeometry(900, 100, 150, 50)
        self.your_gallery_button.clicked.connect(self.open_gallery)
        self.your_gallery_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 18px; font-family: Arial; font-style: italic; border-radius: 10px;")

    def open_gallery(self):
        os.system("python mygallery.py")

    def start_detection(self):
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.play_music_button.setEnabled(False)
        self.open_suggestions_button.setEnabled(False)
        self.timer.start(100)

    def stop_detection(self):
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.play_music_button.setEnabled(True)
        self.open_suggestions_button.setEnabled(True)
        self.timer.stop()
        self.cap.release()  # Release the video capture object

        # Show mode of detected emotions
        self.show_mode_emotion()

    def detect_emotion(self):
        _, frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB format for displaying in PyQt
        height, width, channel = frame.shape
        step = channel * width
        qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qImg))

        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        faces = self.face_classifier.detectMultiScale(gray)

        # Only process the first detected face
        if len(faces) == 1:
            (x, y, w, h) = faces[0]  # Get the coordinates of the first detected face
            roi_gray = gray[y:y + h, x:x + w]
            roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

            if np.sum([roi_gray]) != 0:
                roi = roi_gray.astype('float') / 255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)

                prediction = self.classifier.predict(roi)[0]
                label = self.emotion_labels[prediction.argmax()]

                self.detected_emotion_label.setText(label)
                self.detected_emotions.append(label)
                self.myemo = label
            else:
                self.detected_emotion_label.setText('No Faces')
        else:
            # If no face is detected or more than one face is detected, show a message
            self.detected_emotion_label.setText('Please show only one face')

    def play_music(self):
        if self.myemo is not None:
            folder_path = os.path.join(self.base_directory, self.myemo)
            music_files = [file for file in os.listdir(folder_path) if file.endswith('.mp3')]
            if not music_files:
                print(f"No music files found in {folder_path}")
                return
            random_music_file = random.choice(music_files)
            music_file_path = os.path.join(folder_path, random_music_file)

            pygame.init()
            pygame.mixer.init()
            try:
                pygame.mixer.music.load(music_file_path)
                pygame.mixer.music.play()
                # Add a delay to allow the audio to play
                pygame.time.delay(10000)  # 10000 milliseconds (10 seconds)
                pygame.mixer.music.stop()
            finally:
                pygame.quit()
        else:
            print("No emotion detected to play music for.")

    def open_suggestions_window(self):
        if self.myemo is not None:
            self.suggestions_window = SuggestionsApp(self.myemo)  # Pass detected emotion to SuggestionsApp
            self.suggestions_window.show()
        else:
            print("No emotion detected.")

    def show_mode_emotion(self):
        if self.detected_emotions:
            mode_emotion = Counter(self.detected_emotions).most_common(1)[0][0]
            self.myemo = mode_emotion  # Set myemo to the mode emotion
            self.mode_emotion_label.setText(f"Mode Emotion: {mode_emotion}")
        else:
            self.mode_emotion_label.setText("No emotions detected yet.")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EmotionDetector()
    window.show()
    sys.exit(app.exec_())
