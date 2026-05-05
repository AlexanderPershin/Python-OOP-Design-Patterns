from abc import ABC, abstractmethod
from typing import Dict

from game.entities.mixins import HasHealth
from game.interfaces.contracts import (
    Damageable,
    HealthQueryable,
    Spawnable,
    Triggerable,
)


class Enemy(HasHealth, Spawnable, Damageable, HealthQueryable):
    def __init__(self, name: str, health: int = 100):
        super().__init__(health=health)
        self._name = name

    @property
    def name(self) -> str:
        return self._name


class ForestOrc(Enemy):
    def __init__(self):
        super().__init__(name="Лесной Орк", health=50)

    def spawn(self) -> str:
        return f"🌲 {self.name} вылез из-за дерева! (HP: {self.health})"


class FireElemental(Enemy):
    def __init__(self):
        super().__init__(name="Огненный Элементаль", health=100)

    def spawn(self) -> str:
        return f"🔥 {self.name} восстал из лавы! (HP: {self.health})"


class IceGolem(Enemy):
    def __init__(self):
        super().__init__(name="Ледяной Голем", health=120)

    def spawn(self) -> str:
        return f"❄️ {self.name} пробудился! (HP: {self.health}, броня: 20)"


class Trap(Spawnable, Triggerable):
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def spawn(self) -> str:
        return f"💀 Ловушка '{self.name}' скрыта в тени..."


class ForestSnare(Trap):
    def __init__(self):
        super().__init__(name="Сеть")

    def trigger(self) -> str:
        return "🕸️ Ловушка-сеть! Герой опутан ветвями."


class LavaPit(Trap):
    def __init__(self):
        super().__init__(name="Лавовая яма")

    def trigger(self) -> str:
        return "🌋 Лавовая яма! Ноги обжигает."


class IceSpike(Trap):
    def __init__(self):
        super().__init__(name="Ледяной шип")

    def trigger(self) -> str:
        return "🧊 Ледяной шип выстрелил из-под ног!"


class LevelFactory(ABC):
    @abstractmethod
    def create_enemy(self) -> Enemy:
        pass

    @abstractmethod
    def create_trap(self) -> Trap:
        pass


class LavaLevelFactory(LevelFactory):
    def create_enemy(self) -> Enemy:
        return FireElemental()

    def create_trap(self) -> Trap:
        return LavaPit()


class ForestLevelFactory(LevelFactory):
    def create_enemy(self) -> Enemy:
        return ForestOrc()

    def create_trap(self) -> Trap:
        return ForestSnare()


class IceLevelFactory(LevelFactory):
    def create_enemy(self) -> Enemy:
        return IceGolem()

    def create_trap(self) -> Trap:
        return IceSpike()


FACTORY_REGISTRY: Dict[str, type[LevelFactory]] = {
    "forest": ForestLevelFactory,
    "lava": LavaLevelFactory,
    "ice": IceLevelFactory,
}


def get_factory(level_name: str) -> LevelFactory:
    factory_class = FACTORY_REGISTRY.get(level_name)
    if not factory_class:
        raise ValueError(f"Неизвестный биом: {level_name}")
    return factory_class()
