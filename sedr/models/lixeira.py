import pygame

from config import config


class Lixeira:

    def __init__(self, tipo, imagem, pos_x, pos_y):

        self.tipo = tipo

        self.imagem_original = imagem
        self.imagem = imagem

        self.x = pos_x
        self.y = pos_y

        self.largura, self.altura = self.calcular_tamanho()

        self.imagem = pygame.transform.scale(
            self.imagem_original,
            (
                int(self.largura),
                int(self.altura)
            )
        )

    def calcular_tamanho(self):

        largura = config.LARGURA_TELA * config.PROPORCAO_LIXEIRA

        proporcao = (
            self.imagem_original.get_width()
            / self.imagem_original.get_height()
        )

        altura = largura / proporcao

        return largura, altura

    def atualizar_tamanho(self):

        self.largura, self.altura = self.calcular_tamanho()

        self.imagem = pygame.transform.scale(
            self.imagem_original,
            (
                int(self.largura),
                int(self.altura)
            )
        )