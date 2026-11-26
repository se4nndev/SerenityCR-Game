import pygame
import random

class AsteroideChefe(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.image = pygame.image.load(
            "imagens/asteroide-sprite4.png"
        ).convert_alpha()

        self.image = pygame.transform.scale(
            self.image,
            (500, 350)
        )

        self.rect = self.image.get_rect()

        self.rect.centerx = 300
        self.rect.bottom = 0

        self.vida = random.randint(7, 10)
        self.vida_max = self.vida
        self.velocidade = 1

    def update(self):

        self.rect.y += self.velocidade