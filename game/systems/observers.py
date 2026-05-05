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
