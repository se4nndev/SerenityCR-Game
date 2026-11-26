
import pygame
from configs.config_sons import FIM_MUSICA

class GerenciadorMusica:

    def __init__(self, musicas_jogo, musica_menu):

        self.musicas_jogo = musicas_jogo
        self.musica_menu = musica_menu
        self.musica_atual = 0

    def tocar_menu(self):

        pygame.mixer.music.set_endevent()

        pygame.mixer.music.load(self.musica_menu)
        pygame.mixer.music.play(-1)

    def tocar_jogo(self):

        self.musica_atual = 0

        pygame.mixer.music.set_endevent(FIM_MUSICA)

        pygame.mixer.music.load(
            self.musicas_jogo[self.musica_atual]
        )

        pygame.mixer.music.play()

    def proxima_musica(self):

        self.musica_atual += 1

        if self.musica_atual >= len(self.musicas_jogo):
            self.musica_atual = 0

        pygame.mixer.music.load(
            self.musicas_jogo[self.musica_atual]
        )

        pygame.mixer.music.play()

    def pausar(self):

        pygame.mixer.music.pause()

    def retomar(self):

        pygame.mixer.music.unpause()
