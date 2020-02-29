import pygame
import random
import os
import neat
import time

from src.game.base import Base
from src.game.bird import Bird
from src.game.pipe import Pipe

pygame.font.init()

WIDTH_WINDOW = 500
HEIGHT_WINDOW = 800

BACKGROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("statics/img", "background-night.png")))
SCORE_FONT = pygame.font.SysFont("comicsans", 50)


def draw_window(window, bird, pipes, base, score):
    window.blit(BACKGROUND_IMAGE, (0,0))
    for pipe in pipes:
        pipe.draw(window)

    text = SCORE_FONT.render("Puntuacion: " + str(score), 1, (255, 255, 255))
    window.blit(text, (WIDTH_WINDOW - 10 - text.get_width(), 10))
    base.draw(window)
    bird.draw(window)
    pygame.display.update()


def main():
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(700)]
    win = pygame.display.set_mode((WIDTH_WINDOW, HEIGHT_WINDOW))
    run = True
    score = 0
    clock = pygame.time.Clock()
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        #bird.move()
        rem = []
        add_pipe = False
        for pipe in pipes:
            if pipe.collide(bird):
                pass #TODO gameover
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
            pipe.move()

        if add_pipe:
            score += 1
            pipes.append(Pipe(700))

        for r in rem:
            pipes.remove(r)

        if bird.y + bird.img.get_height() >= 750:
            pass
        draw_window(win, bird, pipes, base, score)
    pygame.quit()
    quit()

main()