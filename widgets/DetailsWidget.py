import json
import requests
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QLabel, QFrame, QPushButton, QGridLayout, QListWidget, QListWidgetItem, QHBoxLayout,
    QDialog, QPushButton, QFileDialog, QFormLayout
)
from PyQt5.QtCore import Qt, QUrl, QSize
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath, QCursor, QFont, QIcon
from PyQt5.QtWebSockets import QWebSocket
from PyQt5.QtGui import QDesktopServices
import os
from services.DB import CaesarAIGamesCRUD
from services.Models import Settings
class CustomItemWidget(QWidget):
    def __init__(self, text, icon_path, origin_url, parent=None):
        super().__init__()
        self.parent_widget = parent
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 0, 5, 0)
        self.origin_url = origin_url

        self.label = QLabel(text)
        self.label.setStyleSheet("color: #FFFFFF; font-family: Arial, sans-serif;")
        font = QFont()
        font.setPointSize(11)
        self.label.setFont(font)

        self.icon_button = QPushButton()
        self.icon_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.icon_button.clicked.connect(self.open_website)
        self.icon_button.setIcon(QIcon(icon_path))
        self.icon_button.setFlat(True)
        self.icon_button.setFixedSize(24, 24)

        layout.addWidget(self.label)
        layout.addStretch()
        layout.addWidget(self.icon_button)

        self.setLayout(layout)

    def open_website(self):
        self.parent_widget.close_websocket()
        QDesktopServices.openUrl(QUrl(self.origin_url))

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setFixedSize(400, 200)
        self.setStyleSheet("background-color: #18181b; color: #FFFFFF;")

        layout = QFormLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Labels to display current paths
        self.install_path_label = QLabel("Not set")
        self.install_path_label.setStyleSheet("color: #FFFFFF; font-size: 14px;")
        self.saved_games_path_label = QLabel("Not set")
        self.saved_games_path_label.setStyleSheet("color: #FFFFFF; font-size: 14px;")

        # Buttons to select folders
        self.install_button = QPushButton("Select Install Folder")
        self.install_button.setStyleSheet("""
            QPushButton {
                color: #FFFFFF;
                background-color: #252528;
                border: none;
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #3a3a3c;
            }
        """)
        self.install_button.clicked.connect(self.select_install_folder)

        self.saved_games_button = QPushButton("Select Saved Games Folder")
        self.saved_games_button.setStyleSheet("""
            QPushButton {
                color: #FFFFFF;
                background-color: #252528;
                border: none;
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #3a3a3c;
            }
        """)
        self.saved_games_button.clicked.connect(self.select_saved_games_folder)

        # Add widgets to layout
        layout.addRow("Install Folder:", self.install_path_label)
        layout.addRow("", self.install_button)
        layout.addRow("Saved Games Folder:", self.saved_games_path_label)
        layout.addRow("", self.saved_games_button)

        self.setLayout(layout)

        # Load existing settings if available
        self.load_settings()

    def select_install_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Install Folder")
        if folder:
            self.install_path_label.setText(folder)
            self.save_settings()

    def select_saved_games_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Saved Games Folder")
        if folder:
            self.saved_games_path_label.setText(folder)
            self.save_settings()

    def save_settings(self):
        caesaraigmscrud  = CaesarAIGamesCRUD()
        settings = Settings.model_validate({"install_folder":self.install_path_label.text(),"saved_games_folder":self.saved_games_path_label.text()})
        caesaraigmscrud.post_data(Settings.fields_to_tuple(),settings.values_to_tuple(),Settings.SETTINGSTABLENAME)



    def load_settings(self):
        try:
            with open("settings.json", "r") as f:
                settings = json.load(f)
                self.install_path_label.setText(settings.get("install_folder", "Not set"))
                self.saved_games_path_label.setText(settings.get("saved_games_folder", "Not set"))
        except FileNotFoundError:
            pass

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
            QScrollArea { background-color: #18181b; border: none; }
            QScrollBar:vertical { background: #18181b; width: 8px; margin: 0px 0px 0px 0px; border-radius: 4px; }
            QScrollBar::handle:vertical { background: #4a4a4c; min-height: 20px; border-radius: 4px; }
            QScrollBar::handle:vertical:hover { background: #5a5a5c; }
        """)

        # Create a content widget to hold all the content
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setSpacing(1)
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
        title = item.get("name", "")
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #FFFFFF; font-size: 28px; font-weight: bold; font-family: Arial, sans-serif;")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setWordWrap(True)
        content_layout.addWidget(title_label)

        # Poster
        poster_frame = QFrame()
        poster_frame.setFixedSize(264, 352)
        poster_frame.setStyleSheet("border-radius: 10px; background-color: #252528; border: none;")
        poster_label = QLabel(poster_frame)
        poster_label.setAlignment(Qt.AlignCenter)
        poster_label.setGeometry(0, 0, 264, 352)
        poster_label.setScaledContents(True)
        poster_label.setStyleSheet("background-color: #252528; border-radius: 10px;")
        cover = self.item.get("cover", "")
        if cover:
            image_id = cover.get("image_id", "")
            if image_id in self.image_cache:
                poster_path = "/" + image_id + ".jpg"
                self.set_rounded_image(poster_label, self.image_cache[poster_path])
            else:
                poster_path = "/" + image_id + ".jpg"
                self.fetch_image_async(poster_label, poster_path)
        content_layout.addWidget(poster_frame, alignment=Qt.AlignCenter)

        # Description
        self.description_label = QLabel()
        self.description_label.setStyleSheet("color: #FFFFFF; font-size: 20px; font-family: Arial, sans-serif; width:100px;")
        self.description_label.setAlignment(Qt.AlignCenter)
        self.description_label.setWordWrap(True)
        content_layout.addWidget(self.description_label)

        # Media usage layout for Play and Backup buttons
        self.media_usage_layout = QHBoxLayout()
        self.media_usage_layout.setContentsMargins(0, 10, 0, 20)
        self.media_usage_layout.setSpacing(10)
        self.media_usage_layout.setAlignment(Qt.AlignLeft)

        # Play button
        play_button = QPushButton("Play")
        play_button.setFixedWidth(100)
        play_button.setCursor(QCursor(Qt.PointingHandCursor))
        play_button.setStyleSheet("""
            QPushButton {
                color: #FFFFFF;
                background-color: #28a745;
                border: none;
                border-radius: 6px;
                padding: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        play_button.setIcon(QIcon("imgs/play.png"))
        play_button.setIconSize(QSize(16, 16))
        play_button.clicked.connect(self.play_game)
        self.media_usage_layout.addWidget(play_button)

        # Backup button (icon-only)
        backup_button = QPushButton()
        backup_button.setFixedSize(32, 32)
        backup_button.setCursor(QCursor(Qt.PointingHandCursor))
        backup_button.setFlat(True)
        backup_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 6px;
            }
        """)
        backup_button.setIcon(QIcon("imgs/cloud_backup.png"))
        backup_button.setIconSize(QSize(24, 24))
        backup_button.clicked.connect(self.play_game)
        self.media_usage_layout.addWidget(backup_button)

        # Library button (icon-only)
        library_button = QPushButton()
        library_button.setFixedSize(32, 32)
        library_button.setCursor(QCursor(Qt.PointingHandCursor))
        library_button.setFlat(True)
        library_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 6px;
            }
        """)
        library_button.setIcon(QIcon("imgs/not_saved.png"))
        library_button.setIconSize(QSize(24, 24))
        library_button.clicked.connect(self.play_game)
        self.media_usage_layout.addWidget(library_button)

        # Add stretch to push buttons to the left
        self.media_usage_layout.addStretch()

        # Settings button (icon-only)
        settings_button = QPushButton()
        settings_button.setFixedSize(32, 32)
        settings_button.setCursor(QCursor(Qt.PointingHandCursor))
        settings_button.setFlat(True)
        settings_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 6px;
            }
        """)
        settings_button.setIcon(QIcon("imgs/settings.png"))
        settings_button.setIconSize(QSize(24, 24))
        settings_button.clicked.connect(self.show_settings_dialog)
        self.media_usage_layout.addWidget(settings_button)

        content_layout.addLayout(self.media_usage_layout)

        # Streams container
        self.streams_label = QLabel("Streaming Options")
        self.streams_label.setStyleSheet("color: #FFFFFF; font-size: 20px; font-weight: bold; font-family: Arial, sans-serif;")
        self.streams_label.setAlignment(Qt.AlignLeft)
        self.streams_label.hide()
        content_layout.addWidget(self.streams_label)

        self.streams_list = QListWidget()
        self.streams_list.setStyleSheet("""
            QListWidget { background-color: #18181b; border: none; color: #FFFFFF; font-size: 16px; font-family: Arial, sans-serif; }
            QListWidget::item { padding: 10px; border-bottom: 1px solid #252528;}
            QListWidget::item:hover { background-color: #3a3a3c; }
            QListWidget::item:selected { background-color: #4a4a4c; }
        """)
        self.streams_list.setSpacing(2)
        self.streams_list.itemClicked.connect(self.on_stream_clicked)
        content_layout.addWidget(self.streams_list, stretch=1)

        # Set the content layout to the content widget
        content_widget.setLayout(content_layout)

        # Set the content widget as the scroll area's widget
        scroll_area.setWidget(content_widget)

        # Add the scroll area to the main layout
        main_layout.addWidget(scroll_area)

        # Set the main layout for the DetailsWidget
        self.setLayout(main_layout)

        # Fetch series details
        if item.get("name"):
            self.get_film_details()

    def play_game(self):
        pass

    def show_settings_dialog(self):
        dialog = SettingsDialog(self)
        dialog.exec_()

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

    def get_film_details(self):
        try:
            self.description = self.item.get("summary", "No description available.")
            self.description_label.setText(self.description)
            self.start_streaming()
        except requests.RequestException as e:
            print(f"Error fetching details: {e}")

    def start_streaming(self):
        self.close_websocket()
        self.streams = []
        self.total_streams = 0
        self.streams_list.clear()
        self.streams_label.setText("Loading Streams...")
        self.streams_label.show()
        self.streams_list.show()

        self.websocket = QWebSocket()
        self.websocket.connected.connect(self.on_websocket_connected)
        self.websocket.disconnected.connect(self.on_websocket_disconnected)
        self.websocket.textMessageReceived.connect(self.on_websocket_message)
        self.websocket.error.connect(self.on_websocket_error)
        ws_url = f"wss://movies.caesaraihub.org/api/v1/stream_get_gamews"
        self.websocket.open(QUrl(ws_url))

    def on_websocket_connected(self):
        print("WebSocket connected")
        message = json.dumps({"title": self.item.get("name", "")})
        self.websocket.sendTextMessage(message)

    def on_websocket_disconnected(self):
        print("WebSocket disconnected")
        #self.websocket = None

    def on_websocket_message(self, message):
        try:
            data = json.loads(message)
            print(f"Received WebSocket message: {data}")
            event = data.get("event", {})
            if event.get("games"):
                games_data = event.get("games", {}).get("data", {}).get("games", [])
                self.total_streams = data.get("total", 0)
                self.streams.append(games_data)
                self.update_streams_list()
        except json.JSONDecodeError as e:
            print(f"WebSocket message parse error: {e}")
            self.streams_label.setText("Error parsing stream data")
            self.streams_list.hide()

    def on_websocket_error(self, error):
        print(f"WebSocket error: {error}")
        self.close_websocket()
        self.streams_label.setText("Failed to load streams")
        self.streams_list.hide()

    def update_streams_list(self):
        self.streams_list.clear()
        if not self.streams:
            self.streams_label.setText("No streams available")
            self.streams_list.hide()
            return

        for ind,stream in enumerate(self.streams):
            if ind > 60:
                self.websocket.close()
                break
            print("Stream:", stream)
            torrent_title = stream.get("title", "Unknown")
            seeders = stream.get("seeders", "Unknown")
            magnet_link = stream.get("magnet_link", "No Magnet")
            origin_url = stream.get("guid", "No Origin")
            display_text = f"{torrent_title} | Seeders:{seeders}"
            item = QListWidgetItem()
            item.setData(Qt.UserRole, magnet_link)

            item_widget = CustomItemWidget(display_text, "imgs/world-wide-web.png", origin_url, self)
            self.streams_list.addItem(item)
            self.streams_list.setItemWidget(item, item_widget)

        self.streams_label.setText(f"Streaming Options (Total: {self.total_streams})")
        self.streams_list.show()

    def on_stream_clicked(self, item):
        magnet_link = item.data(Qt.UserRole)
        self.get_torrenting(magnet_link)

    def close_websocket(self):
        if self.websocket:
            self.websocket.close()

    def get_torrenting(self, magnet_link):
        self.close_websocket()
        print("Streams:", magnet_link)
        print("Torrenting...")
        response = requests.post("https://movies.caesaraihub.org/api/v1/torrent_magnet", json={"torrent_link": magnet_link})
        data = response.json()
        print("Finished Torrenting.")
        _id = data["id"]
        response = requests.get("https://movies.caesaraihub.org/api/v1/get_container_links", params={"_id": _id})
        streams = response.json()
        print(streams)