
import pygame


class MenuPrincipal:

    def __init__(self, tela):

        self.tela = tela

        self.fonte_titulo = pygame.font.Font(
            "fonte/Orbitron.ttf", 55
        )

        self.fonte_botoes = pygame.font.Font(
            "fonte/Orbitron.ttf", 28
        )

        self.branco = (255, 255, 255)
        self.azul = (30, 150, 220)
        self.ciano = (0, 220, 255)

        self.botao_jogar = pygame.Rect(150, 350, 300, 65)
        self.botao_sair = pygame.Rect(150, 450, 300, 65)

    def desenhar(self):

        self.tela.fill((5, 5, 25))

        titulo = self.fonte_titulo.render(
            "SERENITY", True, self.ciano
        )

        subtitulo = self.fonte_botoes.render(
            "COSMIC RAIN", True, self.branco
        )

        self.tela.blit(
            titulo,
            titulo.get_rect(center=(300, 180))
        )

        self.tela.blit(
            subtitulo,
            subtitulo.get_rect(center=(300, 240))
        )

        self.desenhar_botao(self.botao_jogar, "JOGAR")
        self.desenhar_botao(self.botao_sair, "SAIR")

    def desenhar_botao(self, botao, texto):

        mouse = pygame.mouse.get_pos()

        if botao.collidepoint(mouse):
            cor = self.ciano
        else:
            cor = self.azul

        pygame.draw.rect(
            self.tela,
            cor,
            botao,
            2
        )

        texto_renderizado = self.fonte_botoes.render(
            texto, True, self.branco
        )

        texto_rect = texto_renderizado.get_rect(
            center=botao.center
        )

        self.tela.blit(texto_renderizado, texto_rect)

    def verificar_clique(self, posicao):

        if self.botao_jogar.collidepoint(posicao):
            return "jogar"

        elif self.botao_sair.collidepoint(posicao):
            return "sair"

        return None
