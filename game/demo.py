from game.bootstrap import setup_observers
from game.core.save import SaveManager
from game.hero import Hero
from game.interfaces.contracts import Attackable, Damageable
from game.patterns.adapter import EpicBoss, EpicBossAdapter
from game.patterns.command import (
    AttackCommand,
    CommandHistory,
    DrinkPotionCommand,
)
from game.patterns.decorators import (
    FireRingDecorator,
    PoisonWeaponDecorator,
    SlowCurseDecorator,
    StrengthPotionDecorator,
)
from game.world.entities import ForestOrc


def slap(entity: Damageable, damage: int):
    dead = entity.take_damage(damage)
    print(f"  → {'💀 УМЕР' if dead else '❤️ Жив'}")


def run_demo():
    setup_observers()

    print("=" * 60)
    print("🎮 DUNGEON CRAWLER — ПОЛНАЯ ДЕМОНСТРАЦИЯ")
    print("=" * 60)

    print("\n📊 Проверка MRO ForestOrc:")
    for cls in ForestOrc.__mro__:
        print(f"  → {cls.__name__}")

    orc = ForestOrc()
    print(f"\n{orc.spawn()}")
    print(f"Жив? {orc.is_alive()}")
    orc.take_damage(20)
    orc.take_damage(40)
    print(f"HP%: {orc.get_health_percent() * 100:.1f}%")

    print("\n" + "=" * 60)
    print("🦸 СОЗДАНИЕ ГЕРОЯ")
    print("=" * 60)

    hero = Hero("Артур")
    hero.render_ui()

    print("\n⚔️ АТАКА 1: Меч (стратегия)")
    hero.attack("Гоблин")

    print("\n💥 Герой получает урон:")
    hero.take_damage(25)
    hero.render_ui()

    print("\n📦 Работа с инвентарём:")
    hero.inventory.add("Зелье лечения")
    hero.inventory.add("Карта подземелья")
    print(f"Инвентарь: {hero.inventory.list_items()}")

    print("\n🏹 Смена оружия:")
    hero.weapon_type = "bow"
    hero.attack("Орк")

    hero.weapon_type = "magic_staff"
    hero.attack("Демон")
    hero.render_ui()

    print("\n🌲 Переход в другую локацию:")
    hero.move("lava")
    hero.render_ui()

    print("\n" + "=" * 60)
    print("👋 УНИВЕРСАЛЬНАЯ ФУНКЦИЯ slap()")
    print("=" * 60)

    orc2 = ForestOrc()
    slap(orc2, 60)
    slap(hero, 90)
    hero.render_ui()

    print("\n" + "=" * 60)
    print("👹 БОСС (АДАПТЕР)")
    print("=" * 60)

    boss = EpicBossAdapter(EpicBoss("Тайрелл", 200), difficulty=1.0)
    print(boss.spawn())
    slap(boss, 100)
    slap(boss, 80)

    print("\n" + "=" * 60)
    print("🔮 ПАТТЕРН ДЕКОРАТОР (GoF)")
    print("=" * 60)

    hero2: Attackable = Hero("Мерлин")
    hero2.weapon_type = "sword"  # type: ignore

    print("\n📊 НАЧАЛЬНОЕ СОСТОЯНИЕ (голый герой):")
    hero2.render_ui()  # type: ignore

    print("\n⚔️ АТАКА 1: Без баффов")
    hero2.attack("Слизень")

    print("\n🔥 Надеваем Кольцо Огня...")
    hero2 = FireRingDecorator(hero2)
    print("\n📊 ТЕКУЩЕЕ СОСТОЯНИЕ:")
    hero2.render_ui()  # type: ignore

    print("\n⚔️ АТАКА 2: С кольцом огня")
    hero2.attack("Гоблин")

    print("\n💪 Пьём Зелье Силы...")
    hero2 = StrengthPotionDecorator(hero2)

    print("\n⚔️ АТАКА 3: Кольцо + Зелье")
    hero2.attack("Орк")

    print("\n💀 Наложено Проклятие Замедления...")
    hero2 = SlowCurseDecorator(hero2)

    print("\n⚔️ АТАКА 4: Кольцо + Зелье + Проклятие")
    hero2.attack("Дракон")

    print("\n☠️ Отравляем оружие...")
    hero2 = PoisonWeaponDecorator(hero2)

    print("\n⚔️ АТАКА 5: Полная комбинация")
    hero2.attack("Демон")

    print("\n📊 ФИНАЛЬНОЕ СОСТОЯНИЕ:")
    hero2.render_ui()  # type: ignore

    print("\n" + "=" * 60)
    print("🧪 ДЕМОНСТРАЦИЯ: ПОРЯДОК ВАЖЕН!")
    print("=" * 60)

    hero_a: Attackable = Hero("Тест-А")
    hero_a.weapon_type = "sword"  # type: ignore
    print("\nВариант А: Сначала Кольцо (+5), потом Зелье (×1.5)")
    hero_a = StrengthPotionDecorator(FireRingDecorator(hero_a))
    hero_a.attack("Манекен")

    hero_b: Attackable = Hero("Тест-Б")
    hero_b.weapon_type = "sword"  # type: ignore
    print("\nВариант Б: Сначала Зелье (×1.5), потом Кольцо (+5)")
    hero_b = FireRingDecorator(StrengthPotionDecorator(hero_b))
    hero_b.attack("Манекен")

    print("\n" + "=" * 60)
    print("📜 ПАТТЕРН КОМАНДА (GoF): атака и зелья")
    print("=" * 60)

    hero_cmd = Hero("Роланд")
    hero_cmd.take_damage(45)
    print("\nСтарт (после урона):")
    hero_cmd.render_ui()

    cmd_hist = CommandHistory()
    print("\n▶ Выполняем команды через историю:")
    cmd_hist.execute(AttackCommand(hero_cmd, "Скелет"))
    cmd_hist.execute(DrinkPotionCommand(hero_cmd, "heal"))
    hero_cmd.render_ui()

    macro_snapshot = cmd_hist.get_macro()
    print("\n↩ Отмена последней команды (зелье):")
    cmd_hist.undo()
    hero_cmd.render_ui()
    print("\n↪ Повтор (зелье снова):")
    cmd_hist.redo()
    hero_cmd.render_ui()

    hero_echo = Hero("Эхо")
    hero_echo.take_damage(60)
    print("\n🎬 Тот же сценарий — воспроизведение макроса на другом герое:")
    hero_echo.render_ui()
    cmd_hist2 = CommandHistory()
    cmd_hist2.replay_macro(macro_snapshot, hero_echo)
    hero_echo.render_ui()

    print("\n" + "=" * 60)
    print("💾 СОХРАНЕНИЕ")
    print("=" * 60)

    SaveManager.save_to_json(hero.export_state(), "hero_save.json")
    SaveManager.save_to_json(hero2.export_state(), "hero2_save.json")

    print("\n" + "=" * 60)
    print("✅ Демонстрация завершена!")
    print("=" * 60)
