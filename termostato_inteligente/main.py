from env import Environment 
from agent import Agent 

def main():
    env = Environment()
    agent = Agent()

    #que corra por 10 iteraciones, imprimiendo en cada paso:  

    #El estado actual (Temperatura). o La acción elegida por el agente. o El nuevo estado después de la acción.  
    for i in range(10):
        print("Iteración", i)
        actual_temp: int = env.setTemperature(15, 30)
        print("Estado actual:", actual_temp)
        action = agent.act(actual_temp)
        print("Acción:", action)
        env.update(action)
        print("Nuevo estado:", env.temperature)
        print("\n")

main()