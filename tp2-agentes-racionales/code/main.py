# Ejemplo de uso

from environment import *
from agent import *
import time 

if __name__ == "__main__":
    results=[]
    for j in range(1,5):
        if j==1:
            dirt=0.1
        elif j==2:
            dirt=0.2
        elif j==3:
            dirt=0.4
        else:
            dirt=0.8
        for i in range (1, 11):
            #print(f'Iteración {i}')
            size=2*2*2*2*2*2*2
            start=time.time()
            x= random.randint(1, size)
            y= random.randint(1, size)
            # Crear el entorno con tamaño 2*2, posición inicial en (x, y) y tasa de suciedad del 10%
            env = Environment(size , size, x-1, y-1, dirt)
            # Crear el agente
            ag = Agent(env)
            for action in range (1000):
                ag.think()
            #env.print_environment()
            end = time.time()
            # Imprimir el entorno final y el rendimiento
            #env.print_environment()
            results.append((i,dirt, env.get_performance(), end-start))
            #print(f'Rendimiento final: {env.get_performance()}')
            #print(f'Tiempo de ejecución: {end-start}')
    print(results)