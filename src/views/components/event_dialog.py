from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt

class EventDialog(QDialog):
    def __init__(self, parent=None, event: dict = {}):
        super().__init__(parent)
        self.setWindowTitle(event["title"])
        self.setWindowFlags(Qt.Dialog | Qt.WindowStaysOnTopHint)
        
        layout = QVBoxLayout()
        
        # Event description
        message = QLabel(event["description"])
        message.setWordWrap(True)
        layout.addWidget(message)
        
        # Buttons
        button_layout = QHBoxLayout()
        for choice in event.get("choices", []):
            choice_button = QPushButton(choice["text"])
            choice_button.clicked.connect(lambda _, c=choice["text"]: self.handle_choice(c))
            button_layout.addWidget(choice_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def handle_choice(self, choice_text: str):
        # Handle the choice made by the player
        print(f"Player chose: {choice_text}")
        # Here you can implement the logic to update the game state based on the choice
        self.accept()