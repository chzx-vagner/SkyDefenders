import pygame
import sys
import os
import time
import random

# НА ДАННЫЙ МОМЕНТ, ПОКА НЕ РЕАЛИЗОВАНО ПВО, ТЕХНИКА УКРАИНСКАЯ, ПОТОМУ ЧТО МНЕ НЕ ХОЧЕТСЯ БОМБИТЬ НАШИХ

pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
speed = 2
FPS = 60
sbito = 0
health = 100
prohodov = 0
popadania = 0
s = (-1000, -1000)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


afghan = load_image('afghan.png')
all_sprites = pygame.sprite.Group()


class PPO(pygame.sprite.Sprite):
    image = load_image("cross.png")
    image_boom = load_image("boom.png")

    def __init__(self, *args):
        super().__init__(all_sprites)
        global s
        self.image = PPO.image
        self.rect = self.image.get_rect()
        print(s)

    def update(self, *args):
        global sbito
        global health
        global popadania
        global prohodov

        self.rect.centerx = s[0]
        self.rect.centery = s[1]
        self.prospeed = 3
        self.rect.y -= self.prospeed
        if not pygame.sprite.collide_mask(self, rocket):
            self.rect.y -= self.prospeed
            self.rect.x += self.prospeed // 2
        if prohodov == 10:
            self.kill()


protivorocket = PPO()


class PPOrocket(pygame.sprite.Sprite):
    image = load_image("missle.png")
    image_boom = load_image("boom.png")

    def __init__(self, *args):
        super().__init__(all_sprites)
        global s
        self.image = PPOrocket.image
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.bottom = height
        print(s, 'dddd')

    def update(self, *args):
        self.prospeed = 3
        self.rect.y += self.prospeed
        if not pygame.sprite.collide_mask(self, rocket):
            self.rect.y += self.prospeed
            self.rect.x += self.prospeed // 2
        else:
            self.image = self.image_boom
            print(health, 'PPO PRUZUE!')
        if prohodov == 10:
            self.kill()


pporocket = PPOrocket()


class BTR(pygame.sprite.Sprite):
    image = load_image("btr.png")

    def __init__(self):
        super().__init__(all_sprites)
        self.image = BTR.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width)
        self.rect.y = 532
        self.rect.bottom = height
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        global health
        global speed
        global prohodov
        self.rect.x -= speed
        self.coords = self.rect.x, self.rect.y
        if speed == 0:
            if health != 0:
                self.rect.right = width
                self.rect.y = 532
                speed = 2
            else:
                self.rect.x = 1000
                self.rect.y = 1000
        if self.rect.left <= 0:
            self.rect.right = width
            prohodov += 1
            print(prohodov)
            if prohodov == 10:
                self.kill()


btr = BTR()


class Missles(pygame.sprite.Sprite):
    image = load_image("missle.png")
    image_bomb = load_image('bomb.png')
    image_boom = load_image('boom.png')

    def __init__(self):
        super().__init__(all_sprites)
        self.ab = random.randint(-2, 2)
        if self.ab > 0:
            self.image = Missles.image
        else:
            self.image = Missles.image_bomb
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = random.randint(0, 704)
        self.rect.y = 0

    def update(self):
        global speed
        global health
        global popadania
        if self.ab > 0:
            self.bombspeed = 8
        else:
            self.bombspeed = 4
        if not pygame.sprite.collide_mask(self, btr):
            self.rect.y += self.bombspeed
            if self.ab > 0:
                self.rect.x += self.bombspeed // 2
            if pygame.sprite.collide_mask(self, protivorocket):
                self.image = self.image_boom
                self.rect.y = 10000
                self.rect.x = 10000
                self.kill()
        else:
            self.image = self.image_boom
            speed = 0
            health -= 10
            popadania += 1
            print(health, 'marker')


rocket = Missles()


def draw(screen):
    print('eeeee')
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render('Попаданий: ' + str(popadania), True, (100, 255, 100))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)


def main():
    timed = (1, 150, 200, 999, 580, 600, 320)
    pygame.display.set_caption("SkyDefenders 0.0.0.0.1")
    screen.blit(afghan, (0, 0))
    running = True
    global health
    global s
    global prohodov
    while running:
        if health != 0:
            if prohodov != 10:
                a = random.randint(0, 1000)
                '''print(a)'''
                if a in timed:
                    Missles()
            else:
                draw(screen)
        clock.tick(FPS)
        screen.blit(afghan, (0, 0))
        all_sprites.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                s = event.pos
                print(s)
        all_sprites.update()
        pygame.display.flip()
    pygame.quit()
    print(sbito)
    print(health, 'markerrr')


if __name__ == '__main__':
    sys.exit(main())