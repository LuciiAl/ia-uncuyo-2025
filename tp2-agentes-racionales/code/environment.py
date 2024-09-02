import random

"""
Implementar un simulador que determine la medida de rendimiento para el entorno del mundo
de la aspiradora segun las siguientes especificaciones

La medida de rendimiento premia con un punto al agente por cada recuadro que limpia
(aspira) en un periodo de tiempo concreto, a lo largo de una ≪vida≫ de 1000 acciones.

La ≪dimension≫ de la grilla se conoce a priori pero la distribucion de la suciedad y la
localizacion inicial del agente no se conocen (aleatorio).

Las cuadriculas se mantienen limpias y al aspirar se limpia la cuadricula en la que se
encuentra el agente.

Las acciones Izquierda, Derecha, Arriba, Abajo mueven al agente en dichas direcciones,
excepto en el caso en que lo puedan llevar fuera de la grilla

El agente percibe su locacion y si esta contiene suciedad."""

class Environment:
    def __init__(self, sizeX, sizeY, posX, posY, dirt):
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.agent_pos = (posX, posY)
        self.grid = [[random.random() < dirt for i in range(sizeX)] for i in range(sizeY)]
        self.performance = 0
        self.actions = ['Arriba', 'Abajo', 'Izquierda', 'Derecha', 'Limpiar', 'NoHacerNada']

    def accept_action(self, action):
        x, y = self.agent_pos
        if action == 'Arriba' and y > 0:
            self.agent_pos = (x , y - 1)
        elif action == 'Abajo' and y < self.sizeY - 1:
            self.agent_pos = (x, y + 1)
        elif action == 'Izquierda' and x > 0:
            self.agent_pos = (x - 1, y )
        elif action == 'Derecha' and x < self.sizeX - 1:
            self.agent_pos = (x + 1, y )
        elif action == 'Limpiar':
            if self.grid[x][y]:  # Si hay suciedad
                self.grid[x][y] = False
                self.performance += 1
        # Si la acción es 'NoHacerNada', no se hace nada
        
    def is_dirty(self):
        x, y = self.agent_pos
        return self.grid[x][y]

    def get_performance(self):
        return self.performance

    def print_environment(self):
        for i in range(self.sizeX):
            for j in range(self.sizeY):
                if (i, j) == self.agent_pos:
                    print('A', end=' ')
                elif self.grid[i][j]:
                    print('D', end=' ')  # D para la suciedad (Dirt)
                else:
                    print('.', end=' ')
            print()
        print(f'Performance: {self.performance}')


