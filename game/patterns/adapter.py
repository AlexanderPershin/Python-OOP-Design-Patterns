from game.interfaces.contracts import Damageable, HealthQueryable, Spawnable


class EpicBoss:
    """Чужой код — менять нельзя."""

    def __init__(self, name: str, base_hp: int):
        self._name = name
        self._max_hp = base_hp
        self._current_hp = base_hp
        self._phase = 1
        self._is_enraged = False

    def initialize_combat(self, difficulty: float):
        self._current_hp = int(self._max_hp * difficulty)
        print(f"[EpicBoss] {self._name} enters combat!")

    def apply_damage(self, raw: float) -> dict:
        actual = raw * (0.5 if self._is_enraged else 1.0)
        self._current_hp -= int(actual)
        if self._current_hp / self._max_hp < 0.3 and self._phase < 3:
            self._phase = 3
            self._is_enraged = True
            print("[EpicBoss] PHASE 3! ENRAGED!")
        return {
            "dead": self._current_hp <= 0,
            "hp_ratio": max(0, self._current_hp) / self._max_hp,
        }


class EpicBossAdapter(Spawnable, Damageable, HealthQueryable):
    """Адаптер для чужого кода"""

    def __init__(self, boss: EpicBoss, difficulty: float = 1.0):
        self._boss = boss
        self._difficulty = difficulty
        self._spawned = False

    def spawn(self) -> str:
        self._boss.initialize_combat(self._difficulty)
        self._spawned = True
        return f"⚠️ БОСС {self._boss._name} появился!"

    def take_damage(self, amount: int) -> bool:
        if not self._spawned:
            self.spawn()
        result = self._boss.apply_damage(float(amount))
        return result["dead"]

    def get_health_percent(self) -> float:
        return self._boss._current_hp / self._boss._max_hp

    def is_alive(self) -> bool:
        return self._boss._current_hp > 0
