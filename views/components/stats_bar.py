from PyQt5.QtWidgets import QHBoxLayout, QPushButton
from models.game_state import GameState

def create_stats_bar(parent):
    stats_bar = QHBoxLayout()
    game_state = GameState.get_instance()
    player_stats = game_state.player_stats
    for stat, value in player_stats.items():
        if stat == "score":
            continue
        stat_button = QPushButton(f"{stat}: {value}")
        stat_button.setEnabled(False)  # Disable button to prevent interaction
        stats_bar.addWidget(stat_button)
    score = game_state.score
    for score_field, score_value in score.items():
        score_button = QPushButton(f"{score_field}: {score_value}")
        score_button.setEnabled(False)
        stats_bar.addWidget(score_button)
    stats_bar.addStretch()
    
    return stats_bar