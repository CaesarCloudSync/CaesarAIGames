from PyQt5.QtWidgets import (
    QVBoxLayout,QPushButton,
    QLabel, QListWidget, QListWidgetItem,QDialog,
)
from PyQt5.QtCore import Qt

class StreamModal(QDialog):
    def __init__(self, streams, series_name, season, episode, get_streaming_link, total_streams, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Streaming Options")
        self.setStyleSheet("background-color: #18181b; color: #FFFFFF;")
        self.streams = streams
        self.series_name = series_name
        self.season = season
        self.episode = episode
        self.get_streaming_link = get_streaming_link
        self.total_streams = total_streams

        layout = QVBoxLayout()
        self.stream_list = QListWidget()
        self.stream_list.setStyleSheet("""
            background-color: #252528; 
            color: #FFFFFF; 
            border: none;
            border-radius: 6px;
        """)
        self.update_streams(streams)
        layout.addWidget(QLabel(f"Streams for {series_name} S{season}E{episode} (Total: {total_streams})"))
        layout.addWidget(self.stream_list)

        close_button = QPushButton("Close")
        close_button.setStyleSheet("""
            QPushButton {
                color: #FFFFFF;
                background-color: #252528;
                border: none;
                border-radius: 6px;
                padding: 8px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #3a3a3c;
            }
        """)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        self.setLayout(layout)

    def update_streams(self, streams):
        self.stream_list.clear()
        for stream in streams:
            #print(stream)
            item = QListWidgetItem(f"Stream: {stream.get('title', 'Unknown')}")
            item.setData(Qt.UserRole, stream.get('id'))
            self.stream_list.addItem(item)
        self.stream_list.itemClicked.connect(self.on_stream_selected)

    def on_stream_selected(self, item):
        stream_id = item.data(Qt.UserRole)
        self.get_streaming_link(self.episode, self.season, stream_id)
        self.close()
