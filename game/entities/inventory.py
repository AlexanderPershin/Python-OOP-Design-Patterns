from typing import List


class Inventory:
    def __init__(self):
        self._items = []

    def add(self, item: str):
        self._items.append(item)
        print(f"📦 В инвентарь добавлено: {item}")

    def list_items(self) -> List[str]:
        return self._items.copy()
