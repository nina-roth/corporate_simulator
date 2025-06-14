from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QWidget

def create_navigation_bar(parent):
    navigation_bar = QHBoxLayout()
    nav_buttons = [
        ("Main Menu", "Select View")
    ]
    for text, view in nav_buttons:
        btn = QPushButton(text)
        btn.clicked.connect(lambda _, v=view: parent.parent().setCurrentWidget(parent.parent().findChild(QWidget, v)))
        navigation_bar.addWidget(btn)
    navigation_bar.addStretch()
    navigation_bar.setContentsMargins(10, 10, 10, 10)
    navigation_bar.setSpacing(10)
    return navigation_bar