import random

class Environment:
    def __init__(self):
        self.temperature = random.uniform(15, 30)  # Temperature in Celsius

    def get_percept(self):
        #simulación de sensores
        return self.temperature

    def update(self, action):
        # modificar temperatura
        if action == "calentar":
            self.temperature += 5
        elif action == "enfriar":
            self.temperature -= 5