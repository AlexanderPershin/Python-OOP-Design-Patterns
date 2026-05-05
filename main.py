import json


class Hero:
    def __init__(self, name: str):
        self.name = name
        self.hp = 100
        self.weapon_type = "sword"
        self.inventory = []
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

        if damage > 20:
            print("🏆 АЧИВКА: Сокрушительный удар!")

    def move(self, location: str):
        self.level = location
        print(f"\n[{self.name}] переходит в локацию: {self.level}")
        self.spawn_enemy()

    def spawn_enemy(self):
        print("Генерация врагов...")
        if self.level == "forest":
            print("Появился Лесной Орк (HP: 50)!")
        elif self.level == "lava":
            print("Появился Огненный Элементаль (HP: 100)!")
        elif self.level == "ice_caves":
            print("Появился Ледяной Тролль (HP: 80)!")

    def save_game(self, filename: str = "save.json"):
        data = {
            "name": self.name,
            "hp": self.hp,
            "weapon_type": self.weapon_type,
            "level": self.level,
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f)
        print(f"\n💾 Игра сохранена в {filename}")

    def render_ui(self):
        print("\n" + "=" * 30)
        print(f"ГЕРОЙ: {self.name} | HP: {self.hp}")
        print(
            f"ОРУЖИЕ: {self.weapon_type.upper()} | ЛОКАЦИЯ: {self.level.upper()}"
        )
        print("=" * 30 + "\n")


if __name__ == "__main__":
    player = Hero("Артур")
    player.render_ui()

    player.attack("Слизень")

    player.weapon_type = "magic_staff"
    player.attack("Гоблин")

    player.move("lava")
    player.save_game()
