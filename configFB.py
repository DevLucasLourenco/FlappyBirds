import pygame 
from pathlib import Path


class Configuracao():

    def __init__(self) -> None:
        self.TELA_LARGURA = 500
        self.TELA_ALTURA = 800

        self.IMAGEM_PIPE = pygame.transform.scale2x(pygame.image.load(Path('Imagens/pipe.png')))
        self.IMAGEM_GROUND = pygame.transform.scale2x(pygame.image.load(Path('Imagens/base.png')))
        self.IMAGEM_BG = pygame.transform.scale2x(pygame.image.load(Path('Imagens/bg.png')))
        
        self.IMAGENS_BIRD = [
            pygame.transform.scale2x(
                    pygame.image.load(Path('Imagens/bird1.png'))),

            pygame.transform.scale2x(
                    pygame.image.load(Path('Imagens/bird2.png'))),

            pygame.transform.scale2x(
                    pygame.image.load(Path('Imagens/bird3.png'))),
        ]

        pygame.font.init()
        self.FONTE_PONTOS = pygame.font.SysFont('arial', 50)

    