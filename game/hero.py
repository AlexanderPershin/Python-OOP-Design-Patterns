from typing import Any, Dict

from game.combat.strategies import WEAPON_REGISTRY, unarmed_strategy
from game.core.events import game_events
from game.core.ui import ConsoleUI
from game.entities.inventory import Inventory
from game.entities.mixins import HasHealth
from game.interfaces.contracts import Attackable, Damageable, HealthQueryable
from game.world.level_manager import LevelManager


class Hero(HasHealth, Attackable, Damageable, HealthQueryable):
    def __init__(self, name: str):
        super().__init__(health=100)
        self.name = name
        self.level = "forest"
        self.inventory = Inventory()

        self._weapon_type = "sword"
        self._attack_strategy = WEAPON_REGISTRY.get("sword", unarmed_strategy)

    @property
    def weapon_type(self) -> str:
        return self._weapon_type

    @weapon_type.setter
    def weapon_type(self, weapon_name: str):
        self._weapon_type = weapon_name
        self._attack_strategy = WEAPON_REGISTRY.get(
            weapon_name, unarmed_strategy
        )
        print(f"⚔️ Оружие изменено на: {weapon_name}")

    def attack(self, target_name: str) -> int:
        print(f"[{self.name}] атакует {target_name}!")
        damage = self._attack_strategy(self, target_name)
        print(f"Базовый урон: {damage}")
        game_events.notify("damage_dealt", damage)
        return damage

    def get_stats(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "hp": self.health,
            "max_hp": self.max_health,
            "weapon": self.weapon_type,
            "level": self.level,
        }

    def render_ui(self):
        stats = self.get_stats()
        ConsoleUI.render_hero(
            stats["name"],
            stats["hp"],
            stats["max_hp"],
            stats["weapon"],
            stats["level"],
        )

    def export_state(self) -> Dict[str, Any]:
        stats = self.get_stats()
        return {
            "name": stats["name"],
            "hp": stats["hp"],
            "max_hp": stats["max_hp"],
            "weapon_type": stats["weapon"],
            "level": stats["level"],
            "inventory": self.inventory.list_items(),
        }

    def move(self, location: str):
        self.level = location
        print(f"\n[{self.name}] переходит в локацию: {self.level}")
        LevelManager.spawn_enemies_for_level(self.level)
