import random

import pygame

from Base import Base


class Platform(Base):
    def __init__(self, resolution, platforms, score):
        super().__init__(img_path='img/Base.png', resolution=resolution)
        self.type = random.randrange(0, 11)  # 0-7 normal, 8-9 fake, 10 explosive
        self.wobble = 0

        if score < 10:  # limit difficulty at lower scores
            self.type = 0
        elif score < 15 and self.type > 9:
            self.type = 9
        elif score < 30 and self.type < 9:
            self.wobble = self.size[0] / 4
        elif score < 50 and self.type < 9:
            self.wobble = self.size[0] / 3
        elif score < 70 and self.type < 9:
            self.wobble = self.size[0] / 2
        elif self.type < 9:
            self.wobble = self.size[0]

        self.speed[0] = self.wobble * random.randrange(-1, 1, 2)

        if self.type < 10:
            self.width = self.size[1] * 1.5  # 1.5 times wider than player
        else:
            self.width = self.size[1]  # red  platforms are 2/3 as wide because they are OP
        self.pos[0] = random.randrange(-self.width / 2,
                                       resolution[0] - self.width / 2)  # placed somewhere in the frame above
        self.alive = True
        self.points = 1
        if len(platforms):

            if platforms[len(platforms) - 1].type > 9 and self.type > 9:
                self.type = 9  # two red platforms in a row is kinda unfair

            if self.type < 10:
                self.pos[1] = platforms[len(platforms) - 1].pos[1] - self.size[1] * random.randrange(2,
                                                                                                     4) * 0.8  # place high up
            else:
                self.pos[1] = platforms[len(platforms) - 1].pos[1] - self.size[1] * random.randrange(1, 2)
                self.points = 0

                # dangerous platforms spawned litthe bit lower
        else:
            self.type = 0  # define the first platform spawned so you not die on spawn
            self.pos[0] = 0
            self.pos[1] = self.resolution[1] - self.size[1] * 1.5
            self.width = self.resolution[0]
            self.points = 0

    def draw(self, surface):

        if self.type < 8:
            color = (50, 210, 50)  # green
        elif self.type < 10:
            color = (180, 180, 50)  # yellow
        else:
            color = (180, 50, 50)  # red

        pygame.draw.rect(surface, color, (self.pos[0], self.pos[1], self.width, self.size[0] / 5))

    def go(self):
        super().go()
        if self.pos[0] < -self.width / 2:
            self.speed[0] = self.wobble

        if self.pos[0] > self.resolution[0] - self.width / 2:
            self.speed[0] = -self.wobble


    def reward(self):
        points = self.points
        self.points = 0
        return points
