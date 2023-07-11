from typing import Any
import pygame 
import os
import random
from pathlib import Path
from configFB import Configuracao

config = Configuracao()


class Bird:

    def __init__(self, x, y) -> None:
        self.lista_imagens: dict = config.IMAGENS_BIRD
        self.rotacao_maxima: int = 25
        self.rotacao_velocidade: int = 20
        self.tempo_animacao: int = 5

        self.eixo_x: int = x
        self.eixo_y: int = y
        
        self.angulo: int = 0
        self.velocidade: int = 0
        self.altura: object = self.eixo_y

        self.tempo: int = 0
        self.contagem_imagem:int = 0
        self.imagem: object = self.lista_imagens[0]


    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.eixo_y


    def mover(self):
        # calcular o deslocamento
        self.tempo += 1
        deslocamento = 1.5*(self.tempo**2) + self.velocidade * self.tempo

        # restringir o deslocamento
        if deslocamento > 16:
            deslocamento = 16

        elif deslocamento < 0:
            deslocamento -= 2
        
        self.eixo_y += deslocamento

        # o angulo do passaro
        if deslocamento < 0 or self.eixo_y < (self.altura + 50):
            if self.angulo < self.rotacao_maxima:
                self.altura = self.rotacao_maxima
        else:
            if self.angulo > -90:
                self.angulo -= self.rotacao_velocidade


    def draw(self, tela):

        # definiar qual imagem do passaro usar
        self.contagem_imagem += 1

        if self.contagem_imagem < self.tempo_animacao:
            self.imagem = self.lista_imagens[0]
        elif self.contagem_imagem < self.tempo_animacao*2:
            self.imagem = self.lista_imagens[1]
        elif self.contagem_imagem < self.tempo_animacao*3:
            self.imagem = self.lista_imagens[2]
        elif self.contagem_imagem < self.tempo_animacao*4:
            self.imagem = self.lista_imagens[1]
        elif self.contagem_imagem < self.tempo_animacao*4+1:
            self.imagem = self.lista_imagens[0]
            self.contagem_imagem = 0

        # ao cair, nao bate asa
        if self.angulo <= 80:
            self.imagem = self.lista_imagens[1]
            self.contagem_imagem = self.tempo_animacao*2

        # load img
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.eixo_x, self.eixo_y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)


    def get_colisao(self):
        return pygame.mask.from_surface(self.imagem)
        

class Pipe:
    DISTANCIA =  200
    VELOCIDADE = 5

    def __init__(self, x) -> None:
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_BASE = config.IMAGEM_PIPE
        self.CANO_TOPO = pygame.transform.flip(config.IMAGEM_PIPE, False, True)
        self.passou_cano = False
        self.definir_altura_objeto_cano()


    def definir_altura_objeto_cano(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA


    def mover(self):
        self.x -= self.VELOCIDADE


    def draw(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    
    def colidir(self, passaro):
        passaro_mask = passaro.get_colisao()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.eixo_x, self.pos_topo - round(passaro.eixo_y))
        distancia_base = (self.x - passaro.eixo_x, self.pos_base - round(passaro.eixo_y))

        topo_ponto_colisao = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto_colisao = passaro_mask.overlap(base_mask, distancia_base)

        if base_ponto_colisao or topo_ponto_colisao:
            return True
        else:
            return False



class Ground:
    VELOCIDADE = 5
    LARGURA = config.IMAGEM_GROUND.get_width()
    IMAGEM = config.IMAGEM_GROUND

    def __init__(self, y) -> None:
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA    


    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA


    def draw(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))



def run_tela(tela, passaros, pipes, ground, pontos):
    tela.blit(config.IMAGEM_BG, (0,0))
    for passaro in passaros:
        passaro.draw(tela)

    for cano in pipes:
        cano.draw(tela)

    texto = config.FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, 'white')
    tela.blit(texto, (config.TELA_LARGURA - 10 - texto.get_width(), 10))

    ground.draw(tela)

    pygame.display.update()

def main():
    passaros = [Bird(230, 350)]
    chao = Ground(730)
    canos = [Pipe(700)]
    tela = pygame.display.set_mode((config.TELA_LARGURA, config.TELA_ALTURA))
    pontos = 0
    att_tela_relogio = pygame.time.Clock()

    jogo_rodando = True
    while jogo_rodando:
        att_tela_relogio.tick(30)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jogo_rodando = False
                pygame.quit()
                quit()
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE :
                    passaro.pular()
        for passaro in passaros:
            passaro.mover()
        chao.mover()

        adicionar_cano = False
        remover_canos = list()

        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                if not cano.passou_cano and passaro.eixo_x > cano.x:
                    cano.passou_cano = True
                    adicionar_cano = True

            cano.mover()
            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)

            
        if adicionar_cano:
            pontos += 1
            canos.append(Pipe(600))

        for cano in remover_canos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if (passaro.eixo_y + passaro.imagem.get_height()) > chao.y or passaro.eixo_y < 0:
                passaros.pop(i)


        run_tela(tela, passaros, canos, chao, pontos)


if __name__=='__main__':
    main()
