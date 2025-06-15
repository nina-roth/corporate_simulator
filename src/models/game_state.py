import json
import os
import logging
from dataclasses import dataclass

@dataclass
class ScoreClass:
    morale: int
    reputation: int
    stress: int
    salary: float

    MAX_REPUTATION = 150
    MAX_MORALE = 100
    MAX_STRESS = 100
    MIN_SALARY = 30000
    MAX_SALARY = 1000000

    def __post_init__(self):
        self._validate_and_constrain_scores()

    def _validate_and_constrain_scores(self):
        """Enforce score limits"""
        self.reputation = min(max(0, self.reputation), self.MAX_REPUTATION)
        self.morale = min(max(0, self.morale), self.MAX_MORALE)
        self.stress = min(max(0, self.stress), self.MAX_STRESS)
        self.salary = min(max(self.MIN_SALARY, self.salary), self.MAX_SALARY)

    def to_dict(self):
        return {
            "morale": self.morale,
            "reputation": self.reputation,
            "stress": self.stress,
            "salary": self.salary
        }

@dataclass
class PlayerStats:
    player_name: str
    player_id: str
    score: ScoreClass

    def to_dict(self):
        return {
            "player_name": self.player_name,
            "player_id": self.player_id,
            "score": self.score.to_dict() if self.score else None
        }

@dataclass
class StateClass:
    player_stats: PlayerStats
    game_progress: dict
    event_timer: int #something like days until next event

    def __post_init__(self):
        if not isinstance(self.game_progress, dict):
            raise TypeError("game_progress must be a dictionary")
        if not isinstance(self.event_timer, int):
            raise TypeError("event_timer must be an integer")
        
    def to_dict(self):
        return {
            "player_stats": self.player_stats.to_dict() if self.player_stats else None,
            "game_progress": self.game_progress,
            "event_timer": self.event_timer
        }

class GameState():
    _instance = None

    @classmethod
    def get_instance(cls) -> 'GameState':
        if cls._instance is None:
            raise RuntimeError("GameState not initialized. Call initialize_game_state first.")
        return cls._instance

    @classmethod
    def initialize_game_state(cls, game_id: str, state: StateClass) -> 'GameState':
        if cls._instance is None:
            cls._instance = cls(game_id, state)
        return cls._instance

    def __init__(self, game_id: str, state: StateClass):
        self.game_id = game_id
        self.state = state
        save_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "data", "save_files")
        self.save_path = os.path.join(save_dir, f"{self.game_id}_{self.state.player_stats.player_id}_state.json")
        self.events = self.load_events()

    def load_events(self):
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "data", "events", "random_events.json"), 'r') as f:
            random_events = json.load(f)
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "data", "events", "fixed_events.json"), 'r') as f:
            fixed_events = json.load(f)

        print("loaded events files")
        return {
            "random_events": random_events["random_events"],
            "fixed_events": fixed_events["fixed_events"]
        }

    def setup_player(self, player_name: str, player_id: str, score: ScoreClass):
        self.state.player_stats = PlayerStats(player_name, player_id, score)

    def update_score(self, morale: int, reputation: int, stress: int, salary: float):
        if self.state.player_stats is None:
            raise ValueError("Player stats not initialized. Call setup_player first.")
        
        self.state.player_stats.score.morale += morale
        self.state.player_stats.score.reputation += reputation
        self.state.player_stats.score.stress += stress
        self.state.player_stats.score.salary += salary

         # Enforce constraints
        self.state.player_stats.score._validate_and_constrain_scores()

        # Check triggers
        self._check_score_triggers()
    
    def _check_score_triggers(self):
        """Check for score-based event triggers"""
        score = self.state.player_stats.score
        triggers = []

        # Add trigger conditions
        if score.morale <= 0:
            triggers.append("low_morale")
        if score.stress >= 30:
            triggers.append("high_stress")
        if score.reputation <= 0:
            triggers.append("no_reputation")
        if score.salary > 100_000:
            triggers.append("high_salary")
        
        # Handle triggers
        for trigger in triggers:
            self._handle_trigger(trigger)

    def _handle_trigger(self, trigger: str):
        """Handle different types of triggers"""
        
        event = self._get_event_by_id(trigger)
        if event:
            from views.main_window import MainWindow
            from PyQt5.QtWidgets import QApplication
            # Get the main window instance - you might need to modify this
            # based on how you want to handle the reference to the main window
            main_window = QApplication.activeWindow()
            if isinstance(main_window, MainWindow):
                main_window.show_event(event)
        else:
            logging.warning(f"No event found for fixed trigger: {trigger}")

    def _get_event_by_id(self, event_id: str) -> dict:
        """Retrieve an event by its ID from the loaded events"""
        for event in self.events["fixed_events"]:
            if event.get("id") == event_id:
                return event
        return None

    def apply_event_effects(self, effects: dict):
        """Apply the effects of an event choice to the player's stats"""
        if not effects:
            return
            
        self.update_score(
            morale=effects.get("morale", 0),
            reputation=effects.get("reputation", 0),
            stress=effects.get("stress", 0),
            salary=effects.get("salary", 0)
    )

    def __repr__(self):
        return f"GameState(player_id={self.state.player_stats.player_id}, game_id={self.game_id}, state={self.state})"

    def to_dict(self):
        return {
            "player_id": self.state.player_stats.player_id,
            "game_id": self.game_id,
            "state": self.state.to_dict()
        }
    
    @property
    def player_stats(self) -> dict:
        if self.state.player_stats:
            return self.state.player_stats.to_dict()
        raise ValueError("Player stats not initialized.")
    
    @property
    def score(self) -> dict:
        if self.state.player_stats and self.state.player_stats.score:
            return self.state.player_stats.score.to_dict()
        raise ValueError("Player stats or score not initialized.")
    
    def save_state(self):
        # Placeholder for save logic, e.g., saving to a database or file
        print(f"save path: {self.save_path}")
        print(f"Saving game state for player {self.state.player_stats.player_id} in game {self.game_id}")
        
        with open(self.save_path, "w") as f:
            json.dump(self.to_dict(), f, indent=4)

    def load_state(self, game_id: str, player_id: str):
        # Placeholder for load logic, e.g., loading from a database or file
        print(f"Loading game state for player {player_id} in game {game_id}")
        print(f"load path: {self.save_path}")
        try:
            with open(self.save_path, "r") as f:
                data = json.load(f)
                #self.player_id = data["player_id"]
                self.game_id = data["game_id"]
                            # Reconstruct nested objects properly
                state_data = data["state"]
                player_stats_data = state_data["player_stats"]
                score_data = player_stats_data["score"]
                
                # Create ScoreClass instance
                score = ScoreClass(
                    morale=score_data["morale"],
                    reputation=score_data["reputation"],
                    stress=score_data["stress"],
                    salary=score_data["salary"]
                )
                
                # Create PlayerStats instance
                player_stats = PlayerStats(
                    player_name=player_stats_data["player_name"],
                    player_id=player_stats_data["player_id"],
                    score=score
                )
                
                # Create StateClass instance
                self.state = StateClass(
                    player_stats=player_stats,
                    game_progress=state_data["game_progress"],
                    event_timer=state_data["event_timer"]
                )
            print(f"Loaded game state for player {self.state.player_stats.player_id} in game {self.game_id}")
        except FileNotFoundError:
            logging.error(f"Game state file not found for player {player_id} in game {game_id}.")
            return None
    
