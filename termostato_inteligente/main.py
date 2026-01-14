from env import Environment 
from agent import Agent 

def main():
    env = Environment()
    agent = Agent()

    #que corra por 10 iteraciones, imprimiendo en cada paso:  

    #El estado actual (Temperatura). o La acción elegida por el agente. o El nuevo estado después de la acción.  
    for i in range(10):
        print("Iteración", i)
        print("Estado actual:", env.temperature)
        action = agent.act(env.temperature)
        print("Acción:", action)
        env.update(action)
        print("Nuevo estado:", env.temperature)
        print("\n")