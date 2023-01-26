import pygame
import sys
import os
import time
import random
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
ppo_pos = False
flag = 0
cross = (-1000, -1000)
font = pygame.font.SysFont('Calibri', 30)


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
    image_strela = load_image("strela.png")
    image_boom = load_image("boom.png")

    def __init__(self, *args):
        super().__init__(all_sprites)
        global cross
        self.image = PPO.image
        self.rect = self.image.get_rect()

    def update(self, *args):
        global sbito
        global health
        global popadania
        global prohodov
        self.rect.centerx = cross[0]
        self.rect.centery = cross[1]
        self.prospeed = 3
        if not pygame.sprite.collide_mask(self, rocket):
            self.rect.y -= self.prospeed
            self.rect.x += self.prospeed // 2
        if prohodov == 10:
            self.kill()


protivorocket = PPO()


class BTR(pygame.sprite.Sprite):
    image = load_image("btr.png")
    image_boom = load_image("boom.png")

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
        global popadania
        self.rect.x -= speed
        self.coords = self.rect.x, self.rect.y
        if speed == 0:
            if health != 0:
                self.rect.right = width
                self.rect.y = 532
                speed = 2
            else:
                self.rect.x = 10000
                self.rect.y = 10000
                self.kill()
                print('tested')
        if self.rect.left <= 0:
            self.rect.right = width
            prohodov += 1
            print(prohodov)
            if prohodov == 10:
                self.kill()
        if pygame.sprite.collide_mask(self, protivorocket):
            health -= 10
            print('НЕ СТРЕЛЯЙ ПО СВОИМ!') 
            popadania += 1
            speed = 0


btr = BTR()


class PVOSys(pygame.sprite.Sprite):
    image = load_image("ppo.png")
    image_boom = load_image("boom.png")

    def __init__(self):
        super().__init__(all_sprites)
        self.image = PVOSys.image
        self.rect = self.image.get_rect()
        self.rect.x = width // 2
        self.rect.y = 532
        self.rect.bottom = height
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        global health
        global flag
        global popadania
        global ppo_pos
        if health != 0 and prohodov != 10:
            if flag == -1:
                self.rect.x -= 1
            elif flag == 1:
                self.rect.x += 1
            if self.rect.left <= 0:
                health = 0
                ppo_pos = True
            if self.rect.right >= width:
                health = 0
                ppo_pos = True
        else:
            self.rect.x = 10000
            self.rect.y = 10000
            self.kill()
        if pygame.sprite.collide_mask(self, protivorocket):
            print('НЕ СТРЕЛЯЙ ПО СВОИМ!')
            health = 0


pvo = PVOSys()


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
        global health
        global sbito
        global speed
        global popadania
        global pvo_alive
        if self.ab > 0:
            self.bombspeed = 8
        else:
            self.bombspeed = 4
        if not pygame.sprite.collide_mask(self, btr):
            self.rect.y += self.bombspeed
            if self.rect.bottom == height:
                self.image = self.image_boom
            if self.ab > 0:
                self.rect.x += self.bombspeed // 2
            if pygame.sprite.collide_mask(self, pvo):
                self.image = self.image_boom
                health = 0
                pvo_alive = 0
                speed = 0
                popadania += 1
            if pygame.sprite.collide_mask(self, protivorocket):
                self.image = self.image_boom
                sbito += 1
                self.kill()
        else:
            self.image = self.image_boom
            speed = 0
            health -= 10
            popadania += 1
            print(health, 'marker')


rocket = Missles()


def main():
    timed = (1, 20, 97, 444, 413, 876, 150, 200, 999)
    pygame.display.set_caption("SkyDefenders 0.2 Open Alpha")
    screen.blit(afghan, (0, 0))
    running = True
    global health
    global cross
    global prohodov
    global sbito
    global flag
    global popadania
    while running:
        if health != 0:
            if prohodov != 10:
                a = random.randint(0, 1000)
                if a in timed:
                    Missles()
        if popadania > 10:
            popadania = 10
        clock.tick(FPS)
        screen.blit(afghan, (0, 0))
        all_sprites.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    flag = -1
                if event.key == pygame.K_RIGHT:
                    flag = 1
                if event.key == pygame.K_DOWN:
                    flag = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                cross = event.pos
        all_sprites.update()
        popad = font.render(f'Попаданий: {popadania}', False, (0, 0, 0))
        sbit = font.render(f'Сбито: {sbito}', False, (0, 0, 0))
        uspeh = font.render(f'Успешно: {prohodov}', False, (0, 0, 0))
        finalpopad = font.render(f'Вы проиграли! Попаданий: {popadania}', False, (0, 0, 0))
        zrada = font.render('А кто Родину защищать будет?', False, (255, 0, 0))
        victory = font.render(f'Вы выиграли!', False, (0, 0, 0))
        if health > 0 and prohodov != 10:
            screen.blit(popad, (0, 0))
            screen.blit(sbit, (0, 25))
            screen.blit(uspeh, (0, 50))
        elif health <= 0 and prohodov != 10:
            screen.blit(finalpopad, (width // 4, height // 2))
        if prohodov == 10:
            screen.blit(victory, (screen.get_rect().centerx, screen.get_rect().centery))
            screen.blit(popad, (width // 4, height // 2 + 25))
            screen.blit(sbit, (width // 4, height // 2 + 50))
        if ppo_pos == True:
            screen.blit(zrada, (width // 4, 100))
        pygame.display.flip()
    pygame.quit()
    print(sbito)


if __name__ == '__main__':
    sys.exit(main())
