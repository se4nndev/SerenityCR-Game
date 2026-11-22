import pygame
from pygame.locals import *
from sys import exit
from scripts.jogador import Jogador
from scripts.tirolaser import Laser
from scripts.asteroide import Asteroide
import random

pygame.init()

fonte = pygame.font.Font("fonte/Orbitron.ttf", 35)
fonte_grande = pygame.font.Font("fonte/Orbitron.ttf", 60)

largura_tela = 700
altura_tela = 750

som_laser = pygame.mixer.Sound("sons/tiro-laser.wav")
som_laser.set_volume(0.9)

ultimo_tiro = 0
intervalo_tiro = 350

som_explosao = pygame.mixer.Sound("sons/explosao-asteroide.wav")
som_explosao.set_volume(0.65)

som_game_over = pygame.mixer.Sound("sons/game-over.wav")
som_game_over.set_volume(0.7)

tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Serenity: Cosmic Rain")
relogio = pygame.time.Clock()

imagem_explosao = pygame.image.load("imagens/explosao-asteroide.png").convert_alpha()
imagem_explosao = pygame.transform.scale(imagem_explosao, (135, 135))
explosoes = []

plano_fundo = pygame.image.load("imagens/fundo-espacial.png").convert()
plano_fundo = pygame.transform.scale(plano_fundo, (largura_tela, altura_tela))
movimentacao_fundo = 0
velocidade_fundo = 1

musicas = ["sons/musica-jogo-agitacao.wav", "sons/musica-jogo-vibes.wav", "sons/musica-jogo-tensa.wav"]
musica_atual = 0
FIM_MUSICA = USEREVENT + 2

pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.set_endevent(FIM_MUSICA)
pygame.mixer.music.load(musicas[musica_atual])
pygame.mixer.music.play()

jogador = Jogador()
grupo_lasers = pygame.sprite.Group()
grupo_asteroides = pygame.sprite.Group()
CRIAR_ASTEROIDE = USEREVENT + 1
pygame.time.set_timer(CRIAR_ASTEROIDE, 600)

pontuacao = 0
proxima_vida = 5000
estado = "jogando"

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
                tempo_atual = pygame.time.get_ticks()
                if tempo_atual - ultimo_tiro >= intervalo_tiro and estado == "jogando":
                    laser = Laser(jogador.rect.centerx, jogador.rect.top + 10)
                    grupo_lasers.add(laser)
                    som_laser.play()
                    ultimo_tiro = tempo_atual

        if event.type == CRIAR_ASTEROIDE:
            if len(grupo_asteroides) < 6 and estado == "jogando":
                asteroide = Asteroide()
                grupo_asteroides.add(asteroide)

        if event.type == FIM_MUSICA:
            musica_atual += 1
            if musica_atual >= len(musicas):
                musica_atual = 0
            pygame.mixer.music.load(musicas[musica_atual])
            pygame.mixer.music.play()

    if estado == "jogando":
        jogador.update()
        grupo_lasers.update()
        grupo_asteroides.update()

        for asteroide in grupo_asteroides:
            if asteroide.rect.top > altura_tela:
                jogador.vidas -= 1
                asteroide.kill()

        colisoes = pygame.sprite.groupcollide(grupo_asteroides, grupo_lasers, True, True, pygame.sprite.collide_mask)
        for asteroide_atingido in colisoes:
            som_explosao.play()
            posicao = imagem_explosao.get_rect(center=asteroide_atingido.rect.center)
            explosoes.append([posicao, pygame.time.get_ticks()])

            pontuacao += random.randint(50, 150)
            if pontuacao >= proxima_vida:
                jogador.vidas = jogador.vidas + 1
                proxima_vida = proxima_vida + 5000

        batidas = pygame.sprite.spritecollide(jogador, grupo_asteroides, True, pygame.sprite.collide_mask)
        for asteroide_batido in batidas:
            jogador.vidas = jogador.vidas - 1
            som_explosao.play()

        if jogador.vidas <= 0:
            estado = "game_over"

    movimentacao_fundo = movimentacao_fundo + velocidade_fundo
    if movimentacao_fundo >= altura_tela:
        movimentacao_fundo = 0

    tela.blit(plano_fundo, (0, movimentacao_fundo))
    tela.blit(plano_fundo, (0, movimentacao_fundo - altura_tela))
    grupo_lasers.draw(tela)
    grupo_asteroides.draw(tela)

    for explosao in explosoes[:]:
        if pygame.time.get_ticks() - explosao[1] > 300:
            explosoes.remove(explosao)
        else:
            tela.blit(imagem_explosao, explosao[0])
    tela.blit(jogador.image, jogador.rect) #desenha a nave

    texto_pontos = fonte.render(f"Pontos: {pontuacao}", True, (255, 255, 255))
    tela.blit(texto_pontos, (10, 10))

    texto_vidas = fonte.render(f"Vidas: {max(0, jogador.vidas)}", True, (255, 255, 255))
    tela.blit(texto_vidas, texto_vidas.get_rect(topright=(largura_tela - 10, 10)))

    if estado == "game_over":
        texto_fim = fonte_grande.render("GAME OVER", True, (255, 80, 80))
        tela.blit(texto_fim, texto_fim.get_rect(center=(largura_tela // 2, altura_tela // 2)))
        velocidade_fundo = 0
        pygame.mixer.music.pause()

    pygame.display.flip()