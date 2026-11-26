import pygame
from configs.config_gerais import *

class Menu:
    
    def __init__(self):
        
        self.fonte_menu = pygame.font.Font(
            "fonte/8bit.ttf",
            32
        )

        self.fonte_menu_titulo = pygame.font.Font(
            "fonte/8bit.ttf",
            64
        )

    def desenhar_menu(self, tela):
            
        titulo = self.fonte_menu_titulo.render("SERENITY", True, (255, 255, 255))
        subtitulo = self.fonte_menu.render("COSMIC RAIN", True, (180, 180, 255))
        iniciar = self.fonte_menu.render("Pressione ENTER para jogar", True, (255, 255, 255))
        sair = self.fonte_menu.render("ESC para sair", True, (255, 255, 255))
            
        tela.blit(titulo, titulo.get_rect(center=(largura_tela // 2, 250)))
        tela.blit(subtitulo, subtitulo.get_rect(center=(largura_tela // 2, 320)))
        tela.blit(iniciar, iniciar.get_rect(center=(largura_tela // 2, 450)))
        tela.blit(sair, sair.get_rect(center=(largura_tela // 2, 500)))
            