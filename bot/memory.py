from typing import Any, Dict
from collections import defaultdict
import json
import os

class ConversationMemory:
    def __init__(self, persistence_file="memory.json"):
        self.memory = defaultdict(dict)
        self.persistence_file = persistence_file
        self._load()

    def store(self, user_id: int, key: str, value: Any):
        self.memory[user_id][key] = value
        self._save()

    def recall(self, user_id: int, key: str, default=None) -> Any:
        return self.memory[user_id].get(key, default)

    def clear(self, user_id: int):
        if user_id in self.memory:
            del self.memory[user_id]
            self._save()

    def _save(self):
        try:
            with open(self.persistence_file, 'w') as f:
                json.dump(dict(self.memory), f)
        except Exception as e:
            print(f"Failed to save memory: {e}")

    def _load(self):
        if os.path.exists(self.persistence_file):
            try:
                with open(self.persistence_file, 'r') as f:
                    data = json.load(f)
                    self.memory.update({int(k): v for k, v in data.items()})
            except Exception as e:
                print(f"Failed to load memory: {e}")
