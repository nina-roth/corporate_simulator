from PyQt5.QtWidgets import (
    QWidget, 
    QVBoxLayout
)
from .components.navigation_bar import create_navigation_bar

class OtherApp(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        #self.setup_ui_components()
        self.main_window = main_window
        main_layout = self.get_main_layout()
        self.setLayout(main_layout)
        self.setWindowTitle("Other Simulator")
        self.resize(800, 500)

    def get_main_layout(self):
        main_layout = QVBoxLayout()
        navigation_bar = self.get_navigation_bar()
        main_layout.addLayout(navigation_bar)
        return main_layout

    def get_navigation_bar(self):
        return create_navigation_bar(self, self.main_window) 