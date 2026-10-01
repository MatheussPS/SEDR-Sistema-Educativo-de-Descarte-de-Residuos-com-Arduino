import pygame

from config import config


class BackgroundService:

    TOTAL_NIVEIS = 6
    BASE_ASSET = 'bg_park_dirt_0'
    BASE_CAMINHO_BACKGROUND = f"assets/background/{BASE_ASSET}"

    # Pontuações mínimas para cada nível (índice = nível)
    PONTUACOES = [100, 75, 50, 35, 20, 0]

    def __init__(self):
        # Pré-carrega todas as imagens originais uma única vez
        self.imagens_originais = [
            pygame.image.load(
                f'{self.BASE_CAMINHO_BACKGROUND}{i}.jpeg'
            ).convert()
            for i in range(self.TOTAL_NIVEIS)
        ]

        self.nivel_atual = 5
        self.imagem = self.redimensionar()

    def redimensionar(self):
        self.imagem = pygame.transform.scale(
            self.imagens_originais[self.nivel_atual],
            (config.LARGURA_TELA, config.ALTURA_TELA)
        )
        return self.imagem

    def atualizar_background(self, pontuacao):
        novo_nivel = 5  # padrão: background inicial

        for nivel, pontuacaoT in enumerate(self.PONTUACOES):
            if pontuacao >= pontuacaoT:
                novo_nivel = nivel
                break

        # Só reescala se o nível realmente mudou
        if novo_nivel != self.nivel_atual:
            self.nivel_atual = novo_nivel
            return self.redimensionar()

        return self.imagem
