from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from .select_view import SelectViews
from .inbox import InboxApp
from .chat import ChatApp
from .other import OtherApp

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Corporate Simulator")
        self.resize(800, 500)

        # Create stacked widget to hold different views
        self.stacked_widget = QStackedWidget()
        
        # Create and add views
        self.select_view = SelectViews()
        self.select_view.setObjectName("Select View")
        self.inbox_view = InboxApp()
        self.inbox_view.setObjectName("Inbox")
        self.chat_view = ChatApp()
        self.chat_view.setObjectName("Chat")
        self.other_view = OtherApp()
        self.other_view.setObjectName("Other")
        
        self.stacked_widget.addWidget(self.select_view)
        self.stacked_widget.addWidget(self.inbox_view)
        self.stacked_widget.addWidget(self.chat_view)
        self.stacked_widget.addWidget(self.other_view)
        
        # Set central widget
        self.setCentralWidget(self.stacked_widget)
        
        # Connect signals
        self.select_view.view_selected.connect(self.switch_view)
        
    def switch_view(self, view_name):
        if view_name == "Inbox":
            self.stacked_widget.setCurrentWidget(self.inbox_view)
        elif view_name == "Chat":
            self.stacked_widget.setCurrentWidget(self.chat_view)
        elif view_name == "Other":
            self.stacked_widget.setCurrentWidget(self.other_view)
        elif view_name == "Main Menu":
            self.stacked_widget.setCurrentWidget(self.select_view)