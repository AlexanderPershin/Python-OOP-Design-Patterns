from abc import ABC, abstractmethod
from typing import Any, Dict, List

from game.hero import Hero


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Сериализация для сохранения."""
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any], hero: Hero) -> "Command":
        """Десериализация при загрузке."""
        pass


class AttackCommand(Command):
    def __init__(self, hero: Hero, target: str):
        self._hero = hero
        self._target = target
        self._damage_dealt: int = 0

    def execute(self) -> None:
        print(f"⚔️ Атака по {self._target}!")
        self._damage_dealt = self._hero.attack(self._target)

    def undo(self) -> None:
        print(
            f"↩️ Отмена атаки. {self._target} восстанавливает {self._damage_dealt} HP."
        )
        # В реальности: enemy.heal(self._damage_dealt)

    def to_dict(self) -> Dict[str, Any]:
        return {"type": "attack", "target": self._target}

    @classmethod
    def from_dict(cls, data: Dict[str, Any], hero: Hero) -> "AttackCommand":
        return cls(hero, data["target"])


class DrinkPotionCommand(Command):
    def __init__(self, hero: Hero, potion_type: str = "heal"):
        self._hero = hero
        self._potion_type = potion_type
        self._hp_before: int = 0

    def execute(self) -> None:
        self._hp_before = self._hero.health
        if self._potion_type == "heal":
            self._hero.heal(30)
            print(
                f"🧪 Зелье лечения! HP: {self._hp_before} → {self._hero.health}"
            )

    def undo(self) -> None:
        self._hero.set_health(self._hp_before)
        print(f"↩️ Отмена зелья. HP возвращён к {self._hp_before}")

    def to_dict(self) -> Dict[str, Any]:
        return {"type": "potion", "potion_type": self._potion_type}

    @classmethod
    def from_dict(
        cls, data: Dict[str, Any], hero: Hero
    ) -> "DrinkPotionCommand":
        return cls(hero, data.get("potion_type", "heal"))


class CommandHistory:
    def __init__(self):
        self._history: List[Command] = []
        self._redo_stack: List[Command] = []

    def execute(self, command: Command) -> None:
        command.execute()
        self._history.append(command)
        self._redo_stack.clear()

    def undo(self) -> None:
        if not self._history:
            print("⛔ Нечего отменять!")
            return
        cmd = self._history.pop()
        cmd.undo()
        self._redo_stack.append(cmd)

    def redo(self) -> None:
        if not self._redo_stack:
            print("⛔ Нечего повторять!")
            return
        cmd = self._redo_stack.pop()
        cmd.execute()
        self._history.append(cmd)

    def get_macro(self) -> List[Dict[str, Any]]:
        return [cmd.to_dict() for cmd in self._history]

    def replay_macro(
        self, macro_data: List[Dict[str, Any]], hero: Hero
    ) -> None:
        print("\n🎬 ВОСПРОИЗВЕДЕНИЕ МАКРОСА")
        registry = {
            "attack": AttackCommand,
            "potion": DrinkPotionCommand,
        }
        for data in macro_data:
            cmd_class = registry.get(data["type"])
            if cmd_class:
                cmd = cmd_class.from_dict(data, hero)
                self.execute(cmd)
