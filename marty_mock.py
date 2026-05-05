# marty_mock.py

class MartyMock:

    def __init__(self):
        self.historique = []

    def walk(self, num_steps: int, step_length: int, move_time: int):
        direction = "avant" if step_length > 0 else "arrière"
        entry = {
            "action": "walk",
            "num_steps": num_steps,
            "direction": direction,
            "move_time": move_time,
        }
        self.historique.append(entry)
        print(f"[MOCK] walk → {num_steps} pas en {direction} ({move_time}ms)")

    def sidestep(self, side: str, num_steps: int, move_time: int):
        entry = {
            "action": "sidestep",
            "num_steps": num_steps,
            "side": side,
            "move_time": move_time,
        }
        self.historique.append(entry)
        print(f"[MOCK] sidestep → {num_steps} pas à {side} ({move_time}ms)")