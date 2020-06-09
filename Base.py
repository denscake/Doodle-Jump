import pygame
import time


class Base(pygame.sprite.Sprite):
    def __init__(self, *groups, img_path, resolution):
        super().__init__(*groups)
        self.dt = 0
        self.size = (96, 96)
        self.image = pygame.Surface(self.size, pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.picture = pygame.image.load(img_path).convert_alpha()
        self.picture.set_colorkey((0, 0, 0))
        self.picture = pygame.transform.scale(self.picture, self.size)
        self.image.blit(self.picture, (0, 0))
        self.pos = [0, 0]
        self.speed = [0, 0]
        self.time = time.time()
        self.resolution = resolution

    def go(self, *args, **kwargs):
        self.dt = time.time() - self.time
        self.time = time.time()

        self.pos = [self.pos[0] + self.speed[0] * self.dt,
                    self.pos[1] + self.speed[1] * self.dt]

        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]


    def draw(self, *args, **kwargs):
        pass

    def checkHit(self, *args, **kwargs):
        pass

    def move(self, *args, **kwargs):
        pass
