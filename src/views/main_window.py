from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QMessageBox
from .select_view import SelectViews
from .inbox import InboxApp
from .chat import ChatApp
from .other import OtherApp
from models.game_state import GameState
from .components.event_dialog import EventDialog

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
        self.inbox_view = InboxApp(main_window=self)
        self.inbox_view.setObjectName("Inbox")
        self.chat_view = ChatApp(main_window=self)
        self.chat_view.setObjectName("Chat")
        self.other_view = OtherApp(main_window=self)
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

    def save_game(self):
        try:
            game_state = GameState.get_instance()
            game_state.save_state()
            QMessageBox.information(self, "Success", "Game saved successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save game: {str(e)}")

    def load_game(self):
        try:
            game_state = GameState.get_instance()
            # For now, we'll use the current game_id and player_id
            game_state.load_state(game_state.game_id, game_state.state.player_stats.player_id)
            QMessageBox.information(self, "Success", "Game loaded successfully!")
            # Refresh the current view
            current_widget = self.stacked_widget.currentWidget()
            if hasattr(current_widget, 'refresh_ui'):
                current_widget.refresh_ui()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load game: {str(e)}")

    def show_event(self, event):
        dialog = EventDialog(self, event)
        dialog.exec_()

    #future enhancement, but still broken
    # def load_game_with_dialog(self):
    #     from PyQt5.QtWidgets import QFileDialog
    #     import os
        
    #     save_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "data", "save_files")
    #     file_path, _ = QFileDialog.getOpenFileName(
    #         parent,
    #         "Load Game",
    #         save_dir,
    #         "Save Files (*.json)"
    #     )
        
    #     if file_path:
    #         try:
    #             # Extract game_id and player_id from filename
    #             filename = os.path.basename(file_path)
    #             game_id = filename.split('_')[0]
    #             player_id = filename.split('_')[1]
                
    #             game_state = GameState.get_instance()
    #             game_state.load_state(game_id, player_id)
    #             QMessageBox.information(parent, "Success", "Game loaded successfully!")
    #             if hasattr(parent, 'refresh_ui'):
    #                 parent.refresh_ui()
    #         except Exception as e:
    #             QMessageBox.critical(parent, "Error", f"Failed to load game: {str(e)}")