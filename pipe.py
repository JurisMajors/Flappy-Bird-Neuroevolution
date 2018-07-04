import numpy as np


class Pipe:
    def __init__(self, x, shape=(160, 210)):
        self.x = x
        self.width = 20
        self.top = np.random.randint(0, 3*shape[1]/4)
        self.bot = self.top + np.random.randint(100, 150)

    def collision(self, bird):
        ''' takes bird as input. if bird collides with pipe, return True. '''

        if not bird.x >= self.x:
            return False
        elif bird.y < self.top or bird.y > self.bot:
            return True

    def move(self, distance):
        self.x += distance





