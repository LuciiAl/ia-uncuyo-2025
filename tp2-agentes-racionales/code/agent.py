"""Implementar un agente reflexivo simple para el entorno de la aspiradora del ejercicio anterior.
A continuacion se describe una posible interfaz a utilizar para el agente"""

"""class Agent:
def __init__(self,env): # recibe como parametro un objeto
# de la clase Environment
def up(self):
def down(self):
def left(self):
def right(self):
def suck(self): # Limpia
def idle(self): # no hace nada
def perspective(self,env): # sensa el entorno
def think(self): # implementa las acciones a seguir por el agente"""

import random

class Agent:
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
        if self.perspective(self.env):
            self.suck()
        random.choice(self.up, self.down, self.left, self.right, self.idle)  # Ejecutar un movimiento aleatorio
