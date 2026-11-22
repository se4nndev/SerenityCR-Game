import pygame
from pygame.locals import *

largura_tela = 700
altura_tela = 750
class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("imagens/serenity-nave.png").convert_alpha() #convert_alpha mantém o fundo transparente (png)
        self.image = pygame.transform.scale(self.image, (100, 100))

        self.rect = self.image.get_rect()
        self.rect.midbottom = (largura_tela // 2, altura_tela - 20)

        self.velocidade = 13 #velocidade da nave
        self.vidas = 3
    
    def update(self):
        tecla_pressionada = pygame.key.get_pressed()

        if tecla_pressionada[K_LEFT] or tecla_pressionada[K_a]:
            self.rect.x = self.rect.x - self.velocidade

        if tecla_pressionada[K_RIGHT] or tecla_pressionada[K_d]:
            self.rect.x = self.rect.x + self.velocidade

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > largura_tela:
            self.rect.right = largura_tela