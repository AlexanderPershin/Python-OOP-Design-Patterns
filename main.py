import json
from typing import Dict, Any


# ==========================================
# 1. СЛОЙ ОТОБРАЖЕНИЯ (UI)
# ==========================================
class ConsoleUI:
    @staticmethod
    def render_hero(name: str, hp: int, weapon: str, level: str):
        print("\n" + "=" * 30)
        print(f"ГЕРОЙ: {name} | HP: {hp}")
        print(f"ОРУЖИЕ: {weapon.upper()} | ЛОКАЦИЯ: {level.upper()}")
        print("=" * 30 + "\n")


# ==========================================
# 2. СЛОЙ ИНФРАСТРУКТУРЫ
# ==========================================
class SaveManager:
    @staticmethod
    def save_to_json(data: Dict[str, Any], filename: str = "save.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f)
        print(f"\n💾 Игра сохранена в {filename}")


# ==========================================
# 3. ПОДСИСТЕМЫ И ДВИЖОК
# ==========================================
class LevelManager:
    @staticmethod
    def spawn_enemies_for_level(level_name: str):
        print("Генерация врагов...")
        if level_name == "forest":
            print("Появился Лесной Орк (HP: 50)!")
        elif level_name == "lava":
            print("Появился Огненный Элементаль (HP: 100)!")
        elif level_name == "ice_caves":
            print("Появился Ледяной Тролль (HP: 80)!")


class AchievementSystem:
    @staticmethod
    def check_damage(damage: int):
        if damage > 20:
            print("🏆 АЧИВКА: Сокрушительный удар!")


class Inventory:
    def __init__(self):
        self._items = []

    def add(self, item: str):
        self._items.append(item)


# ==========================================
# 4. ДОМЕННАЯ МОДЕЛЬ — Герой
# ==========================================
class Hero:
    def __init__(self, name: str):
        self.name = name
        self.hp = 100
        self.weapon_type = "sword"
        self.inventory = Inventory()
        self.level = "forest"

    def attack(self, enemy_name: str):
        print(f"[{self.name}] атакует {enemy_name}!")
        damage = 0

        if self.weapon_type == "sword":
            damage = 15
            print("Взмах мечом! Вжииих!")
        elif self.weapon_type == "bow":
            damage = 10
            print("Выстрел из лука! Пиу!")
        elif self.weapon_type == "magic_staff":
            damage = 25
            self.hp -= 5
            print("Магический удар! Бабах! (Потрачено 5 HP)")
        else:
            print("Герой бьет кулаками.")
            damage = 2

        print(f"Нанесено {damage} урона.")

        AchievementSystem.check_damage(damage)

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
