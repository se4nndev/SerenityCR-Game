import pygame
from pygame.locals import *

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("imagens/laser-serenity.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (35, 45)) #redimensiona o tamanho do laser

        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y) #faz o tiro nascer na posição que o main.py mandar #...

        self.velocidade = 10 #velocidade do laser disparado 

    def update(self):
        self.rect.y = self.rect.y - self.velocidade

        if self.rect.bottom < 0: #...
            self.kill()