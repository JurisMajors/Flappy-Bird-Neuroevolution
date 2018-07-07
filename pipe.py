import numpy as np


class Pipe:
    def __init__(self, x, shape=(160, 210), seed = 1):
        self.x = x
        self.width = 20
        self.height = shape[1]
        self.top = np.random.randint(0, 3*self.height/4)
        self.bot = self.top + np.random.randint(100, 150)

    def collision(self, bird):
        ''' takes bird as input. if bird collides with pipe, return True. '''

        if bird.y < bird.radius or bird.y > self.height - bird.radius:
            return True
        elif not bird.x >= self.x:
            return False
        elif bird.y < self.top or bird.y > self.bot:
            bird.alive = False
            return True


    def move(self, distance):
        self.x += distance





