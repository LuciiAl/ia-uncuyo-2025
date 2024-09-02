
import random

class AgentR:
    def __init__(self,env): # recibe como parametro un objeto
        self.env = env
        self.actions = ['Arriba', 'Abajo', 'Izquierda', 'Derecha', 'Limpiar', 'NoHacerNada']
        self.posX = env.agent_pos[0]
        self.posY = env.agent_pos[1]

    def up(self):
        self.env.accept_action('Arriba')
        if self.posY != self.env.agent_pos[1]:
            self.posY = self.env.agent_pos[1]
        
    def down(self):
        self.env.accept_action('Abajo')
        if self.posY != self.env.agent_pos[1]:
            self.posY = self.env.agent_pos[1]

    def left(self):
        self.env.accept_action('Izquierda')
        if self.posX != self.env.agent_pos[0]:
            self.posX = self.env.agent_pos[0]
    
    def right(self):
        self.env.accept_action('Derecha')
        if self.posX != self.env.agent_pos[0]:
            self.posX = self.env.agent_pos[0]

    def suck(self):
        self.env.accept_action('Limpiar')
    
    def idle(self):
        self.env.accept_action('NoHacerNada')
    
    def perspective(self,env):
        return env.is_dirty()
    
    def think(self):
        action=random.choice([self.up, self.down, self.left, self.right, self.idle, self.suck])  # Ejecutar un movimiento aleatorio
        action()
