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
FLOOR = 730
DRAW_LINES = True
gen = 1

win = pygame.display.set_mode((WIDTH_WINDOW, HEIGHT_WINDOW))

BACKGROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("statics/img", "background-night.png")))
SCORE_FONT = pygame.font.SysFont("comicsans", 40)


def draw_window(birds, pipes, base, score, gen, pipe_ind):
    """
    draws the windows for the main game loop
    :param win: pygame window surface
    :param bird: a Bird object
    :param pipes: List of pipes
    :param score: score of the game (int)
    :param gen: current generation
    :param pipe_ind: index of closest pipe
    :return: None
    """
    global win
    win.blit(BACKGROUND_IMAGE, (0,0))

    for pipe in pipes:
        pipe.draw(win)

    base.draw(win)
    for bird in birds:
        # draw lines from bird to pipe
        if DRAW_LINES:
            try:
                pygame.draw.line(win, (255,0,0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_TOP.get_width()/2, pipes[pipe_ind].height), 5)
                pygame.draw.line(win, (255,0,0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_BOTTOM.get_width()/2, pipes[pipe_ind].bottom), 5)
            except:
                pass
        bird.draw(win)

    # score
    score_label = SCORE_FONT.render("Puntuacion " + str(score),1,(255,255,255))
    win.blit(score_label, (WIDTH_WINDOW - score_label.get_width() - 15, 10))

    # generations
    score_label = SCORE_FONT.render("Generacion: " + str(gen-1),1,(255,255,255))
    win.blit(score_label, (10, 10))

    # alive
    score_label = SCORE_FONT.render("Vivos: " + str(len(birds)),1,(255,255,255))
    win.blit(score_label, (10, 50))

    pygame.display.update()


def eval_genome(genomes, config):
    nets = []
    ge = []
    birds = []
    global gen
    gen += 1

    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(230,350))
        ge.append(genome)

    base = Base(FLOOR)
    pipes = [Pipe(700)]
    score = 0

    clock = pygame.time.Clock()

    run = True
    while run and len(birds) > 0:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():  # determine whether to use the first or second
                pipe_ind = 1

        for x, bird in enumerate(birds):
            ge[x].fitness += 0.1
            bird.move()
            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                bird.jump()



        rem = []
        add_pipe = False
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird) or bird.y + bird.img.get_height() >= 750 or bird.y < 0:
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(700))

        for r in rem:
            pipes.remove(r)

        draw_window(birds, pipes, base, score, gen, pipe_ind)


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_file)
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())
    winner = population.run(eval_genome, 50)
    print('\nMejor genoma:\n{!s}'.format(winner))


if __name__ == "__main__":
    local_directory = os.path.dirname(__file__)
    config_path = os.path.join(local_directory, "config-neat.txt")
    run(config_path)