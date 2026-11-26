
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

        self.fonte_creditos = pygame.font.Font(
            "fonte/Orbitron.ttf", 22
        )

        self.branco = (255, 255, 255)
        self.azul = (30, 150, 220)
        self.ciano = (0, 220, 255)

        self.botao_jogar = pygame.Rect(150, 330, 300, 65)
        self.botao_sair = pygame.Rect(150, 410, 300, 65)
        self.botao_creditos = pygame.Rect(150, 490, 300, 65)

        self.botao_voltar = pygame.Rect(150, 490, 300, 65)

    def desenhar(self, mouse):

        titulo = self.fonte_titulo.render(
            "ASTEROIDES", True, self.branco
        )

        titulo_rect = titulo.get_rect(center=(300, 200))
        self.tela.blit(titulo, titulo_rect)

        self.desenhar_botao(self.botao_jogar, "JOGAR", mouse)
        self.desenhar_botao(self.botao_sair, "SAIR", mouse)
        self.desenhar_botao(self.botao_creditos, "CREDITOS", mouse)

    def desenhar_creditos(self, mouse):

        mouse = pygame.mouse.get_pos()

        titulo = self.fonte_titulo.render(
            "CREDITOS", True, self.branco
        )

        titulo_rect = titulo.get_rect(center=(300, 180))
        self.tela.blit(titulo, titulo_rect)

        textos = [
            "Desenvolvimento:",
            "Alvaro Gabriel",
            "Anderson Antonio",
            "Seann Halley",
            "Projeto de jogo em Pygame"
        ]

        for i, texto in enumerate(textos):
            imagem = self.fonte_creditos.render(
                texto, True, self.branco
            )

            rect = imagem.get_rect(
                center=(300, 280 + i * 45)
            )

            self.tela.blit(imagem, rect)

        self.desenhar_botao(
            self.botao_voltar, "VOLTAR", mouse
        )

    def desenhar_botao(self, botao, texto, mouse):

        if botao.collidepoint(mouse):
            cor = self.ciano
        else:
            cor = self.azul

        pygame.draw.rect(self.tela, cor, botao, 2)

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

        elif self.botao_creditos.collidepoint(posicao):
            return "creditos"

        return None

    def verificar_clique_creditos(self, posicao):

        if self.botao_voltar.collidepoint(posicao):
            return "menu"

        return None
