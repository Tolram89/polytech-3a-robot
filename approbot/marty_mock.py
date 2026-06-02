# marty_mock.py

class MartyMock:

    def __init__(self):
        self.historique = []

    def walk(self, steps: int, step_length: int, move_time: int):
        direction = "avant" if step_length > 0 else "arrière"
        entry = {
            "action": "walk",
            "steps": steps,
            "direction": direction,
            "move_time": move_time,
        }
        self.historique.append(entry)
        print(f"[MOCK] walk → {steps} pas en {direction} ({move_time}ms)")

    def sidestep(self, side: str, steps: int, move_time: int):
        entry = {
            "action": "sidestep",
            "steps": steps,
            "side": side,
            "move_time": move_time,
        }
        self.historique.append(entry)
        print(f"[MOCK] sidestep → {steps} pas à {side} ({move_time}ms)")

    def arms(self, left_angle: int, right_angle: int, move_time: int):
        entry = {
            "action": "arms",
            "left_angle": left_angle,
            "right_angle": right_angle,
            "move_time": move_time,
        }
        self.historique.append(entry)
        print(f"[MOCK] arms → gauche={left_angle}° droite={right_angle}° ({move_time}ms)")

    def eyes(self, pose_or_angle, move_time: int = 1000):
        entry = {
            "action": "eyes",
            "pose_or_angle": pose_or_angle,
            "move_time": move_time,
        }
        self.historique.append(entry)
        print(f"[MOCK] eyes → {pose_or_angle} ({move_time}ms)")

    def disco_color(self, color: str, add_on: str, region: str = 'all'):
        entry = {
            "action": "disco_color",
            "color": color,
            "add_on": add_on,
        }
        self.historique.append(entry)
        print(f"[MOCK] disco_color → {color} sur {add_on}")
