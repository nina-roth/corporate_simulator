from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QWidget

def create_navigation_bar(parent, main_window):
    navigation_bar = QHBoxLayout()
    
    #go back to main menu button
    back_btn = QPushButton("Main Menu")
    back_btn.clicked.connect(lambda _, v="Select View": main_window.switch_view(v))
    navigation_bar.addWidget(back_btn)

    #save game
    save_btn = QPushButton("Save Game")
    save_btn.clicked.connect(main_window.save_game)
    navigation_bar.addWidget(save_btn)

    #load game
    load_btn = QPushButton("Load Game")
    load_btn.clicked.connect(main_window.load_game)
    navigation_bar.addWidget(load_btn)
    
    navigation_bar.addStretch()
    navigation_bar.setContentsMargins(10, 10, 10, 10)
    navigation_bar.setSpacing(10)
    return navigation_bar