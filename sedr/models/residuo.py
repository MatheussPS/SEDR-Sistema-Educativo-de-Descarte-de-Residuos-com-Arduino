import pygame
import random

from config import config


class Residuo:

    def __init__(self, tipo, imagem):
        self.tipo = tipo

        self.imagem_original = imagem

        self.largura, self.altura = self.calcular_tamanho()

        self.imagem = pygame.transform.scale(
            self.imagem_original,
            (
                int(self.largura),
                int(self.altura)
            )
        )

        self.x = random.randint(
            0,
            int(config.LARGURA_TELA - self.largura)
        )

        self.y = 0

        self.ativo = True
        
        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.largura,
            self.altura
        )

    def calcular_tamanho(self):
        largura = config.LARGURA_TELA * config.PROPORCAO_RESIDUO

        proporcao = (
            self.imagem_original.get_width()
            / self.imagem_original.get_height()
        )

        altura = largura / proporcao

        return largura, altura

    def atualizar_tamanho(self):
        centro_x = self.x + self.largura / 2

        self.largura, self.altura = self.calcular_tamanho()

        self.x = centro_x - self.largura / 2

        self.imagem = pygame.transform.scale(
                self.imagem_original,
                (
                    int(self.largura),
                    int(self.altura)
                )
            )
        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.largura,
            self.altura
        )

    def mover(self, dx, dy):
        self.x += dx
        self.y += dy
        
        if self.x + self.largura < 0 :
            self.x = config.LARGURA_TELA

        elif self.x  > config.LARGURA_TELA:
            self.x = 0
        
        self.rect.topleft = (self.x, self.y)

    # IMPEDE QUE O RESIDUO PASSE DOS LIMITES
    # def mover(self, dx, dy):
    #     self.x += dx
    #     self.y += dy
        
    #     if self.x < 0:
    #         self.x = 0

    #     if self.x + self.largura > config.LARGURA_TELA:
    #         self.x = config.LARGURA_TELA - self.largura
        
    #     self.rect.topleft = (self.x, self.y)
    
    # def centralizar_x(self):
    #     centro_x = config.LARGURA_TELA / 2

    #     self.x = centro_x - self.largura / 2