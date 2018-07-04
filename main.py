import pygame
from bird import Bird
from pipe import Pipe
import numpy as np

SHAPE = (500, 500)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WIDTH = SHAPE[0]
HEIGHT = SHAPE[1]
pygame.init()
screen = pygame.display.set_mode(SHAPE)
clock = pygame.time.Clock()
font = pygame.font.Font(None, int(0.1*WIDTH))

def start_game():
    player = Bird(SHAPE)
    pipes = [Pipe(x=WIDTH, shape=SHAPE)]
    return player, pipes


def draw_bird(player):
    pygame.draw.circle(screen, WHITE, [player.x, player.y], player.radius)


def draw_pipes(pipes):
    for p in pipes:
        pygame.draw.rect(screen, WHITE, [p.x, 0, p.width, p.top])
        pygame.draw.rect(screen, WHITE, [p.x, p.bot, p.width, HEIGHT - p.bot])  # better length????


def draw_scores(score):
    score_text = font.render(str(score), True, WHITE)
    screen.blit(score_text, [10, 0])


def draw(player, pipes):
    screen.fill(BLACK)
    draw_bird(player)
    draw_pipes(pipes)
    draw_scores(player.score)


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
        p = Pipe(x=WIDTH, shape=SHAPE)
        pipes.append(p)
    return pipes


def bound_delta_y(dy, low, high):
    if dy < low:
        dy = low
    elif dy > high:
        dy = high
    return dy


def main():
    player, pipes = start_game()
    np.random.seed(1)
    pipe_speed = -2
    gravity = 3
    flapping_max = -25
    dy = 0
    while True:
        for pipe in pipes:
            if pipe.collision(player):
                print(player.score)
                main()  # RESTART
        draw(player, pipes)
        player.increase_score(0.1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.set_flapping()

        if player.flapping:
            flapping_speed = flapping_max
        else:
            flapping_speed = 0

        dy += gravity + flapping_speed
        dy = bound_delta_y(dy, flapping_max, gravity)
        player.flap(dy)

        pipes, player_passed_pipe = clean_and_move_pipes(pipes, pipe_speed)
        if player_passed_pipe:
            player.increase_score(10)

        pipes = new_pipe(WIDTH/3, pipes)

        pygame.display.flip()
        clock.tick(60)
        player.flapping = False


main()
