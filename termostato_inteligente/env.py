import random

class Environment:

    def get_percept(self):
        #simulación de sensores
        return self.temperature

    def update(self, action):
        # modificar temperatura
        if action == "calentar":
            self.temperature += 5
        elif action == "enfriar":
            self.temperature -= 5
    
    def setTemperature(self, lower, higher):
        self.temperature = random.uniform(lower, higher)
        return self.temperature