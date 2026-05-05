class ConsoleUI:
    @staticmethod
    def render_hero(
        name: str,
        hp: int,
        max_hp: int,
        weapon: str,
        level: str,
        buffs: str = "",
    ):
        print("\n" + "=" * 40)
        print(f"ГЕРОЙ: {name} | HP: {hp}/{max_hp}")
        print(f"ОРУЖИЕ: {weapon.upper()} | ЛОКАЦИЯ: {level.upper()}")
        if buffs:
            print(f"ЭФФЕКТЫ: {buffs}")
        print("=" * 40 + "\n")
