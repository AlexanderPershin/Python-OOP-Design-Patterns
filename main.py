import json
from abc import ABC, abstractmethod
from typing import Dict, Any, Callable, List


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
    def render_hero(
        name: str, hp: int, weapon: str, level: str, buffs: str = ""
    ):
        print("\n" + "=" * 40)
        print(f"ГЕРОЙ: {name} | HP: {hp}")
        print(f"ОРУЖИЕ: {weapon.upper()} | ЛОКАЦИЯ: {level.upper()}")
        if buffs:
            print(f"ЭФФЕКТЫ: {buffs}")
        print("=" * 40 + "\n")


class SaveManager:
    @staticmethod
    def save_to_json(data: Dict[str, Any], filename: str = "save.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f)
        print(f"\n💾 Игра сохранена в {filename}")


class Enemy(ABC):
    @abstractmethod
    def spawn(self) -> str:
        pass


class Trap(ABC):
    @abstractmethod
    def trigger(self) -> str:
        pass


class LevelFactory(ABC):
    @abstractmethod
    def create_enemy(self) -> Enemy:
        pass

    @abstractmethod
    def create_trap(self) -> Trap:
        pass


class ForestOrc(Enemy):
    def spawn(self) -> str:
        return "🌲 Лесной Орк вылез из-за дерева! (HP: 50)"


class ForestSnare(Trap):
    def trigger(self) -> str:
        return "🕸️ Ловушка-сеть! Герой опутан ветвями"


class ForestLevelFactory(LevelFactory):
    def create_enemy(self) -> Enemy:
        return ForestOrc()

    def create_trap(self) -> Trap:
        return ForestSnare()


class FireElemental(Enemy):
    def spawn(self) -> str:
        return "🔥 Огненный Элементаль восстал из лавы! (HP: 100)"


class LavaPit(Trap):
    def trigger(self) -> str:
        return "🌋 Лавовая яма! Ноги обжигает"


class LavaLevelFactory(LevelFactory):
    def create_enemy(self) -> Enemy:
        return FireElemental()

    def create_trap(self) -> Trap:
        return LavaPit()


class IceGolem(Enemy):
    def spawn(self) -> str:
        return "❄️ Ледяной Голем пробудился! (HP: 120, броня: 20)"


class IceSpike(Trap):
    def trigger(self) -> str:
        return "🧊 Ледяной шип выстрелил из-под ног!"


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


class LevelManager:
    @staticmethod
    def spawn_enemies_for_level(level_name: str):
        print("Генерация врагов...")
        factory = get_factory(level_name)

        enemy = factory.create_enemy()
        trap = factory.create_trap()

        print(enemy.spawn())
        print(trap.trigger())


# ==========================================
# ПАТТЕРН ДЕКОРАТОР (GoF)
# ==========================================


class Attackable(ABC):
    @abstractmethod
    def attack(self, enemy_name: str) -> int:
        pass

    @abstractmethod
    def get_stats(self) -> Dict[str, Any]:
        pass


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
        print(f"💪 {self.NAME} умножает урон на {self.BONUS_DAMAGE}")
        return base_damage * self.MULTIPLIER


class SlowCurseDecorator(AttackDecorator):
    MULTIPLIER = 0.5
    NAME = "Проклятие замедления"

    def _apply_damage_modification(self, base_damage: int) -> int:
        print(f"{self.NAME} умножает урон на {self.MULTIPLIER}")
        return base_damage * self.MULTIPLIER


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
        self._wrapped.hp = max(0, self._wrapped.hp - self.HP_COST)
        print(f"🩸 {self.NAME} умножает урон на {self.MULTIPLIER}")
        print(f"🩸 {self.NAME} отнимает {self.HP_COST} здоровья")
        return base_damage * self.MULTIPLIER


# ==========================================
# КОНЕЦ ОБНОВЛЕНИЙ
# ==========================================


class AchievementSystem:
    @staticmethod
    def on_damage_dealt(damage: int):
        if damage > 20:
            print("🏆 АЧИВКА: Сокрушительный удар!")
        if damage > 40:
            print("🏆 АЧИВКА: Бог войны!")


class AudioEngine:
    @staticmethod
    def on_damage_dealt(damage: int):
        if damage > 30:
            print("🔊 ЗВУК: [Эпичный взрыв и крик врага]")
        elif damage > 15:
            print("🔊 ЗВУК: [Мощный удар]")
        else:
            print("🔊 ЗВУК: [Глухой звук удара]")


class Inventory:
    def __init__(self):
        self._items = []

    def add(self, item: str):
        self._items.append(item)
        print(f"📦 В инвентарь добавлено: {item}")

    def list_items(self) -> List[str]:
        return self._items.copy()


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


class Hero(Attackable):
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
        print(f"⚔️ Оружие изменено на: {weapon_name}")

    def attack(self, enemy_name: str) -> int:
        print(f"[{self.name}] атакует {enemy_name}!")
        damage = self._attack_strategy(self, enemy_name)
        print(f"Базовый урон: {damage}")
        game_events.notify("damage_dealt", damage)
        return damage

    def get_stats(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "hp": self.hp,
            "weapon": self.weapon_type,
            "level": self.level,
        }

    def move(self, location: str):
        self.level = location
        print(f"\n[{self.name}] переходит в локацию: {self.level}")
        LevelManager.spawn_enemies_for_level(self.level)

    def render_ui(self):
        stats = self.get_stats()
        ConsoleUI.render_hero(
            stats["name"],
            stats["hp"],
            stats["weapon"],
            stats["level"],
        )

    def export_state(self) -> Dict[str, Any]:
        stats = self.get_stats()
        return {
            "name": stats["name"],
            "hp": stats["hp"],
            "weapon_type": stats["weapon"],
            "level": stats["level"],
            "inventory": self.inventory.list_items(),
        }


if __name__ == "__main__":
    print("=" * 50)
    print("🎮 DUNGEON CRAWLER + ПАТТЕРН ДЕКОРАТОР (GoF)")
    print("=" * 50)

    hero: Attackable = Hero("Артур")

    print("\n📊 НАЧАЛЬНОЕ СОСТОЯНИЕ (голый герой):")
    hero.render_ui()

    print("\n⚔️ АТАКА 1: Без баффов")
    hero.attack("Слизень")

    print("\n🔥 Надеваем Кольцо Огня...")
    hero = FireRingDecorator(hero)
    print("\n📊 ТЕКУЩЕЕ СОСТОЯНИЕ:")
    hero.render_ui()

    print("\n⚔️ АТАКА 2: С кольцом огня")
    hero.attack("Гоблин")

    print("\n💪 Пьём Зелье Силы...")
    hero = StrengthPotionDecorator(hero)

    print("\n⚔️ АТАКА 3: Кольцо + Зелье")
    hero.attack("Орк")

    print("\n💀 Наложено Проклятие Замедления...")
    hero = SlowCurseDecorator(hero)

    print("\n⚔️ АТАКА 4: Кольцо + Зелье + Проклятие")
    hero.attack("Дракон")

    print("\n☠️ Отравляем оружие...")
    hero = PoisonWeaponDecorator(hero)

    print("\n⚔️ АТАКА 5: Полная комбинация")
    hero.attack("Демон")

    print("\n📊 ФИНАЛЬНОЕ СОСТОЯНИЕ:")
    hero.render_ui()

    print("\n💾 СОХРАНЕНИЕ:")
    SaveManager.save_to_json(hero.export_state())

    print("\n" + "=" * 50)
    print("🧪 ДЕМОНСТРАЦИЯ: ПОРЯДОК ВАЖЕН!")
    print("=" * 50)

    hero2: Attackable = Hero("Тест")
    hero2.weapon_type = "sword"
    print("\nВариант А: Сначала Кольцо, потом Зелье")
    hero_a = StrengthPotionDecorator(FireRingDecorator(hero2))
    hero_a.attack("Манекен")

    hero3: Attackable = Hero("Тест2")
    hero3.weapon_type = "sword"
    print("\nВариант Б: Сначала Зелье, потом Кольцо")
    hero_b = FireRingDecorator(StrengthPotionDecorator(hero3))
    hero_b.attack("Манекен")

    print("\n" + "=" * 50)
    print("✅ Демонстрация завершена!")
    print("=" * 50)
