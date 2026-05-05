import json
from typing import Dict, Any, Callable, List


# ==========================================
# ЯДРО СОБЫТИЙ (Основа паттерна Observer)
# ==========================================
class EventManager:
    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, listener: Callable):
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)

    def notify(self, event_type: str, data: Any = None):
        for listener in self._listeners.get(event_type, []):
            listener(data)


game_events = EventManager()


class ConsoleUI:
    @staticmethod
    def render_hero(name: str, hp: int, weapon: str, level: str):
        print("\n" + "=" * 30)
        print(f"ГЕРОЙ: {name} | HP: {hp}")
        print(f"ОРУЖИЕ: {weapon.upper()} | ЛОКАЦИЯ: {level.upper()}")
        print("=" * 30 + "\n")


class SaveManager:
    @staticmethod
    def save_to_json(data: Dict[str, Any], filename: str = "save.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f)
        print(f"\n💾 Игра сохранена в {filename}")


# ==========================================
# ПОДСИСТЕМЫ И ДВИЖОК (Подписчики/Наблюдатели)
# ==========================================
class LevelManager:
    @staticmethod
    def spawn_enemies_for_level(level_name: str):
        print("Генерация врагов...")
        if level_name == "forest":
            print("Появился Лесной Орк (HP: 50)!")
        elif level_name == "lava":
            print("Появился Огненный Элементаль (HP: 100)!")


class AchievementSystem:
    @staticmethod
    def on_damage_dealt(damage: int):
        if damage > 20:
            print("🏆 АЧИВКА: Сокрушительный удар!")


class AudioEngine:
    @staticmethod
    def on_damage_dealt(damage: int):
        if damage > 20:
            print("🔊 ЗВУК: [Эпичный взрыв и крик врага]")
        else:
            print("🔊 ЗВУК: [Глухой звук удара]")


class Inventory:
    def __init__(self):
        self._items = []

    def add(self, item: str):
        self._items.append(item)


game_events.subscribe("damage_dealt", AchievementSystem.on_damage_dealt)
game_events.subscribe("damage_dealt", AudioEngine.on_damage_dealt)


WeaponStrategy = Callable[["Hero", str], int]


def sword_strategy(hero: "Hero", enemy_name: str) -> int:
    print("Взмах мечом! Вжииих!")
    return 15


def bow_strategy(hero: "Hero", enemy_name: str) -> int:
    print("Выстрел из лука! Пиу!")
    return 10


def magic_staff_strategy(hero: "Hero", enemy_name: str) -> int:
    hero.hp -= 5
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


class Hero:
    def __init__(self, name: str):
        self.name = name
        self.hp = 100
        self.inventory = Inventory()
        self.level = "forest"

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

    def attack(self, enemy_name: str):
        print(f"[{self.name}] атакует {enemy_name}!")
        damage = self._attack_strategy(self, enemy_name)
        print(f"Нанесено {damage} урона.")

        game_events.notify("damage_dealt", damage)

    def move(self, location: str):
        self.level = location
        print(f"\n[{self.name}] переходит в локацию: {self.level}")
        LevelManager.spawn_enemies_for_level(self.level)

    def render_ui(self):
        ConsoleUI.render_hero(self.name, self.hp, self.weapon_type, self.level)

    def export_state(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "hp": self.hp,
            "weapon_type": self.weapon_type,
            "level": self.level,
        }


if __name__ == "__main__":
    player = Hero("Артур")
    player.render_ui()

    player.attack("Слизень")

    player.weapon_type = "magic_staff"
    player.attack("Гоблин")

    player.move("lava")
    SaveManager.save_to_json(player.export_state())
