import pygame
import sys
import os
import time
import random

# НА ДАННЫЙ МОМЕНТ, ПОКА НЕ РЕАЛИЗОВАНО ПВО, ТЕХНИКА УКРАИНСКАЯ, ПОТОМУ ЧТО МНЕ НЕ ХОЧЕТСЯ БОМБИТЬ НАШИХ

pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
'''screen.fill(pygame.Color('white'))'''
clock = pygame.time.Clock()
speed = 2
FPS = 60
sbito = 0
health = 100
prohodov = 0
popadania = 0
s = (0, 0)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


all_sprites = pygame.sprite.Group()


class PPO(pygame.sprite.Sprite):
    image = load_image("bomb.png")
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
        self.rect.x = s[0]
        self.rect.y = s[1]
        self.prospeed = 3
        self.rect.y -= self.prospeed
        if not pygame.sprite.collide_mask(self, rocket):
            self.rect.y -= self.prospeed
            self.rect.x += self.prospeed // 2
        else:
            self.image = self.image_boom
            self.rect.y = 10000
            self.rect.x = 10000
            print(health, 'PPO PRUZUE!')
        if prohodov == 10:
            self.kill()


protivorocket = PPO()


class BTR(pygame.sprite.Sprite):
    image = load_image("btr.png")

    def __init__(self):
        super().__init__(all_sprites)
        self.image = BTR.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(800)
        self.rect.y = 532
        self.rect.bottom = 600
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
    image_boom = load_image('boom.png')

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Missles.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = random.randint(0, 704)
        self.rect.y = 0

    def update(self):
        global speed
        global health
        global popadania
        self.bombspeed = 6
        if not pygame.sprite.collide_mask(self, btr):
            self.rect.y += self.bombspeed
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


'''class Landing(pygame.sprite.Sprite):
    image = load_image("missle.png")
    image_boom = load_image('boom.png')

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = Landing.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        bombspeed = 3
        if self.rect.y >= 600:
            self.image = self.image_boom
        if not pygame.sprite.collide_mask(self, mountain):
            self.rect.y += bombspeed
        else:
            self.image = self.image_boom
            global speed
            speed = 0'''


print(all_sprites)


'''class Boom(pygame.sprite.Sprite):
    image = load_image("boom.png")

    def __init__(self, group, *args):
        super().__init__(group)
        self.image = Boom.image
        self.rect = self.image.get_rect()
        self.rect.x = args[0]
        print(args[0])
        self.rect.y = args[1]'''


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
        screen.fill(pygame.Color('white'))
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