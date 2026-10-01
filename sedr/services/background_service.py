import pygame

from config import config


class BackgroundService:

    nivel = 5
    BASE_ASSET = 'bg_park_dirt_0'
    BASE_CAMINHO_BACKGROUND = f"assets/background/{BASE_ASSET}"

    def __init__(self):
        self.imagem_original = self.gerar_imagem()
        self.imagem = self.redimensionar()

    def gerar_imagem(self):

        return pygame.image.load(
            f'{self.BASE_CAMINHO_BACKGROUND}{self.nivel}.jpeg'
        ).convert()

    def redimensionar(self):

        self.imagem = pygame.transform.scale(
            self.imagem_original,
            (
                config.LARGURA_TELA,
                config.ALTURA_TELA
            )
        )

        return self.imagem

    def atualizar_background(self, pontuacao):

        if pontuacao >= 100:
            self.nivel = 0

        elif pontuacao >= 75:
            self.nivel = 1

        elif pontuacao >= 50:
            self.nivel = 2

        elif pontuacao >= 35:
            self.nivel = 3

        elif pontuacao >= 20:
            self.nivel = 4

        self.imagem_original = self.gerar_imagem()

        return self.redimensionar()