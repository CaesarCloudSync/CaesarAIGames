import json
from components import ItemCard
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea
)
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtGui import QPixmap

class ContentWidget(QWidget):
    def __init__(self, api_endpoint, main_window):
        super().__init__()
        self.api_endpoint = api_endpoint
        self.main_window = main_window
        self.page_num = 1
        self.items = []
        self.is_loading = False
        self.image_cache = {}
        self.network_manager = QNetworkAccessManager(self)
        self.preload_manager = QNetworkAccessManager(self)
        self.network_manager.finished.connect(self.on_items_fetched)
        self.preload_manager.finished.connect(self.on_preload_fetched)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("""
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
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        self.scroll_area.verticalScrollBar().valueChanged.connect(self.on_scroll)

        self.carousel_widget = QWidget()
        self.carousel_layout = QVBoxLayout()
        self.carousel_layout.setSpacing(15)
        self.carousel_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.carousel_layout.setContentsMargins(8, 15, 8, 15)
        self.carousel_widget.setLayout(self.carousel_layout)
        self.scroll_area.setWidget(self.carousel_widget)

        layout.addWidget(self.scroll_area, stretch=1)
        self.setLayout(layout)

        self.current_row_items = []  # Track items for the current row
        self.load_items()

    def load_items(self):
        if self.is_loading:
            return
        self.is_loading = True
        url = f"https://games.caesaraihub.org/api/v1/popular_games?offset={self.page_num * 20}&limit=20"
        print(url)
        request = QNetworkRequest(QUrl(url))
        self.network_manager.get(request)

    def on_items_fetched(self, reply):
        if reply.error() == QNetworkReply.NoError:
            data = reply.readAll()
            try:
                result = json.loads(data.data().decode())
                new_items = result.get("games", [])
                self.items.extend(new_items)
                self.page_num += 1
                self.process_items_incrementally(new_items)
                QTimer.singleShot(500, self.preload_next_page)
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON: {e}")
        else:
            print(f"Failed to load items: {reply.errorString()}")
        self.is_loading = False
        reply.deleteLater()

    def process_items_incrementally(self, new_items):
        for item in new_items:
            self.current_row_items.append(item)
            if len(self.current_row_items) >= 5:  # Process in rows of 5
                self.update_carousel(self.current_row_items)
                self.current_row_items = []  # Reset for the next row
        if self.current_row_items:  # Handle any remaining items
            self.update_carousel(self.current_row_items)
            self.current_row_items = []

    def preload_next_page(self):
        url = f"https://games.caesaraihub.org/api/v1/popular_games?offset={self.page_num * 20}&limit=20"
        request = QNetworkRequest(QUrl(url))
        self.network_manager.get(request)

    def on_preload_fetched(self, reply):
        if reply.error() == QNetworkReply.NoError:
            image_data = reply.readAll()
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            url = reply.url().toString()
            poster_path = url.split("/t_cover_big")[-1]
            self.image_cache[poster_path] = pixmap
        reply.deleteLater()

    def update_carousel(self, row_items):
        row_widget = QWidget()
        row_layout = QHBoxLayout()
        row_layout.setSpacing(8)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setAlignment(Qt.AlignLeft)

        for j, item in enumerate(row_items):
            item_card = ItemCard(item, self.image_cache)
            item_card.clicked.connect(self.main_window.show_details)
            row_layout.addWidget(item_card)
            row_layout.setStretch(j, 1)

        while row_layout.count() < 5:
            row_layout.addStretch(1)

        row_widget.setLayout(row_layout)
        self.carousel_layout.addWidget(row_widget)

        for j in range(row_layout.count()):
            widget = row_layout.itemAt(j).widget()
            if isinstance(widget, ItemCard) and not widget.image_loaded:
                QTimer.singleShot(100 * j, widget.fetch_image_async)

    def on_scroll(self):
        scroll_bar = self.scroll_area.verticalScrollBar()
        if scroll_bar.value() >= scroll_bar.maximum() - 200 and not self.is_loading:
            QTimer.singleShot(100, self.load_items)