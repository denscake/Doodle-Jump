import pygame
import random
import time

from Player import Player
from Lava import Lava
from Platform import Platform
from Powerup import Powerup

pygame.init()

RESOLUTION = (480, 768)  # width and height of the window
FRAMERATE = 60  # framerate of the game

screen = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption('TBD')

running = True  # if game is running
clock = pygame.time.Clock()

bg_color = (96, 96, 96)

pygame.font.init()

score_font = pygame.font.SysFont('Bauhaus 93', 36)
high_score_font = pygame.font.SysFont('Bauhaus 93', 24)

player_sprite = pygame.sprite.Group()
lava = Lava(resolution=RESOLUTION)
player = Player(resolution=RESOLUTION)
player_sprite.add(player)
platforms = []
powerups = pygame.sprite.Group()
cnt = 0

reset = False

highscore = 0

ded_sound = pygame.mixer.Sound('sound/ded.wav')

pup_sound = pygame.mixer.Sound('sound/pup.wav')


def game_mechanics():
    if player.pos[1] < player.size[1]*2:
        lava.pos[1] += player.size[1]*2 - player.pos[1]
        if lava.pos[1] > RESOLUTION[1]:
            lava.pos[1] = RESOLUTION[1]

        for pl in platforms:
            pl.pos[1] += player.size[1]*2 - player.pos[1]

        for pu in powerups:
            pu.pos[1] += player.size[1]*2 - player.pos[1]

        player.pos[1] = player.size[1]*2

    for pl in platforms:
        if player.checkHit(pl):
            return True

    collisions = pygame.sprite.groupcollide(player_sprite, powerups, False, True)

    if collisions:
        for pups in collisions.values():
            powerup = pups[0]
            exp_time = time.time() + powerup.length
            if powerup.type == 0:
                player.powerup_x2 = exp_time
            elif powerup.type == 1:
                player.powerup_x3 = exp_time
            else:
                player.powerup_j = exp_time
            pup_sound.play()

    if not cnt % 5:  # just check once in a while
        if len(platforms) < 8:  # 5 is not enough
            platforms.append(Platform(RESOLUTION, platforms, player.score(0)))
            if not random.randrange(0, 32):
                powerup = Powerup(resolution=RESOLUTION, platforms=platforms)
                powerups.add(powerup)  # sometimes add powerups

        for pl in platforms:
            if pl.pos[1] > RESOLUTION[1]:
                pl.alive = False  # old platforms must be deleted

        for i in range(len(platforms) - 1, 0, -1):
            if not platforms[i].alive:
                platforms.pop(i)  # delete old platforms

        for pup in powerups.copy():
            if not pup.alive:
                powerups.remove(pup)
    return False


while running:
    if reset:
        ded_sound.play()
        if player.score(0) > highscore:
            highscore = player.score(0)
        reset = False
        score_font = pygame.font.SysFont('Bauhaus 93', 36)
        player_sprite = pygame.sprite.Group()
        lava = Lava(resolution=RESOLUTION)
        player = Player(resolution=RESOLUTION)
        player_sprite.add(player)
        platforms = []
        powerups = pygame.sprite.Group()
        cnt = 0

    clock.tick(FRAMERATE)
    cnt += 1

    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = False

    player_sprite.update()
    screen.fill(bg_color)

    reset = player.checkHit(lava)

    reset += game_mechanics()

    for platform in platforms:
        platform.go()
        platform.draw(screen)

    powerups.update()
    powerups.draw(screen)

    player_sprite.draw(screen)
    lava.go()
    lava.draw(screen)

    score_string = "Score: " + str(player.score(0))
    score_surface = score_font.render(score_string, True, (255, 255, 255))
    screen.blit(score_surface, (20, 20))

    high_score_string = "Highscore: " + str(highscore)
    high_score_surface = high_score_font.render(high_score_string, True, (255, 255, 255))
    screen.blit(high_score_surface, (20, 55))

    pygame.display.flip()
