import pygame

pygame.init()

largura_tela = 600
altura_tela = 750

ultimo_tiro = 0
intervalo_tiro = 350

pontuacao = 0
proxima_vida = 5000

fonte = pygame.font.Font("fonte/Orbitron.ttf", 35)
fonte_grande = pygame.font.Font("fonte/Orbitron.ttf", 60)