import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
from googlesearch import search
from pytube import Search
import requests
import random

class ClickableListWidgetItem(QListWidgetItem):
    def __init__(self, text, url):
        super().__init__(text)
        self.url = url
        

class SuggestionsApp(QWidget):
    def __init__(self, detected_emotion):
        super().__init__()
        self.setWindowTitle("Suggestions App")
        self.detected_emotion = detected_emotion
        self.setup_ui()
        self.resize(800, 600) 

    def setup_ui(self):
        layout = QVBoxLayout()

        # Query input field
        self.query_input = QLineEdit()
        layout.addWidget(self.query_input)

        # Buttons for search
        search_buttons_layout = QHBoxLayout()
        self.blog_button = QPushButton("Search Blogs")
        self.blog_button.clicked.connect(self.search_blogs)
        search_buttons_layout.addWidget(self.blog_button)
        self.blog_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 18px; font-family: Arial; font-style: italic; border-radius: 10px;")

        self.video_button = QPushButton("Search Videos")
        self.video_button.clicked.connect(self.search_videos)
        self.video_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 18px; font-family: Arial; font-style: italic; border-radius: 10px;")
        search_buttons_layout.addWidget(self.video_button)

        self.book_button = QPushButton("Search Books")
        self.book_button.clicked.connect(self.search_books)
        self.book_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 18px; font-family: Arial; font-style: italic; border-radius: 10px;")
        search_buttons_layout.addWidget(self.book_button)

        layout.addLayout(search_buttons_layout)

        # List widgets to display search results
        self.blog_list = QListWidget()
        self.blog_list.itemClicked.connect(self.open_link)
        layout.addWidget(self.blog_list)

        self.video_list = QListWidget()
        self.video_list.itemClicked.connect(self.open_link)
        layout.addWidget(self.video_list)

        self.book_list = QListWidget()
        self.book_list.itemClicked.connect(self.open_link)
        layout.addWidget(self.book_list)

        self.setLayout(layout)

        # Set detected emotion as initial text in query input field
        if self.detected_emotion:
            self.query_input.setText(self.detected_emotion)

    def search_blogs(self):
        self.blog_list.clear()
        query = self.query_input.text()
        google_query = f"i am feeling {query} suggest me some blogs"
        for i, result in enumerate(search(google_query, 5), start=1):
            item = ClickableListWidgetItem(f"Blog {i}: {result}", result)
            item.setText(f"Blog {i}: {result}")
            self.blog_list.addItem(item)

    def search_videos(self):
        self.video_list.clear()
        query = self.query_input.text()
        youtube_query = f"i am feeling {query} suggest me some videos"
        search_results = Search(youtube_query)
        for i, result in enumerate(search_results.results[:5], start=1):
            item = ClickableListWidgetItem(f"Video {i}: {result.title} - {result.watch_url}", result.watch_url)
            item.setText(f"Video {i}: {result.title} - {result.watch_url}")
            self.video_list.addItem(item)

    def search_books(self):
        self.book_list.clear()
        query = self.query_input.text()
        books_query = f"books about {query}"
        book_results = self.get_books(books_query)
        if book_results:
            random_books = random.sample(book_results, min(5, len(book_results)))
            for i, book in enumerate(random_books, start=1):
                title = book["volumeInfo"]["title"]
                link = book["volumeInfo"]["infoLink"]
                item = ClickableListWidgetItem(f"Book {i}: {title} - {link}", link)
                item.setText(f"Book {i}: {title} - {link}")
                self.book_list.addItem(item)
        else:
            self.book_list.addItem("No books found.")

    def get_books(self, query):
        url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
        response = requests.get(url)
        data = response.json()
        if "items" in data:
            return data["items"]
        else:
            return []

    def open_link(self, item):
        url = item.url
        QDesktopServices.openUrl(QUrl(url))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    suggestions_app = SuggestionsApp("happy")  # For testing, replace "happy" with the detected emotion
    suggestions_app.show()
    sys.exit(app.exec_())
