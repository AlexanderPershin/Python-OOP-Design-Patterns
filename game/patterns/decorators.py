from abc import ABC, abstractmethod
from typing import Any, Dict

from game.interfaces.contracts import Attackable


class AttackDecorator(Attackable, ABC):
    def __init__(self, wrapped: Attackable, uses_left: int = 3):
        self._wrapped = wrapped
        self._uses_left = uses_left

    @abstractmethod
    def _apply_damage_modification(self, base_damage: int) -> int:
        pass

    def is_active(self) -> bool:
        if self._uses_left is None:
            return True
        return self._uses_left > 0

    def attack(self, enemy_name: str) -> int:
        if not self.is_active():
            return self._wrapped.attack(enemy_name)
        if self._uses_left is not None:
            self._uses_left -= 1

        base_damage = self._wrapped.attack(enemy_name)
        mod_damage = self._apply_damage_modification(base_damage)

        if self._uses_left == 0:
            print(f"⏳️ Действие {self.NAME} закончилось!")

        return mod_damage

    def get_stats(self) -> Dict[str, Any]:
        return self._wrapped.get_stats()

    def render_ui(self):
        if self.is_active():
            print(f"Бафф активен: {self.NAME}")
        return self._wrapped.render_ui()

    def __getattr__(self, name):
        attr = getattr(self._wrapped, name, None)
        if callable(attr):

            def wrapper(*args, **kwargs):
                return attr(*args, **kwargs)

            return wrapper
        return attr


class FireRingDecorator(AttackDecorator):
    BONUS_DAMAGE = 5
    NAME = "Огненное кольцо"

    def _apply_damage_modification(self, base_damage: int) -> int:
        print(f"🔥 {self.NAME} добавляет {self.BONUS_DAMAGE} урона")
        return base_damage + self.BONUS_DAMAGE


class StrengthPotionDecorator(AttackDecorator):
    MULTIPLIER = 1.5
    NAME = "Зелье силы"

    def _apply_damage_modification(self, base_damage: int) -> int:
        print(f"💪 {self.NAME} умножает урон на {self.MULTIPLIER}")
        return int(base_damage * self.MULTIPLIER)


class SlowCurseDecorator(AttackDecorator):
    MULTIPLIER = 0.5
    NAME = "Проклятие замедления"

    def _apply_damage_modification(self, base_damage: int) -> int:
        print(f"💀 {self.NAME} умножает урон на {self.MULTIPLIER}")
        return int(base_damage * self.MULTIPLIER)


class PoisonWeaponDecorator(AttackDecorator):
    BONUS_DAMAGE = 3
    NAME = "Отравленное оружие"

    def _apply_damage_modification(self, base_damage: int) -> int:
        print(f"☠️ {self.NAME} добавляет {self.BONUS_DAMAGE} урона")
        return base_damage + self.BONUS_DAMAGE


class BerserkRageDecorator(AttackDecorator):
    MULTIPLIER = 2.0
    HP_COST = 5
    NAME = "Ярость берсерка"

    def _apply_damage_modification(self, base_damage: int) -> int:
        if hasattr(self._wrapped, "health") and hasattr(
            self._wrapped, "_health"
        ):
            self._wrapped._health = max(
                0, self._wrapped._health - self.HP_COST
            )
        print(f"🩸 {self.NAME} умножает урон на {self.MULTIPLIER}")
        print(f"🩸 {self.NAME} отнимает {self.HP_COST} здоровья")
        return int(base_damage * self.MULTIPLIER)
