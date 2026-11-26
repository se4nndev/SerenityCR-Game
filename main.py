import pygame

pygame.init()

from pygame.locals import *
from sys import exit
import random

from scripts.gerenciador_musica import GerenciadorMusica
from scripts.jogador import Jogador
from scripts.tirolaser import Laser
from scripts.asteroide import Asteroide
from configs.config_gerais import *
from configs.config_sons import *
from Interface.menu import MenuPrincipal


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

relogio = pygame.time.Clock()

imagem_explosao = pygame.image.load(
    "imagens/explosao-asteroide.png"
).convert_alpha()

imagem_explosao = pygame.transform.scale(
    imagem_explosao, (135, 135)
)

explosoes = []

imagem_menu = pygame.image.load(
    "imagens/menu_tela.jpeg"
).convert()

imagem_menu = pygame.transform.scale(
    imagem_menu, (largura_tela, altura_tela)
)

plano_fundo = pygame.image.load(
    "imagens/fundo-espacial.png"
).convert()

plano_fundo = pygame.transform.scale(
    plano_fundo, (largura_tela, altura_tela)
)


movimentacao_fundo = 0
velocidade_fundo = 1

jogador = Jogador()

gerenciador_musica = GerenciadorMusica(
    musicas,
    "sons/musica-menu.wav"
)
gerenciador_musica.tocar_menu()

grupo_lasers = pygame.sprite.Group()
grupo_asteroides = pygame.sprite.Group()
botao_voltar_menu = pygame.Rect(150, 450, 300, 65)

CRIAR_ASTEROIDE = USEREVENT + 1

pygame.time.set_timer(CRIAR_ASTEROIDE, 600)

fullscreen = True

menu = MenuPrincipal(tela_virtual)

estado = "menu"

def reiniciar_jogo():

    global jogador
    global pontuacao
    global proxima_vida
    global ultimo_tiro
    global movimentacao_fundo
    global velocidade_fundo
    global estado

    jogador = Jogador()

    grupo_lasers.empty()
    grupo_asteroides.empty()

    explosoes.clear()

    pontuacao = 0
    proxima_vida = 5000

    ultimo_tiro = 0

    movimentacao_fundo = 0
    velocidade_fundo = 1

    gerenciador_musica.tocar_jogo()

    estado = "jogando"

def voltar_menu():
    global jogador, pontuacao, proxima_vida
    global movimentacao_fundo, velocidade_fundo, estado

    jogador = Jogador()

    grupo_lasers.empty()
    grupo_asteroides.empty()
    explosoes.clear()

    pontuacao = 0
    proxima_vida = 5000

    movimentacao_fundo = 0
    velocidade_fundo = 1

    estado = "menu"
    gerenciador_musica.tocar_menu()

while True:

    relogio.tick(60)


    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:
                pygame.quit()
                exit()

            elif event.key == K_F11:

                fullscreen = not fullscreen

                if fullscreen:
                    tela = pygame.display.set_mode(
                        (0, 0), pygame.FULLSCREEN
                    )
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

            elif estado == "menu":

                if event.key == K_RETURN:
                    reiniciar_jogo()

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

            elif estado == "game_over":

                if event.key == K_r:
                    reiniciar_jogo()

        if event.type == MOUSEBUTTONDOWN and event.button == 1:

            if (
                offset_x <= event.pos[0] < offset_x + largura_escalada
                and offset_y <= event.pos[1] < offset_y + altura_escalada
            ):

                x = int((event.pos[0] - offset_x) / escala)
                y = int((event.pos[1] - offset_y) / escala)

                posicao = (x, y)

                if estado == "menu":

                    acao = menu.verificar_clique(posicao)

                    if acao == "jogar":
                        reiniciar_jogo()

                    elif acao == "sair":
                        pygame.quit()
                        exit()

                    elif acao == "creditos":
                        estado = "creditos"

                elif estado == "creditos":

                    acao = menu.verificar_clique_creditos(posicao)

                    if acao == "menu":
                        estado = "menu"

                elif estado == "game_over":

                    if botao_voltar_menu.collidepoint(posicao):
                        voltar_menu()

        if event.type == CRIAR_ASTEROIDE:

            if estado == "jogando" and len(grupo_asteroides) < 6:
                grupo_asteroides.add(Asteroide())

        if event.type == FIM_MUSICA and estado == "jogando":
            gerenciador_musica.proxima_musica()

    if estado == "jogando":

        jogador.update()
        grupo_lasers.update()
        grupo_asteroides.update()

        for asteroide in grupo_asteroides:

            if asteroide.rect.top > altura_tela:
                jogador.vidas -= 1
                asteroide.kill()

        colisoes = pygame.sprite.groupcollide(
            grupo_asteroides,
            grupo_lasers,
            True,
            True,
            pygame.sprite.collide_mask
        )

        for asteroide_atingido in colisoes:

            som_explosao.play()

            posicao = imagem_explosao.get_rect(
                center=asteroide_atingido.rect.center
            )

            explosoes.append([
                posicao,
                pygame.time.get_ticks()
            ])

            pontuacao += random.randint(50, 150)

            if pontuacao >= proxima_vida:

                jogador.vidas += 1
                proxima_vida += 5000

        batidas = pygame.sprite.spritecollide(
            jogador,
            grupo_asteroides,
            True,
            pygame.sprite.collide_mask
        )

        for asteroide_batido in batidas:

            jogador.vidas -= 1
            som_explosao.play()

    if estado == "jogando" and jogador.vidas <= 0:

        estado = "game_over"
        velocidade_fundo = 0

        gerenciador_musica.pausar()
        som_game_over.play()

    if estado == "jogando":
        movimentacao_fundo += velocidade_fundo

    if movimentacao_fundo >= altura_tela:
        movimentacao_fundo = 0

    mouse_x, mouse_y = pygame.mouse.get_pos()

    mouse_virtual = (
        int((mouse_x - offset_x) / escala),
        int((mouse_y - offset_y) / escala)
    )

    tela_virtual.fill((0, 0, 0))

    if estado == "menu":

        tela_virtual.blit(imagem_menu, (0, 0))
        menu.desenhar(mouse_virtual)

    elif estado == "creditos":

        tela_virtual.blit(imagem_menu, (0, 0))
        menu.desenhar_creditos(mouse_virtual)

    elif estado == "jogando":

        tela_virtual.blit(
            plano_fundo,
            (0, movimentacao_fundo)
        )

        tela_virtual.blit(
            plano_fundo,
            (0, movimentacao_fundo - altura_tela)
        )

        grupo_lasers.draw(tela_virtual)
        grupo_asteroides.draw(tela_virtual)

        tempo_atual = pygame.time.get_ticks()

        for explosao in explosoes[:]:

            posicao, tempo_explosao = explosao

            tela_virtual.blit(imagem_explosao, posicao)

            if tempo_atual - tempo_explosao >= 300:
                explosoes.remove(explosao)

        tela_virtual.blit(jogador.image, jogador.rect)

        texto_pontuacao = fonte.render(
            f"PONTUAÇÃO: {pontuacao}",
            True,
            (255, 255, 255)
        )

        tela_virtual.blit(texto_pontuacao, (10, 10))

        texto_vidas = fonte.render(
            f"VIDAS: {jogador.vidas}",
            True,
            (255, 255, 255)
        )

        tela_virtual.blit(texto_vidas, (10, 45))

    elif estado == "game_over":

        tela_virtual.blit(plano_fundo, (0, 0))

        texto = fonte_grande.render(
            "GAME OVER", True, (255, 0, 0)
        )

        texto_rect = texto.get_rect(center=(300, 250))
        tela_virtual.blit(texto, texto_rect)

        menu.desenhar_botao(
            botao_voltar_menu,
            "VOLTAR AO MENU",
            mouse_virtual
        )

    # APRESENTAÇÃO DA TELA
    tela.fill((0, 0, 0))

    superficie_escalada = pygame.transform.smoothscale(
        tela_virtual,
        (largura_escalada, altura_escalada)
    )

    tela.blit(
        superficie_escalada,
        (offset_x, offset_y)
    )

    pygame.display.flip()
