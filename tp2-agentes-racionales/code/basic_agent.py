import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_agent import BaseAgent

class YourNameAgent(BaseAgent):
    def __init__(self, server_url="http://127.0.0.1:5000", **kwargs):
        super().__init__(server_url, "YourNameAgent", **kwargs)
        self.phase = "go_down"     # primero bajar
        self.direction = "up"      # snake empieza subiendo

    def get_strategy_description(self):
        return "Goes to bottom-right corner, then performs a snake pattern (up-left-down-left) until reaching a corner."

    def think(self):
        if not self.is_connected():
            return False

        perception = self.get_perception()
        if not perception or perception.get("is_finished", True):
            return False# detener ejecución

        pos = perception.get("position", (0, 0))

        # Si está sucio: limpiar primero
        if perception.get("is_dirty", False):
            return self.suck()

        # --------- Fase inicial: ir a esquina inferior derecha ----------
        if self.phase == "go_down":
            action = self.down()
            if self._stopped_moving(pos, action):
                self.phase = "go_right"
            return action

        if self.phase == "go_right":
            action = self.right()
            if self._stopped_moving(pos, action):
                self.phase = "snake"
            return action

        # --------- Fase snake ----------
        if self.phase == "snake":
            if self.direction == "up":
                action = self.up()
                if self._stopped_moving(pos, action):
                    self.direction = "down"
                    return self.left()
                return action

            elif self.direction == "down":
                action = self.down()
                if self._stopped_moving(pos, action):
                    self.direction = "up"
                    return self.left()
                return action
        return False


    def _stopped_moving(self, prev_pos, action):
        """
        Detecta si al intentar movernos seguimos en la misma posición
        (es decir, llegamos al borde).
        """
        new_perception = self.get_perception()
        new_pos = new_perception.get("position", prev_pos)
        return prev_pos == new_pos
