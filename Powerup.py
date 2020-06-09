from Base import Base
import random
import time


class Powerup(Base):

    def __init__(self, resolution, platforms):
        self.type = random.randrange(0, 3)
        paths = ["img/x2.png", "img/x3.png", "img/jump.png"]

        super().__init__(img_path=paths[self.type], resolution=resolution)
        self.length = random.randrange(7, 25)
        self.activated = False
        self.alive = True
        self.act_time = 0
        self.width = self.size[0]
        self.wobble = 0
        if len(platforms):
            last_platform = platforms[len(platforms) - 1]
            self.pos[1] = last_platform.pos[1] - self.size[1] * 1.5
            self.pos[0] = last_platform.pos[0] + last_platform.width / 2 - self.size[1] / 2
            self.speed[0] = last_platform.speed[0]
            self.wobble = last_platform.wobble
        else:
            self.alive = False

    def activated(self):
        self.activated = True
        self.act_time = time.time()

    def go(self):
        super().go()
        if self.pos[0] < -self.width / 2:
            self.speed[0] = self.wobble

        if self.pos[0] > self.resolution[0] - self.width / 2:
            self.speed[0] = -self.wobble

    def update(self, *args):
        self.go()
        if self.pos[1] > self.resolution[1]:
            self.alive = False
