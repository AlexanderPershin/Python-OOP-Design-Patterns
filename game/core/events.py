from typing import Any, Callable, Dict, List


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
