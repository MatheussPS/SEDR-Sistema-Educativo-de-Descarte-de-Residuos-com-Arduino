import pygame
from config import config

class BackgroundService:

    TOTAL_NIVEIS = 6
    BASE_ASSET = 'bg_park_dirt_0'
    BASE_PASTA = 'padrao_fases'
    BASE_CAMINHO_BACKGROUND = "assets/background"

    PONTUACOES = [100, 75, 50, 35, 20, 0]

    def __init__(self):
        self.imagens_originais = [
            pygame.image.load(
                f'{self.BASE_CAMINHO_BACKGROUND}/{self.BASE_PASTA}/{self.BASE_ASSET}{i}.jpeg'
            ).convert()
            for i in range(self.TOTAL_NIVEIS)
        ]
        
        self.imagens_game_over = [
            pygame.image.load(f"{self.BASE_CAMINHO_BACKGROUND}/game_over/bg_game_over_00.jpeg").convert(),
            pygame.image.load(f"{self.BASE_CAMINHO_BACKGROUND}/game_over/bg_game_over_01.jpeg").convert()
        ]

        self.game_over = False
        self.estado_game_over = 0 
        self.nivel_atual = 5
        
        self.imagem = self.redimensionar()

    def redimensionar(self):

        imagem_base = (
            self.imagens_game_over[self.estado_game_over] 
            if self.game_over 
            else self.imagens_originais[self.nivel_atual]
        )
        
        tamanho_tela = (config.LARGURA_TELA, config.ALTURA_TELA)
        self.imagem = pygame.transform.scale(imagem_base, tamanho_tela)
        
        return self.imagem

    def atualizar_background(self, pontuacao):

        if self.game_over:
            return self.imagem

        novo_nivel = 5  # padrão inicial
        for nivel, pontuacao_minima in enumerate(self.PONTUACOES):
            if pontuacao >= pontuacao_minima:
                novo_nivel = nivel
                break

        # SÓ redimensiona se o nível realmente mudou
        if novo_nivel != self.nivel_atual:
            self.nivel_atual = novo_nivel
            self.redimensionar()

        return self.imagem

    def disparar_game_over(self, pontuacao):
        if not self.game_over:
            self.game_over = True
            
            self.estado_game_over = 1 if pontuacao <= self.PONTUACOES[1] else 0

            self.redimensionar()
        
        return self.imagem
