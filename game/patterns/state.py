from __future__ import annotations

import math
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from game.entities.mixins import HasHealth

if TYPE_CHECKING:
    from game.hero import Hero


class HeroState(ABC):
    @property
    @abstractmethod
    def state_key(self) -> str:
        """Строковый код для сохранения и статистики."""

    @abstractmethod
    def take_damage(self, hero: Hero, amount: int) -> bool:
        """True если сущность уничтожена (HP == 0)."""

    @abstractmethod
    def perform_attack(self, hero: Hero, target_name: str) -> int:
        """Выполнить атаку в контексте состояния."""

    @abstractmethod
    def label_for_ui(self) -> str:
        """Подпись для ConsoleUI или пустая строка."""


class NormalState(HeroState):
    @property
    def state_key(self) -> str:
        return "normal"

    def take_damage(self, hero: Hero, amount: int) -> bool:
        return HasHealth.take_damage(hero, amount)

    def perform_attack(self, hero: Hero, target_name: str) -> int:
        return hero._execute_weapon_attack(target_name)

    def label_for_ui(self) -> str:
        return ""


class InvulnerableState(HeroState):
    @property
    def state_key(self) -> str:
        return "invulnerable"

    def take_damage(self, hero: Hero, amount: int) -> bool:
        print(
            f"🛡️ {hero.name}: неуязвимость — входящий урон ({amount}) не применён. "
            f"HP: {hero.health}/{hero.max_health}"
        )
        return not hero.is_alive()

    def perform_attack(self, hero: Hero, target_name: str) -> int:
        return hero._execute_weapon_attack(target_name)

    def label_for_ui(self) -> str:
        return "НЕУЯЗВИМ"


class StunnedState(HeroState):
    @property
    def state_key(self) -> str:
        return "stunned"

    def take_damage(self, hero: Hero, amount: int) -> bool:
        return HasHealth.take_damage(hero, amount)

    def perform_attack(self, hero: Hero, target_name: str) -> int:
        print(
            f"💫 [{hero.name}] оглушён — атака по {target_name} не выполнена!"
        )
        return 0

    def label_for_ui(self) -> str:
        return "ОГЛУШЁН"


class FragileState(HeroState):
    @property
    def state_key(self) -> str:
        return "fragile"

    def take_damage(self, hero: Hero, amount: int) -> bool:
        effective = math.ceil(amount * 1.1) if amount > 0 else 0
        return HasHealth.take_damage(hero, effective)

    def perform_attack(self, hero: Hero, target_name: str) -> int:
        return hero._execute_weapon_attack(target_name)

    def label_for_ui(self) -> str:
        return "ХРУПОК (+10% урона)"
