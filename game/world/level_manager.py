from game.world.entities import get_factory


class LevelManager:
    @staticmethod
    def spawn_enemies_for_level(level_name: str):
        print("Генерация врагов...")
        enemy_class, trap_class = get_factory(level_name)

        enemy = enemy_class()
        trap = trap_class()

        print(enemy.spawn())
        print(trap.trigger())
