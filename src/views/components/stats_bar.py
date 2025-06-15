from PyQt5.QtWidgets import QHBoxLayout, QPushButton
from models.game_state import GameState

def create_stats_bar(parent):
    stats_bar = QHBoxLayout()
    game_state = GameState.get_instance()
    player_stats = game_state.player_stats

    # Store stat buttons as attributes of parent widget
    parent.stat_buttons = {}
    
    # Create player stat buttons
    for stat, value in player_stats.items():
        if stat == "score":
            continue
        stat_button = QPushButton(f"{stat}: {value}")
        stat_button.setEnabled(False)
        parent.stat_buttons[stat] = stat_button
        stats_bar.addWidget(stat_button)

    # Create score stat buttons    
    score = game_state.score
    for score_field, score_value in score.items():
        button_text = f"{score_field}: {score_value}"
        if score_field == "salary":
            button_text = f"{score_field}: ${score_value:,.2f}"
        score_button = QPushButton(button_text)
        score_button.setEnabled(False)
        parent.stat_buttons[score_field] = score_button
        stats_bar.addWidget(score_button)
    
    stats_bar.addStretch()
    return stats_bar

def update_stats_bar(parent):
    """Update the stats bar with current game state values"""
    game_state = GameState.get_instance()
    try:
        # Update player stats
        player_stats = game_state.player_stats
        for stat, value in player_stats.items():
            if stat == "score":
                continue
            if stat in parent.stat_buttons:
                parent.stat_buttons[stat].setText(f"{stat}: {value}")
        
        # Update score stats
        score = game_state.score
        for stat, value in score.items():
            if stat in parent.stat_buttons:
                text = f"{stat}: {value}"
                if stat == "salary":
                    text = f"{stat}: ${value:,.2f}"
                parent.stat_buttons[stat].setText(text)
                
    except ValueError as e:
        print(f"Error updating stats bar: {e}")