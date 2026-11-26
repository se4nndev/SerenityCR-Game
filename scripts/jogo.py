import pygame
from scripts.jogador import Jogador

class Jogo:

    def __init__(self, tela):

        self.tela = tela

        self.largura_tela = 600
        self.altura_tela = 750

        self.fonte = pygame.font.Font("fonte/Orbitron.ttf", 35)
        self.fonte_grande = pygame.font.Font("fonte/Orbitron.ttf", 60)

        self.som_laser = pygame.mixer.Sound("sons/tiro-laser.wav")
        self.som_laser.set_volume(0.9)

        self.som_explosao = pygame.mixer.Sound("sons/explosao-asteroide.wav")
        self.som_explosao.set_volume(0.65)

        self.som_game_over = pygame.mixer.Sound("sons/game-over.wav")
        self.som_game_over.set_volume(0.7)

        self.ultimo_tiro = 0
        self.intervalo_tiro = 350

        self.imagem_explosao = pygame.image.load(
            "imagens/explosao-asteroide.png"
        ).convert_alpha()

        self.imagem_explosao = pygame.transform.scale(
            self.imagem_explosao, (135, 135)
        )

        self.explosoes = []

        self.plano_fundo = pygame.image.load(
            "imagens/fundo-espacial.png"
        ).convert()

        self.plano_fundo = pygame.transform.scale(
            self.plano_fundo,
            (self.largura_tela, self.altura_tela)
        )

        self.movimentacao_fundo = 0
        self.velocidade_fundo = 1

#instanciando a classe do jogador e criando os grupos
        self.jogador = Jogador()

        self.grupo_lasers = pygame.sprite.Group()
        self.grupo_asteroides = pygame.sprite.Group()

        self.pontuacao = 0
        self.proxima_vida = 5000

        self.estado = "jogando"
        self.game_over_tocado = False

    def iniciar(self):
        self.estado = "jogando"

        self.jogador = Jogador()
        self.grupo_lasers.empty()
        self.grupo_asteroides.empty()

        self.pontuacao = 0
        self.proxima_vida = 5000

        self.ultimo_tiro = 0
        self.game_over_tocado = False

        pygame.time.set_timer(self.CRIAR_ASTEROIDE, 600)

    def eventos(self, event):

            if self.estado != "jogando":
                return

            if event.type == KEYDOWN and event.key == K_SPACE:

                agora = pygame.time.get_ticks()

                if agora - self.ultimo_tiro >= self.intervalo_tiro:

                    laser = Laser(
                        self.jogador.rect.centerx,
                        self.jogador.rect.top
                    )

                    self.grupo_lasers.add(laser)

                    self.som_laser.play()
                    self.ultimo_tiro = agora

            if event.type == self.CRIAR_ASTEROIDE:

                if len(self.grupo_asteroides) < 6:

                    asteroide = Asteroide()
                    self.grupo_asteroides.add(asteroide)

            if event.type == self.FIM_MUSICA:

                self.musica_atual = (self.musica_atual + 1) % len(self.musicas)

                pygame.mixer.music.load(self.musicas[self.musica_atual])
                pygame.mixer.music.play()
