from keras.models import Sequential
from keras.optimizers import  SGD
from keras.layers import Dense, Activation
from random import uniform, randint


class Bird:

    def __init__(self, shape=(160, 210), brain=0):
        self.radius = 5
        self.x = self.radius + 10
        self.height = shape[1]
        self.y = int(self.height / 2)
        self.flapping = False
        self.score = 0
        self.fitness = 0
        self.alive = True
        self.shape = shape
        self.gravity = 2
        self.velocity = 0
        self.lift = -3

        if brain == 0:
            self.brain = self.make_brain()
        else:
            self.brain = brain

    def make_brain(self):
        brain = Sequential()
        brain.add(Dense(units=16, input_dim=4))
        brain.add(Activation('relu'))
        brain.add(Dense(units=1))
        brain.add(Activation('sigmoid'))
        sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        brain.compile(loss='mse', optimizer=sgd)
        return brain

    def set_flapping(self):
        if self.velocity < 0:
            self.flapping = True

    def cap_velocity(self):
        cap = 8
        if self.velocity > cap:
            self.velocity = cap
        elif self.velocity < -cap:
            self.velocity = -cap

    def flap(self):
            self.velocity += self.gravity
            if self.flapping:
                self.velocity += self.lift
            self.cap_velocity()
            #self.velocity *= 0.9
            self.y += self.velocity

    def increase_score(self, increase):
        self.score += increase
        self.score = round(self.score, 1)

    def set_fitness(self, value):
        self.fitness = self.score/value

    def crossover(self, other_bird):
        my_weights = self.brain.get_weights()
        other_weights = other_bird.brain.get_weights()
        new_weights = my_weights
        new_weights2 = other_weights
        first_layer_weights = my_weights[0]
        other_first_layer_weights = other_weights[0]
        index = randint(0, len(first_layer_weights) - 1)
        counter = 0
        for _ in first_layer_weights:
            if counter > index:
                new_weights[0][counter] = other_first_layer_weights[counter]
                new_weights2[0][counter] = first_layer_weights[counter]
            counter += 1

        bird_one = Bird(self.shape)
        bird_two = Bird(self.shape)
        bird_one.brain.set_weights(new_weights2)
        bird_two.brain.set_weights(new_weights)
        return bird_one, bird_two

    def mutate(self, p):
        weights = self.brain.get_weights()
        for xi in range(len(weights)):
            for yi in range(len(weights[xi])):
                if uniform(0, 1) <= p:
                    change = uniform(-0.1, 0.1)
                    weights[xi][yi] += change

        self.brain.set_weights(weights)




