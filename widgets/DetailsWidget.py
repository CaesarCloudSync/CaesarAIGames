import json
import requests
from widgets import SeasonWidget
from modals import StreamModal
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout,QScrollArea,
    QLabel, QFrame, QPushButton,QGridLayout,
)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath, QCursor
from PyQt5.QtWebSockets import QWebSocket
class DetailsWidget(QWidget):
    def __init__(self, item, image_cache, main_window, parent=None):
        super().__init__(parent)
        self.item = item
        self.image_cache = image_cache
        self.main_window = main_window
        self.seasons = []
        self.description = ""
        self.number_of_episodes = 0
        self.streams = []
        self.total_streams = 0
        self.websocket = None

        # Main layout for the widget
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Create a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: #18181b;
                border: none;
            }
            QScrollBar:vertical {
                background: #18181b;
                width: 8px;
                margin: 0px 0px 0px 0px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #4a4a4c;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: #5a5a5c;
            }
        """)

        # Create a content widget to hold all the content
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setAlignment(Qt.AlignTop)

        # Back button
        back_button = QPushButton("Back")
        back_button.setFixedWidth(100)
        back_button.setCursor(QCursor(Qt.PointingHandCursor))
        back_button.setStyleSheet("""
            QPushButton {
                color: #FFFFFF;
                background-color: #252528;
                border: none;
                border-radius: 6px;
                padding: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3a3a3c;
            }
        """)
        back_button.clicked.connect(self.go_back)
        content_layout.addWidget(back_button, alignment=Qt.AlignLeft)

        # Title
        title = item.get("name","")
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #FFFFFF; font-size: 28px; font-weight: bold; font-family: Arial, sans-serif;")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setWordWrap(True)
        content_layout.addWidget(title_label)

        # Poster
        poster_frame = QFrame()
        poster_frame.setFixedSize(300, 450)
        poster_frame.setStyleSheet("""
            border-radius: 10px;
            background-color: #252528;
            border: none;
        """)
        poster_label = QLabel(poster_frame)
        poster_label.setAlignment(Qt.AlignCenter)
        poster_label.setGeometry(0, 0, 300, 450)
        poster_label.setScaledContents(True)
        poster_label.setStyleSheet("background-color: #252528; border-radius: 10px;")
        cover = self.item.get("cover","")
        if cover:
            image_id = cover.get("image_id","")
            if image_id in self.image_cache:
                poster_path = "/" + image_id  +".jpg"
                self.set_rounded_image(poster_label, self.image_cache[poster_path])
            else:
                poster_path = poster_path = "/" + image_id  +".jpg"
                self.fetch_image_async(poster_label, poster_path)
        content_layout.addWidget(poster_frame, alignment=Qt.AlignCenter)

        # Description
        self.description_label = QLabel()
        self.description_label.setStyleSheet("color: #FFFFFF; font-size: 25px; font-family: Arial, sans-serif;")
        self.description_label.setAlignment(Qt.AlignCenter)
        self.description_label.setWordWrap(True)
        content_layout.addWidget(self.description_label)

        # Episode count
        self.episode_count_label = QLabel()
        self.episode_count_label.setStyleSheet("color: #FFFFFF; font-size: 16px; font-family: Arial, sans-serif;")
        self.episode_count_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(self.episode_count_label)

        # Seasons
        self.seasons_widget = QWidget()
        self.seasons_layout = QGridLayout()
        self.seasons_widget.setLayout(self.seasons_layout)
        content_layout.addWidget(self.seasons_widget, stretch=1)

        # Set the content layout to the content widget
        content_widget.setLayout(content_layout)

        # Set the content widget as the scroll area's widget
        scroll_area.setWidget(content_widget)

        # Add the scroll area to the main layout
        main_layout.addWidget(scroll_area)

        # Set the main layout for the DetailsWidget
        self.setLayout(main_layout)

        # Fetch series details if it's a series
        if item.get("media_type") == "tv" or "first_air_date" in item:
            self.get_film_details()

    def set_rounded_image(self, label, pixmap, radius=10):
        scaled_pixmap = pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        rounded = QPixmap(label.size())
        rounded.fill(Qt.transparent)
        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(0, 0, label.width(), label.height(), radius, radius)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, scaled_pixmap)
        painter.end()
        label.setPixmap(rounded)

    def fetch_image_async(self, label, poster_path):
        image_url = f"https://images.igdb.com/igdb/image/upload/t_cover_big{poster_path}"
        request = QNetworkRequest(QUrl(image_url))
        network_manager = QNetworkAccessManager(self)
        network_manager.finished.connect(lambda reply: self.on_image_fetched(reply, label, poster_path))
        network_manager.get(request)

    def on_image_fetched(self, reply, label, poster_path):
        if reply.error() == QNetworkReply.NoError:
            image_data = reply.readAll()
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            self.image_cache[poster_path] = pixmap
            self.set_rounded_image(label, pixmap)
        else:
            print(f"Failed to load image: {reply.errorString()}")
        reply.deleteLater()

    def go_back(self):
        self.close_websocket()
        self.main_window.content_stack.setCurrentIndex(self.main_window.previous_index)
        self.main_window.button_container.show()
        self.main_window.content_nav.show()
        self.main_window.search_container.show()

    def reorder_specials(self, seasons):
        specials = [s for s in seasons if "Special" in s.get("name", "")]
        seasons = [s for s in seasons if "Special" not in s.get("name", "")]
        return seasons + specials

    def get_film_details(self):
        try:
            response = requests.get(
                f"https://api.themoviedb.org/3/tv/{self.item.get('id')}?language=en-US"
            )
            response.raise_for_status()
            result = response.json()
            self.number_of_episodes = result.get("number_of_episodes", 0)
            self.seasons = self.reorder_specials(result.get("seasons", []))
            self.description = result.get("overview", "No description available.")
            self.description_label.setText(self.description)
            self.episode_count_label.setText(f"Number of Episodes: {self.number_of_episodes}")
            self.update_seasons()
        except requests.RequestException as e:
            print(f"Error fetching details: {e}")

    def update_seasons(self):
        for i in range(self.seasons_layout.count()):
            self.seasons_layout.itemAt(i).widget().deleteLater()
        for index, season in enumerate(self.seasons):
            season_widget = SeasonWidget(season, self.item.get("name", "Unknown"), self.item.get("id"), self.start_streaming)
            self.seasons_layout.addWidget(season_widget, index // 2, index % 2)
        self.seasons_widget.setLayout(self.seasons_layout)

    def start_streaming(self, season_number, episode):
        self.close_websocket()
        self.streams = []
        self.total_streams = 0
        self.websocket = QWebSocket()
        self.websocket.connected.connect(self.on_websocket_connected)
        self.websocket.disconnected.connect(self.on_websocket_disconnected)
        self.websocket.textMessageReceived.connect(self.on_websocket_message)
        self.websocket.error.connect(self.on_websocket_error)
        ws_url = f"wss://movies.caesaraihub.org/api/v1/stream_get_episodews"
        self.websocket.open(QUrl(ws_url))
        self.season_number = season_number
        self.episode = episode
        self.modal = StreamModal(self.streams, self.item.get("name"), self.season_number, self.episode, self.get_streaming_link, self.total_streams, self)
        self.modal.show()
    def on_websocket_connected(self):
        print("WebSocket connected")
        self.websocket.sendTextMessage(json.dumps({"title":self.item.get('name'),"season":self.season_number,"episode":self.episode}))

    def on_websocket_disconnected(self):
        print("WebSocket disconnected")
        self.websocket = None

    def on_websocket_message(self, message):
        try:
            #print(message)
            data = json.loads(message)
            #print(data.get("event").get("episodes"))
            
            if data.get("event").get("episodes"):
                next_stream = data.get("event").get("episodes").get("data",{}).get("episodes")
                self.streams.append(next_stream)
                self.total_streams = data.get("total", 0)
                self.modal.update_streams(self.streams)
                self.modal.setWindowTitle(f"Streaming Options (Total: {self.total_streams})")
            elif data.get("type") == "close":
                self.close_websocket()
        except json.JSONDecodeError as e:
            print(f"WebSocket message parse error: {e}")

    def on_websocket_error(self, error):
        print(f"WebSocket error: {error}")
        self.close_websocket()

    def close_websocket(self):
        if self.websocket:
            self.websocket.close()
            self.websocket = None

    def get_streaming_link(self, episode, season, stream_id):
        print(stream_id)
        data = {
            "current_streams": self.streams,
            "current_episode": {
                "series_name": self.item.get("name"),
                "streamid": stream_id,
                "seriesid": self.item.get("id"),
                "poster_path": self.item.get("poster_path"),
                "episode": episode,
                "season": season,
                "numofeps": self.number_of_episodes
            }
        }
        # TODO Navigate to Media Player from Here
       # print(self.main_window.content_stack.count())
       # self.main_window.content_stack.setCurrentIndex(8)
        #Create a new DetailsWidget with the selected item
        #self.main_window.content_stack.content_stack.removeWidget(self.details_widget)
        #self.details_widget = MediaPlayer(self.main_window.instance,self.main_window.player,self)
        #self.main_window.content_stack.addWidget(self.details_widget)
        #self.main_window.content_stack.setCurrentIndex(self.content_stack.count() - 1)  # Show details

        with open("current_stream.json", "w") as f:
            json.dump(data, f)
        print(f"Stream selected: {stream_id} for S{season}E{episode}")
        self.close_websocket()
        