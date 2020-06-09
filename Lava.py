import pygame


from Base import Base


class Lava(Base):
    def __init__(self, resolution):
        super().__init__(img_path='img/Base.png', resolution=resolution)
        self.speed[1] = -40  # set vertical speed
        self.pos[1] = self.resolution[1] - 30  # set start height

    def draw(self, surface):  # draw rectangle that represents lava
        pygame.draw.rect(surface, (230, 50, 50), (0, self.pos[1], self.resolution[1], self.resolution[1] - self.pos[1]))

    def get_y(self):  # for collision check
        return self.pos[1]
