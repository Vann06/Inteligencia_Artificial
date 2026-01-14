

class Agent:
    def act(self, perception):
        if perception > 25:
            return "enfriar"
        elif perception < 18:
            return "calentar"
        else:
            return "esperar"