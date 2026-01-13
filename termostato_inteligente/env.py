import random

class Environment:
    def __init__(self):
        self.temperature = random.uniform(15, 30)  # Temperature in Celsius
        self.humidity = random.uniform(30, 70)      # Humidity in percentage

    def get_percept(self):
        #simulación de sensores
        pass 

    def update(self, action):
        # modificar temperatura
        pass