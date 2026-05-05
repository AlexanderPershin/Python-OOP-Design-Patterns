class HasHealth:
    def __init__(self, health: int = 100, *args, **kwargs):
        self._health = health
        self._max_health = health
        super().__init__(*args, **kwargs)

    @property
    def health(self) -> int:
        return self._health

    @property
    def max_health(self) -> int:
        return self._max_health

    def take_damage(self, amount: int) -> bool:
        self._health = max(0, self._health - amount)
        print(
            f"💥 {getattr(self, 'name', 'Unknown')} получил {amount} урона. HP: {self._health}/{self._max_health}"
        )
        return self._health == 0

    def get_health_percent(self) -> float:
        return self._health / self._max_health if self._max_health else 0.0

    def is_alive(self) -> bool:
        return self._health > 0

    def heal(self, amount: int) -> None:
        self._health = min(self._max_health, self._health + amount)
