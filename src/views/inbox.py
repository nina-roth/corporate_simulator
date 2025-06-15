from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QLabel, QTextEdit, QPushButton
)
from .components.navigation_bar import create_navigation_bar
from .components.stats_bar import create_stats_bar, update_stats_bar
from models.email import EmailManager, Email, EmailStatus
from models.game_state import GameState

class InboxApp(QWidget):
    def __init__(self, main_window=None):
        super().__init__()

        self.main_window = main_window

        self.email_manager = EmailManager()
        self.email_manager.load_emails()
        self.email_manager.on_email_changed = self.refresh_email_list

        self.setup_ui_components()
        main_layout = self.get_main_layout()
        self.setLayout(main_layout)
        self.setWindowTitle("Inbox Simulator")
        self.resize(800, 500)

    def setup_ui_components(self):
        self.list_widget = QListWidget()
        for email in self.email_manager.emails:
            self.list_widget.addItem(f"{email.subject} ({email.sender})")
        self.list_widget.currentRowChanged.connect(self.load_email)

        self.sender_label = QLabel("Sender:")
        self.subject_label = QLabel("Subject:")
        self.time_label = QLabel("Time:")
        self.body_text = QTextEdit()
        self.body_text.setReadOnly(True)
        self.response_layout = QHBoxLayout()

    def get_main_layout(self):
        main_layout = QVBoxLayout()
        navigation_bar = self.get_navigation_bar()
        content_layout = self.get_content_layout()
        stats_bar = self.get_stats_bar()
        main_layout.addLayout(navigation_bar)
        main_layout.addLayout(content_layout)
        main_layout.addLayout(stats_bar)
        return main_layout

    def get_navigation_bar(self):
        return create_navigation_bar(self, self.main_window)
    
    def get_stats_bar(self):
        return create_stats_bar(self)

    def get_content_layout(self):
        content_layout = QHBoxLayout()
        
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.list_widget)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.sender_label)
        right_layout.addWidget(self.subject_label)
        right_layout.addWidget(self.time_label)
        right_layout.addWidget(self.body_text)
        right_layout.addLayout(self.response_layout)

        content_layout.addLayout(left_layout, 2)
        content_layout.addLayout(right_layout, 3)
        return content_layout

    def load_email(self, index):
        if index < 0 or index >= len(self.email_manager.emails): 
            return
            
        email = self.email_manager.emails[index]
        self.sender_label.setText(f"Sender: {email.sender}")
        self.subject_label.setText(f"Subject: {email.subject}")
        self.time_label.setText(f"Time: {email.time}")
        self.body_text.setText(email.body)
        
        # Clear existing response buttons
        for i in reversed(range(self.response_layout.count())):
            item = self.response_layout.itemAt(i)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
        
        # Add new response buttons using response index
        for i, response_option in enumerate(email.responses):
            btn = QPushButton(response_option.text)
            btn.clicked.connect(lambda checked, idx=i: self.reply(index, idx))
            self.response_layout.addWidget(btn)

    def reply(self, email_index: int, response_index: int):
        consequences = self.email_manager.handle_response(email_index, response_index)
        if consequences:
            game_state = GameState.get_instance()
            # Update the game state with consequences
            game_state.update_score(
                morale=consequences.get("morale", 0),
                reputation=consequences.get("reputation", 0),
                stress=consequences.get("stress", 0),
                salary=consequences.get("salary", 0)
            )
        self.refresh_email_list()
        self.refresh_stats()
        print("RE", type(game_state.events["random_events"]), len(game_state.events["random_events"]))
        self.main_window.show_event(game_state.events["random_events"][0])  # Example to show an event dialog

    def refresh_email_list(self):
        self.list_widget.clear()
        for email in self.email_manager.emails:
            status_marker = {
                EmailStatus.UNREAD: "📩",
                EmailStatus.READ: "📨",
                EmailStatus.ANSWERED: "✓"
            }.get(email.status, "")
            self.list_widget.addItem(f"{status_marker} {email.subject} ({email.sender})")

    def refresh_stats(self):
        update_stats_bar(self)

    def refresh_ui(self):
        self.refresh_email_list()
        self.refresh_stats()

