from typing import TYPE_CHECKING, Callable, Dict

if TYPE_CHECKING:
    from game.hero import Hero

WeaponStrategy = Callable[["Hero", str], int]


def sword_strategy(hero: "Hero", enemy_name: str) -> int:
    print("Взмах мечом! Вжииих!")
    return 15


def bow_strategy(hero: "Hero", enemy_name: str) -> int:
    print("Выстрел из лука! Пиу!")
    return 10


def magic_staff_strategy(hero: "Hero", enemy_name: str) -> int:
    hero._health = max(0, hero._health - 5)
    print("Магический удар! Бабах! (Потрачено 5 HP)")
    return 25


def unarmed_strategy(hero: "Hero", enemy_name: str) -> int:
    print("Герой бьет кулаками.")
    return 2


WEAPON_REGISTRY: Dict[str, WeaponStrategy] = {
    "sword": sword_strategy,
    "bow": bow_strategy,
    "magic_staff": magic_staff_strategy,
}
