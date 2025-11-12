import time
from typing import Dict, List, Callable

class EventBus:

    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.last_publish_time: Dict[str, float] = {}
        self.debounce_delay = 0.1

    def subscribe(self, event_name: str, callback: Callable):

        if event_name not in self.subscribers:
            self.subscribers[event_name] = []
        if callback not in self.subscribers[event_name]:
            self.subscribers[event_name].append(callback)

    def unsubscribe(self, event_name: str, callback: Callable):

        if event_name in self.subscribers:
            if callback in self.subscribers[event_name]:
                self.subscribers[event_name].remove(callback)

    def publish(self, event_name: str, data=None):

        current_time = time.time()
        last_time = self.last_publish_time.get(event_name, 0)
        
        if current_time - last_time < self.debounce_delay:
            return 
        
        self.last_publish_time[event_name] = current_time
        
        if event_name in self.subscribers:
            for callback in self.subscribers[event_name]:
                try:
                    callback(data)
                except Exception as e:
                    print(f"Error in event callback for '{event_name}': {e}")
                    import traceback
                    traceback.print_exc()

event_bus = EventBus()