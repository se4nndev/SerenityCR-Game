import pygame
from pygame.locals import *
import random

largura_tela = 600
altura_tela = 750
class Asteroide(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        asteroide1 = pygame.image.load("imagens/asteroide-sprite1.png").convert_alpha()
        asteroide2 = pygame.image.load("imagens/asteroide-sprite2.png").convert_alpha()
        asteroide3 = pygame.image.load("imagens/asteroide-sprite3.png").convert_alpha()
        asteroide4 = pygame.image.load("imagens/asteroide-sprite4.png").convert_alpha()

        asteroide1 = pygame.transform.scale(asteroide1, (150, 150))
        asteroide2 = pygame.transform.scale(asteroide2, (150, 150))
        asteroide3 = pygame.transform.scale(asteroide3, (150, 150))
        asteroide4 = pygame.transform.scale(asteroide4, (150, 150))

        self.sprites = [asteroide1, asteroide2, asteroide3, asteroide4]
        #-------
        self.indice = 0
        self.image = self.sprites[self.indice]

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, largura_tela - self.rect.width)
        self.rect.bottom = 0

        self.velocidade = random.randint(2, 5)
        #-------

    def update(self):
        self.rect.y = self.rect.y + self.velocidade
        #-------
        self.indice += 0.15
        if self.indice >= len(self.sprites):
            self.indice = 0
        self.image = self.sprites[int(self.indice)]
        #-------