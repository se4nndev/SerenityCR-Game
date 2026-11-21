import pygame
from pygame.locals import *
from sys import exit
from scripts.jogador import Jogador
from scripts.tirolaser import Laser

pygame.init()

largura_tela = 850
altura_tela = 750

icone = pygame.image.load("imagens/asteroide-sprite1.png")
pygame.display.set_icon(icone)

tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Serenity: Cosmic Rain")
relogio = pygame.time.Clock()

plano_fundo = pygame.image.load("imagens/fundo-espacial.png").convert()
plano_fundo = pygame.transform.scale(plano_fundo, (largura_tela, altura_tela))
movimentacao_fundo = 0
velocidade_fundo = 2

jogador = Jogador()
grupo_lasers = pygame.sprite.Group() 

while True:
    relogio.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT: #aperte sair pra sair KKKKKKKKKKKKKKK
            pygame.quit()
            exit()
        
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: #aperte esc pra sair
                pygame.quit() 
                exit()

            if event.key == K_SPACE:
                laser = Laser(jogador.rect.centerx, jogador.rect.top + 10) #...
                grupo_lasers.add(laser) #...
    
    jogador.update()
    grupo_lasers.update()

    movimentacao_fundo = movimentacao_fundo + velocidade_fundo
    if movimentacao_fundo >= altura_tela:
        movimentacao_fundo = 0

    tela.blit(plano_fundo, (0, movimentacao_fundo))
    tela.blit(plano_fundo, (0, movimentacao_fundo - altura_tela))
    grupo_lasers.draw(tela)
    tela.blit(jogador.image, jogador.rect) #desenha a nave

    pygame.display.flip()