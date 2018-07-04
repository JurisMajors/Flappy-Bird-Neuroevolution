

class Bird:

    def __init__(self, shape=(160, 210)):
        self.radius = 5
        self.x = self.radius + 10
        self.height = shape[1]
        self.y = int(self.height / 2)
        self.flapping = False
        self.score = 0

    def set_flapping(self):
        self.flapping = True

    def flap(self, distance_y):
        if self.y > self.height - self.radius:
            self.y = self.height - self.radius
        elif self.y < 0:
            self.y = self.radius
        else:
            self.y += distance_y

    def increase_score(self, increase):
        self.score += increase
        self.score = round(self.score, 1)




