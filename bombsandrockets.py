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
health = 100


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


all_sprites = pygame.sprite.Group()

'''class Bomb(pygame.sprite.Sprite): старая версия кода, потом уберу
    image = load_image("bomb.png")
    image_missle = load_image("missle.png")
    image_boom = load_image("boom.png")
    for n in range(1):
        where = random.randint(-2, 2)
        print(where)

    def __init__(self, group, *args):
        super().__init__(group)
        if self.where > 0:
            self.image = Bomb.image
            self.rect = self.image.get_rect()
            self.rect.x = random.randint(0, 800)
            self.rect.y = random.randint(10, 200)
            print(self.rect)
        else:
            self.image = Bomb.image_missle
            self.rect = self.image.get_rect()
            self.rect.x = random.randint(0, 800)
            self.rect.y = random.randint(10, 200)
            print(self.rect)

    def update(self, *args):
        global sbito
        global popadania

        if self.where > 0:
            self.rect.y += 2
        else:
            self.rect.y += 5
            self.rect.x += 10
        if self.rect.left > width:
            self.rect.right = 0
        if self.rect.right > width:
            self.rect.right = 0
        if self.rect.y > height:
            popadania += 1
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            sbito += 1
            self.v = self.rect.x
            self.z = self.rect.y
            self.kill()
            Boom(all_sprites, self.v, self.z)'''


class BTR(pygame.sprite.Sprite):
    image = load_image("svin.png")

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
        bombspeed = 3
        if not pygame.sprite.collide_mask(self, btr):
            self.rect.y += bombspeed
        else:
            self.image = self.image_boom
            speed = 0
            health -= 10
            print(health, 'marker')



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


def main():
    timed = (1, 150, 200, 999, 580, 600, 320)
    pygame.display.set_caption("SkyDefenders 0.0.0.0.1")
    running = True
    while running:
        a = random.randint(0, 1000)
        '''print(a)'''
        if a in timed:
            Missles()
        clock.tick(FPS)
        screen.fill(pygame.Color('white'))
        all_sprites.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
        all_sprites.update()
        pygame.display.flip()
    pygame.quit()
    print(sbito)
    print(health, 'markerrr')


if __name__ == '__main__':
    sys.exit(main())