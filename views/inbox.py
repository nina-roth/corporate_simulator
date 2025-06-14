from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QLabel, QTextEdit, QPushButton
)
from .components.navigation_bar import create_navigation_bar
from .components.stats_bar import create_stats_bar
from models.email import EmailManager, Email, EmailStatus

emails = [
    {
        "from": "hr@megacorp.com",
        "subject": "Welcome Aboard!",
        "time": "9:03 AM",
        "body": "We're excited to have you on board.",
        "responses": ["Thanks!", "Can I have a raise already?", "Ignore"]
    },
    {
        "from": "finance@megacorp.com",
        "subject": "Your Expense Report",
        "time": "10:15 AM",
        "body": "There are discrepancies in your expense report.",
        "responses": ["I'll revise it.", "It's correct.", "Ignore"]
    },
    {
        "from": "boss@megacorp.com",
        "subject": "URGENT: TPS Report",
        "time": "10:45 AM",
        "body": "Where is your TPS report?",
        "responses": ["Sending it now.", "Already submitted.", "Ignore"]
    }
]

class InboxApp(QWidget):
    def __init__(self):
        super().__init__()

        self.email_manager = EmailManager()
        self.email_manager.on_email_changed = self.refresh_email_list

        self.setup_ui_components()
        main_layout = self.get_main_layout()
        self.setLayout(main_layout)
        self.setWindowTitle("Inbox Simulator")
        self.resize(800, 500)

    def setup_ui_components(self):
        self.list_widget = QListWidget()
        for email in emails:
            self.list_widget.addItem(f"{email['subject']} ({email['from']})")
        self.list_widget.currentRowChanged.connect(self.load_email)

        self.sender_label = QLabel("From:")
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
        return create_navigation_bar(self)
    
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
        if index < 0 or index >= len(emails): return
        email = emails[index]
        self.sender_label.setText(f"From: {email['from']}")
        self.subject_label.setText(f"Subject: {email['subject']}")
        self.time_label.setText(f"Time: {email['time']}")
        self.body_text.setText(email['body'])
        for i in reversed(range(self.response_layout.count())):
            item = self.response_layout.itemAt(i)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
        for resp in email['responses']:
            btn = QPushButton(resp)
            btn.clicked.connect(lambda _, r=resp: self.reply(index, r))
            self.response_layout.addWidget(btn)

    def reply(self, index, response):
        consequences = self.email_manager.handle_response(index, response)
        if consequences:
            # Handle the consequences (update stats, trigger events, etc)
            print(f"Response consequences: {consequences}")
        self.refresh_email_list()

    def refresh_email_list(self):
        pass

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     win = InboxApp()
#     win.show()
#     sys.exit(app.exec_())
