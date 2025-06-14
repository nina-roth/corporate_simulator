from PyQt5.QtWidgets import QApplication
import sys
from views.main_window import MainWindow
from models.game_state import GameState, StateClass, PlayerStats, ScoreClass

if __name__ == '__main__':
    app = QApplication(sys.argv)

    player_id = "1"
    initial_score = ScoreClass(morale=100, reputation=100, stress=0, salary=50000)
    initial_state = StateClass(
        PlayerStats("Test_Player", player_id, initial_score),
        game_progress={},
        event_timer=10
    )
    GameState.initialize_game_state("Test_Game", initial_state)

    win = MainWindow()
    win.show()
    sys.exit(app.exec_())