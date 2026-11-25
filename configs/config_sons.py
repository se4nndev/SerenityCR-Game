import pygame

som_laser = pygame.mixer.Sound("sons/tiro-laser.wav")
som_laser.set_volume(0.9)

som_explosao = pygame.mixer.Sound("sons/explosao-asteroide.wav")
som_explosao.set_volume(0.65)

som_game_over = pygame.mixer.Sound("sons/game-over.wav")
som_game_over.set_volume(0.7)

musicas = ["sons/musica-jogo-agitacao.wav", "sons/musica-jogo-vibes.wav", "sons/musica-jogo-tensa.wav"]
musica_atual = 0
FIM_MUSICA = pygame.USEREVENT + 2

pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.set_endevent(FIM_MUSICA)
pygame.mixer.music.load(musicas[musica_atual])
pygame.mixer.music.play()