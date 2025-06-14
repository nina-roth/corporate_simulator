from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QLabel, QPushButton
)
from PyQt5.QtCore import pyqtSignal

class SelectViews(QWidget):
    view_selected = pyqtSignal(str)  # Add signal

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select View")
        self.resize(400, 300)

        self.list_widget = QListWidget()
        self.list_widget.addItems(["Inbox", "Chat", "Other"])

        self.description_label = QLabel("Select a view from the list above.")

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.on_ok_clicked)

        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)
        layout.addWidget(self.description_label)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def on_ok_clicked(self):
        currItem = self.list_widget.currentItem()
        if currItem is not None:
            selected_view = currItem.text()
            self.view_selected.emit(selected_view)