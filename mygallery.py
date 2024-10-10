import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLabel, QListWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class PictureGallery(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Picture Gallery")
        self.setFixedSize(800, 600)  # Set maximum size for the window

        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QHBoxLayout()
        self.central_widget.setLayout(self.layout)

        # List to hold the paths of the images
        self.image_paths = []

        # List widget to display image names
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.preview_image)
        self.layout.addWidget(self.list_widget)

        # Button to open a folder containing images
        self.open_button = QPushButton("Open Folder")
        self.open_button.clicked.connect(self.open_folder)
        self.layout.addWidget(self.open_button)

        # Label to display the preview of the selected image
        self.preview_label = QLabel()
        self.preview_label.setScaledContents(True)
        self.preview_label.setFixedSize(400, 400)  # Set fixed size for the preview label
        self.layout.addWidget(self.preview_label)

    def open_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Open Folder")
        if folder_path:
            self.image_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith((".jpg", ".jpeg", ".png"))]
            self.list_widget.addItems([os.path.basename(file) for file in self.image_paths])

    def preview_image(self, item):
        index = self.list_widget.currentRow()
        if index >= 0:
            image_path = self.image_paths[index]
            pixmap = QPixmap(image_path)
            self.preview_label.setPixmap(pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gallery = PictureGallery()
    gallery.show()
    sys.exit(app.exec_())
