import json
from typing import Any, Dict


class SaveManager:
    @staticmethod
    def save_to_json(data: Dict[str, Any], filename: str = "save.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f)
        print(f"\n💾 Игра сохранена в {filename}")
