import pygame
from src.game.common import blitRotateCenter
import os

BIRD_IMAGES = [pygame.transform.scale2x(pygame.image.load(os.path.join("statics/img", "bird1.png"))),
               pygame.transform.scale2x(pygame.image.load(os.path.join("statics/img", "bird2.png"))),
               pygame.transform.scale2x(pygame.image.load(os.path.join("statics/img", "bird3.png")))]


class Bird:
    IMAGES = BIRD_IMAGES
    MAX_ROTATION = 25
    ROT_VELOCITY = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_from_jump = 0
        self.velocity = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMAGES[0]

    def jump(self):
        self.velocity = -10.5
        self.tick_from_jump = 0
        self.height = self.y

    def move(self):
        self.tick_from_jump += 1
        displacement = self.velocity * self.tick_from_jump + 1.5 * self.tick_from_jump ** 2    # Hace un arco
        # -9,-6.5... hasta 0 (El pajaro sube) desde 0 hacia los positivos (El pajaro cae)
        if displacement >= 16:
            displacement = 16     # REDUCTOR VELOCIDAD HACIA ABAJO
        elif displacement < 0:
            displacement -= 2.2    # Si nos movemos hacia arriba desplacemonos mas
        self.y += displacement
        if displacement < 0 or self.y < self.height + 50:  # tilt up
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:  # tilt down
            if self.tilt > -90:
                self.tilt -= self.ROT_VELOCITY

    def draw(self, win):
        self.img_count += 1
        # Cambiamos la imagen
        # For animation of bird, loop through three images
        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.IMAGES[0]
        elif self.img_count <= self.ANIMATION_TIME*2:
            self.img = self.IMAGES[1]
        elif self.img_count <= self.ANIMATION_TIME*3:
            self.img = self.IMAGES[2]
        elif self.img_count <= self.ANIMATION_TIME*4:
            self.img = self.IMAGES[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMAGES[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMAGES[1]
            self.img_count = self.ANIMATION_TIME * 2

        blitRotateCenter(win, self.img, (self.x, self.y), self.tilt)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)