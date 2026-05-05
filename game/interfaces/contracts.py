from abc import ABC, abstractmethod


class Spawnable(ABC):
    @abstractmethod
    def spawn(self) -> str:
        pass


class Damageable(ABC):
    @abstractmethod
    def take_damage(self, amount: int) -> bool:
        """Возвращает True, если сущность уничтожена"""
        pass


class HealthQueryable(ABC):
    @abstractmethod
    def get_health_percent(self) -> float:
        pass

    @abstractmethod
    def is_alive(self) -> bool:
        pass


class Triggerable(ABC):
    @abstractmethod
    def trigger(self) -> str:
        pass


class Attackable(ABC):
    @abstractmethod
    def attack(self, target_name: str) -> int:
        pass
