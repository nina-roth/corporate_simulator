
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QLabel, QTextEdit, QPushButton
)
import sys

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
        self.setWindowTitle("Inbox Simulator")
        self.resize(800, 500)

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

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.list_widget)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.sender_label)
        right_layout.addWidget(self.subject_label)
        right_layout.addWidget(self.time_label)
        right_layout.addWidget(self.body_text)
        right_layout.addLayout(self.response_layout)

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, 2)
        main_layout.addLayout(right_layout, 3)

        self.setLayout(main_layout)

    def load_email(self, index):
        if index < 0 or index >= len(emails): return
        email = emails[index]
        self.sender_label.setText(f"From: {email['from']}")
        self.subject_label.setText(f"Subject: {email['subject']}")
        self.time_label.setText(f"Time: {email['time']}")
        self.body_text.setText(email['body'])
        for i in reversed(range(self.response_layout.count())):
            self.response_layout.itemAt(i).widget().setParent(None)
        for resp in email['responses']:
            btn = QPushButton(resp)
            btn.clicked.connect(lambda _, r=resp: self.reply(index, r))
            self.response_layout.addWidget(btn)

    def reply(self, index, response):
        print(f"Replied to {emails[index]['from']}: {response}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = InboxApp()
    win.show()
    sys.exit(app.exec_())
