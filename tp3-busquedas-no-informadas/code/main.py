"""0: mueve a la izquierda.
1: mueve hacia abajo.
2: mueve a la derecha.
3: mueve hacia arriba.
F= sin hielo
H=hielo
The observation is a value representing the players current position as current_row * nrows + current_col 
(where both the row and col start at 0)."""
from algorithms import *
import gymnasium as gym
from gymnasium import wrappers
from gymnasium.envs.toy_text.frozen_lake import generate_random_map
import random
from random import seed

#random.seed("semilla frozen lake")
#mover al enano: env.step(0) # 0: mueve a la izquierda.
"""modificar la cantidad de pasos maxima que puede dar un agente"""
#nuevo_limite = 4
#env = gym.make('FrozenLake-v1', render_mode='human').env
#env = wrappers.TimeLimit(env, nuevo_limite)

"""Arme una nueva funcion generate_random_map_custom que permita definir el tamano de
la grilla, la probabilidad que una casilla sea de hielo, y ubique de forma aleatoria la posicion
inicial del agente y del objetivo (el entorno creado a partir de dicha funcion podria no tener
solucion)."""
def generate_random_map_custom(size, ice_prob):
    desc = []
    col = ''
    sx=random.randint(0, size-1)
    sy=random.randint(0, size-1)
    # Generar ex y ey, asegurando que no sean iguales a sx y sy
    while True:
        ex = random.randint(0, size - 1)
        ey = random.randint(0, size - 1)
        if ex != sx or ey != sy:
            break
    for i in range(size):
        for j in range(size):
            if i==sx and j==sy:
                col=col + 'S'
                agent_pos = (i,j)
            elif i==ex and j==ey:
                col=col + 'G'
            else:
                if random.random() < ice_prob:
                    col=col + 'F'
                else:
                    col=col + 'H'
        desc.append(col)
        col=''
    #print(desc)
    return desc, agent_pos

#env = gym.make('FrozenLake-v1', render_mode='human')
desc_pos=generate_random_map_custom(10, 0.8)
desc=desc_pos[0]
agent_pos=desc_pos[1]
nuevo_limite = 1000
env = gym.make('FrozenLake-v1', desc=desc, is_slippery=False, render_mode='human').env
env = wrappers.TimeLimit(env, nuevo_limite)

state = env.reset()
#env = gym.make('FrozenLake-v1', desc=generate_random_map(size=8), render_mode='human')

#mejorar usando deque de collections cuando funcione xd pq es ineficiente usar listas como colas
print(desc)
print(agent_pos)
path_dfs=list()
path_bfs=list()
dfs_info=dfs_search(env,agent_pos, path_dfs)
print("dfs",path_dfs)
bfs_info=bfs_search(env,agent_pos, path_bfs)
print("bfs",path_bfs)
done=False
truncated=False
while not (done or truncated):
    if len(path_dfs)!=0:
        action=path_dfs.pop(0)
        print(path_dfs)
        next_state, reward, done, truncated, _ = env.step(action)
        print(f"Acción: {action}, Nuevo estado: {next_state}, Recompensa: {reward}")
        print(f"¿Ganó? (encontró el objetivo): {done}")
        print(f"¿Frenó? (alcanzó el máximo de pasos posible): {truncated}\n")
        
        state = next_state
    env.render()  # Renderizar el entorno
    
# Mantener la ventana abierta
input("Presiona Enter para cerrar el entorno...")

# Cerrar el entorno
env.close()

