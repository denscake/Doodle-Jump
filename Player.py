import pygame
import time

from Base import Base


class Player(Base):

    def __init__(self, *groups, resolution):

        pygame.init()

        self.jmp_sound = pygame.mixer.Sound('sound/jmp.wav')

        super().__init__(*groups, img_path='img/Player.png', resolution=resolution)
        self.pos[1] = self.resolution[1] - self.size[1] * 3
        self.pos[0] = (self.resolution[0] - self.size[0]) / 2
        self.alive = True
        self.cur_score = 0
        self.powerup_x2 = 0
        self.powerup_x3 = 0
        self.powerup_j = 0

    def score(self, value):
        self.cur_score += value
        return self.cur_score

    def update(self, *args):
        self.go()
        self.speed[1] += int(self.size[1] * 5 * self.dt)

        if self.rect.right > self.resolution[0]:
            self.pos[0] = self.resolution[0] - self.size[1]
        if self.rect.left < 0:
            self.pos[0] = 0
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) \
                and not (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            self.speed[0] = -self.size[0] * 2

        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) \
                and not (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            self.speed[0] = self.size[0] * 2
        else:
            self.speed[0] = 0

    def checkHit(self, obj):
        type_of_sprite = obj.__class__.__name__

        if type_of_sprite == "Lava":
            if self.rect.bottom > obj.get_y():  # if below the surface of Lava
                return True

        elif type_of_sprite == "Platform":
            if self.rect.left < obj.pos[0] + obj.width:
                # if left bound is on the left of the right bound of the platform
                if self.rect.right > obj.pos[0]:  # if right bound is on the right of the left bound of the platform
                    if self.rect.bottom > obj.pos[1]:  # if below of the surface of the platform
                        if self.rect.bottom - self.speed[1] * (self.dt*2) < obj.pos[1]:  # but frame ago was above
                            self.speed[1] = -self.size[1] * 6 * (1 + (self.powerup_j > time.time()))  # jump
                            self.jmp_sound.play()

                            self.score(obj.reward() *
                                       (1 + (self.powerup_x2 > time.time())) *
                                       (1 + 2 * (self.powerup_x3 > time.time())))
                            # multiply reward according to multipliers

                            if 7 < obj.type < 10:
                                obj.alive = False  # break yellow platform
                            elif obj.type > 9:
                                self.alive = False  # die if red platform
                                return True
        return False
