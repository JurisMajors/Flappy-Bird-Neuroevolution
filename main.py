from operator import itemgetter

import pygame
from bird import Bird
from pipe import Pipe
import numpy as np
import random

SHAPE = (500, 500)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WIDTH = SHAPE[0]
HEIGHT = SHAPE[1]
POPULATION = 30
np.random.seed(1)
random.seed(1)
pygame.init()
screen = pygame.display.set_mode(SHAPE)
clock = pygame.time.Clock()
font = pygame.font.Font(None, int(0.1*WIDTH))

def start_game():
    birds = []
    for _ in range(POPULATION):
        player = Bird(SHAPE)
        birds.append(player)
    pipes = init_pipes()
    return birds,   pipes


def init_pipes():
    pipes = [Pipe(x=WIDTH, shape=SHAPE, seed=1)]
    return pipes

def clean_and_move_pipes(pipes, pipe_speed):
    passed = False
    for pipe in pipes:
        if pipe.x + pipe.width < 0:
            pipes.remove(pipe)
            passed = True
        else:
            pipe.move(pipe_speed)
    return pipes, passed


def new_pipe(when, pipes):
    if pipes[-1].x <= when:
        p = Pipe(x=WIDTH, shape=SHAPE, seed=np.random.randint(1, 9))
        pipes.append(p)
    return pipes


def bound_delta_y(dy, low, high):
    if dy < low:
        dy = low
    elif dy > high:
        dy = high
    return dy


def normalize(x, low, high):
    return (x - low)/(high - low)


def select_action(bird, pipes):
    possible_distance = (pipes[0].x + pipes[0].width) - bird.x
    if possible_distance >= 0:
        distance = possible_distance
        closest_pipe = pipes[0]
    else:
        distance = (pipes[1].x + pipes[1].width)- bird.x
        closest_pipe = pipes[1]

    distance = normalize(distance, 0, WIDTH - 10)
    bird_height = normalize(bird.y, 0, HEIGHT)
    pipe_top = normalize(closest_pipe.top, 0, 3*HEIGHT/4)
    pipe_bot = normalize(closest_pipe.bot, 100, 3*HEIGHT/4 + 150)
    pipe_middle = (pipe_bot - pipe_top) / 2 + pipe_top
    distance_from_middle = pipe_middle - bird_height
    input = np.asarray([bird_height, distance, distance_from_middle, (5+bird.velocity)/10])
    input = np.atleast_2d(input)
    probability = bird.brain.predict(input, batch_size=1)[0]
    if probability[0] >= 0.5:
        return 1
    return 2




def draw_bird(player):
    pygame.draw.circle(screen, WHITE, [player.x, player.y], player.radius)


def draw_pipes(pipe):
    for p in pipe:
        pygame.draw.rect(screen, WHITE, [p.x, 0, p.width, p.top])
        pygame.draw.rect(screen, WHITE, [p.x, p.bot, p.width, HEIGHT - p.bot])  # better length????


def draw_scores(score):
    score_text = font.render(str(score), True, WHITE)
    screen.blit(score_text, [10, 0])


def draw(pipe):
    screen.fill(BLACK)
    draw_pipes(pipe)

def main():
    birds, pipes = start_game()
    all_time_best = birds[0]
    pipe_speed = -10
    generations = 400
    all_birds = []
    for generation in range(generations):
        drawing = True
        print('Generation {} started'.format(generation))
        running = True
        pipes = init_pipes()
        scores = [0]*len(birds)
        while running:

            if drawing:
                draw(pipes)
            for player in birds:
                if pipes[0].collision(player):
                    all_birds.append(player)
                    birds.remove(player)
                else:
                    player.increase_score(1)
                    if drawing:
                        draw_bird(player)

            if len(birds) < 1:
                running = False
            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         pygame.display.quit()

            pipes, player_passed_pipe = clean_and_move_pipes(pipes, pipe_speed)
            counter = 0
            for player in birds:
                action = select_action(player, pipes)
                player.flapping = False
                if action == 1:
                    player.flapping = True

                # if player.flapping:
                #     flapping_speed = flapping_max
                # else:
                #     flapping_speed = 0
                #
                # dy += gravity + flapping_speed
                # dy = bound_delta_y(dy, flapping_max, gravity)

                player.flap()

                if player_passed_pipe:
                    player.increase_score(50)
                if player.score > all_time_best.score:
                    all_time_best = player
                scores[counter] = player.score
                counter += 1
                # if player.score > 5000:
                #     running = False
                #     all_time_best = player
                #     return all_time_best

            #draw_scores(max(scores))

            pipes = new_pipe(WIDTH/3, pipes)
            if drawing:
                pygame.display.flip()
                clock.tick(60)
        # create new population of birds
        total_scores = sum(scores)
        maximum = max(scores)
        for bird in all_birds:  # CALCULATE ALL FITNESS
            bird.set_fitness(total_scores)

        fitnesses = [(bird.fitness, bird) for bird in all_birds]
        fitnesses = sorted(fitnesses, key=itemgetter(0), reverse=True)
        #print(fitnesses)
        best_birds = [bird for fitness, bird in fitnesses[:10]]
        parent_one = best_birds[0]
        parent_two = best_birds[1]
        new_child, new_child2 = parent_one.crossover(parent_two)
        best_birds[-1] = new_child
        best_birds[-2] = new_child2
        parent_one = best_birds[2]
        parent_two = best_birds[3]
        new_child, new_child2 = parent_one.crossover(parent_two)
        best_birds[-3] = new_child
        best_birds[-4] = new_child2

        birds = best_birds
        amount = len(birds)
        for index in range(POPULATION - amount):
            birds.append(pick_a_bird(all_birds))
        all_birds = []
        print('Generation {} , max score {}'.format(generation, maximum))
    return all_time_best

def pick_a_bird(all_birds):
    index = 0
    r = random.uniform(0, 1)

    while index < len(all_birds) and r > 0:
        r -= all_birds[index].fitness
        index += 1
    index -= 1
    bird = all_birds[index]
    child = Bird(shape=SHAPE, brain=bird.brain)
    child.mutate(0.2)
    return child



bird = main()
#pygame.init()


# def draw_bird(player):
#     pygame.draw.circle(screen, WHITE, [player.x, player.y], player.radius)
#
#
# def draw_pipes(pipe):
#     for p in pips:
#         pygame.draw.rect(screen, WHITE, [p.x, 0, p.width, p.top])
#         pygame.draw.rect(screen, WHITE, [p.x, p.bot, p.width, HEIGHT - p.bot])  # better length????
#
#
# def draw_scores(score):
#     score_text = font.render(str(score), True, WHITE)
#     screen.blit(score_text, [10, 0])
#
#
# def draw(pipe):
#     screen.fill(BLACK)
#     draw_pipes(pipe)


pipes = init_pipes()
running = True
pipe_speed = -3
while running:
    draw(pipes)
    draw_bird(bird)

    action = select_action(bird, pipes)
    bird.flapping = False
    if action == 1:
        bird.set_flapping()

    bird.flap()
    pipes, passed_pipe = clean_and_move_pipes(pipes, pipe_speed)
    pipes = new_pipe(WIDTH/3, pipes)
    pygame.display.flip()
    clock.tick(60)




