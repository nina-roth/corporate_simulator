import json
import logging
from dataclasses import dataclass

@dataclass
class ScoreClass:
    morale: int
    reputation: int
    stress: int
    salary: float

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

    def setup_player(self, player_name: str, player_id: str, score: ScoreClass):
        self.state.player_stats = PlayerStats(player_name, player_id, score)

    def update_score(self, morale: int, reputation: int, stress: int, salary: float):
        if self.state.player_stats is None:
            raise ValueError("Player stats not initialized. Call setup_player first.")
        
        self.state.player_stats.score.morale += morale
        self.state.player_stats.score.reputation += reputation
        self.state.player_stats.score.stress += stress
        self.state.player_stats.score.salary += salary

    def __repr__(self):
        return f"GameState(player_id={self.player_id}, game_id={self.game_id}, state={self.state})"

    def to_dict(self):
        return {
            "player_id": self.player_id,
            "game_id": self.game_id,
            "state": self.state
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
        print(f"Saving game state for player {self.player_id} in game {self.game_id}")
        with open(f"../data/save_files/{self.game_id}_{self.player_id}_state.json", "w") as f:
            json.dump(self.to_dict(), f, indent=4)

    def load_state(self, game_id: str, player_id: str):
        # Placeholder for load logic, e.g., loading from a database or file
        try:
            with open(f"../data/save_files/{game_id}_{player_id}_state.json", "r") as f:
                data = json.load(f)
                self.player_id = data["player_id"]
                self.game_id = data["game_id"]
                self.state = StateClass(**data["state"])
            print(f"Loaded game state for player {self.player_id} in game {self.game_id}")
        except FileNotFoundError:
            logging.error(f"Game state file not found for player {player_id} in game {game_id}.")
            return None
    
