from game.core.events import game_events
from game.systems.observers import AchievementSystem, AudioEngine


def setup_observers():
    game_events.subscribe("damage_dealt", AchievementSystem.on_damage_dealt)
    game_events.subscribe("damage_dealt", AudioEngine.on_damage_dealt)
