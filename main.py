import pygame
from pygame.locals import *
from sys import exit
from scripts.jogo import Jogo
from scripts.jogador import Jogador
from scripts.tirolaser import Laser
from scripts.asteroide import Asteroide
from configs.config_gerais import *
from configs.config_sons import *
from Interface.menu import Menu
import random

pygame.init()

tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

largura_monitor, altura_monitor = tela.get_size()

tela_virtual = pygame.Surface((largura_tela, altura_tela))

escala = min(
    largura_monitor / largura_tela,
    altura_monitor / altura_tela
)

largura_escalada = int(largura_tela * escala)
altura_escalada = int(altura_tela * escala)

offset_x = (largura_monitor - largura_escalada) // 2
offset_y = (altura_monitor - altura_escalada) // 2

pygame.display.set_caption("Serenity: Cosmic Rain")
relogio = pygame.time.Clock()

imagem_explosao = pygame.image.load("imagens/explosao-asteroide.png").convert_alpha()
imagem_explosao = pygame.transform.scale(imagem_explosao, (135, 135))
explosoes = []

plano_fundo = pygame.image.load("imagens/fundo-espacial.png").convert()
plano_fundo = pygame.transform.scale(plano_fundo, (largura_tela, altura_tela))
movimentacao_fundo = 0
velocidade_fundo = 1

jogador = Jogador()
grupo_lasers = pygame.sprite.Group()
grupo_asteroides = pygame.sprite.Group()
CRIAR_ASTEROIDE = USEREVENT + 1
pygame.time.set_timer(CRIAR_ASTEROIDE, 600)

fullscreen = False

menu = Menu()

estado = "menu"

while True:

    relogio.tick(60)

    for event in pygame.event.get():
    
        if event.type == KEYDOWN:
            
            if event.key == K_F11:

                fullscreen = not fullscreen

                if fullscreen:
                    tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    tela = pygame.display.set_mode((1000, 800))

                largura_monitor, altura_monitor = tela.get_size()

                escala = min(
                    largura_monitor / largura_tela,
                    altura_monitor / altura_tela
                )

                largura_escalada = int(largura_tela * escala)
                altura_escalada = int(altura_tela * escala)

                offset_x = (largura_monitor - largura_escalada) // 2
                offset_y = (altura_monitor - altura_escalada) // 2
    

        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:
                pygame.quit()
                exit()

            if estado == "menu":

                if event.key == K_RETURN:
                    estado = "jogando"

            elif estado == "jogando":

                if event.key == K_SPACE:

                    tempo_atual = pygame.time.get_ticks()

                    if tempo_atual - ultimo_tiro >= intervalo_tiro:

                        laser = Laser(
                            jogador.rect.centerx,
                            jogador.rect.top + 10
                        )

                        grupo_lasers.add(laser)

                        som_laser.play()

                        ultimo_tiro = tempo_atual

        if event.type == CRIAR_ASTEROIDE:

            if estado == "jogando":

                if len(grupo_asteroides) < 6:
                    grupo_asteroides.add(Asteroide())

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

        if jogador.vidas <= 0 and estado != "game_over":
            estado = "game_over"
            pygame.mixer.music.stop()
            som_game_over.play()

    movimentacao_fundo = movimentacao_fundo + velocidade_fundo
    if movimentacao_fundo >= altura_tela:
        movimentacao_fundo = 0

    tela_virtual.fill((0, 0, 0))

    if estado == "menu":

        tela_virtual.blit(plano_fundo, (0, 0))
        menu.desenhar_menu(tela_virtual)

    elif estado == "jogando":

        tela_virtual.blit(plano_fundo, (0, movimentacao_fundo))
        tela_virtual.blit(plano_fundo, (0, movimentacao_fundo - altura_tela))

        grupo_lasers.draw(tela_virtual)
        grupo_asteroides.draw(tela_virtual)

        for explosao in explosoes[:]:
            if pygame.time.get_ticks() - explosao[1] > 300:
                explosoes.remove(explosao)
            else:
                tela_virtual.blit(imagem_explosao, explosao[0])

        tela_virtual.blit(jogador.image, jogador.rect)

        texto_pontos = fonte.render(
            f"Pontos: {pontuacao}",
            True,
            (255, 255, 255)
        )

        tela_virtual.blit(texto_pontos, (10, 10))

        texto_vidas = fonte.render(
            f"Vidas: {max(0, jogador.vidas)}",
            True,
            (255, 255, 255)
        )

        tela_virtual.blit(
            texto_vidas,
            texto_vidas.get_rect(topright=(largura_tela - 10, 10))
        )

    elif estado == "game_over":
        texto_fim = fonte_grande.render("GAME OVER", True, (255, 80, 80))
        tela_virtual.blit(texto_fim, texto_fim.get_rect(center=(largura_tela // 2, altura_tela // 2)))
        velocidade_fundo = 0
        pygame.mixer.music.stop()

    tela.fill((0, 0, 0))

    superficie_escalada = pygame.transform.smoothscale(
        tela_virtual,
        (largura_escalada, altura_escalada)
    )

    tela.blit(superficie_escalada, (offset_x, offset_y))

    pygame.display.flip()