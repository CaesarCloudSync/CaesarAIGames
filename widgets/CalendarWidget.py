from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QScrollArea,
    QLabel, QFrame, QPushButton, QStackedWidget, QLineEdit, QListWidget, QListWidgetItem,QDialog,QGridLayout,
)
from PyQt5.QtCore import Qt

class CalendarWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Calendar Widget")
        label.setStyleSheet("color: #FFFFFF; font-size: 24px;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)