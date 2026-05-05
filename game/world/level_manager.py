from game.world.entities import get_factory


class LevelManager:
    @staticmethod
    def spawn_enemies_for_level(level_name: str):
        print("Генерация врагов...")
        factory = get_factory(level_name)

        enemy = factory.create_enemy()
        trap = factory.create_trap()

        print(enemy.spawn())
        print(trap.trigger())
