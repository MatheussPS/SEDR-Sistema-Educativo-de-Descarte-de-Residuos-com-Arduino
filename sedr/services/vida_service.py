import pygame

from config import config
from models.vida import Vida


class VidaService:

    CAMINHO_CORACAO = "assets/recortes/coracao-vida.png"

    def __init__(self, sessao):

        self.sessao = sessao
        self.vidas = self.criar_vidas()

    def criar_vidas(self):
        imagem = pygame.image.load(
            self.CAMINHO_CORACAO
        ).convert_alpha()

        tamanho = int(
            config.LARGURA_TELA * config.PROPORCAO_CORACAO
        )

        imagem = pygame.transform.scale(
            imagem,
            (tamanho, tamanho)
        )

        vidas = []

        for _ in range(self.sessao.vidas):
            vidas.append(Vida(imagem, 0, 0))

        return vidas

    def atualizar_posicoes(self):
        tamanho = config.LARGURA_TELA * config.PROPORCAO_CORACAO
        espacamento = config.LARGURA_TELA * config.ESPACAMENTO_CORACAO
        margem = config.LARGURA_TELA * config.MARGEM_HUD

        for i, vida in enumerate(self.vidas):
            vida.x = (config.LARGURA_TELA - margem - tamanho- i * (tamanho + espacamento))

            vida.y = margem

    def atualizar(self):
        # Remove vidas se tiver mais do que deveria
        while len(self.vidas) > self.sessao.vidas:
            self.vidas.pop()
        
        # Adiciona vidas se tiver menos do que deveria (quando reinicia)
        while len(self.vidas) < self.sessao.vidas:
            tamanho = int(config.LARGURA_TELA * config.PROPORCAO_CORACAO)
            imagem = pygame.image.load(self.CAMINHO_CORACAO).convert_alpha()
            imagem = pygame.transform.scale(imagem, (tamanho, tamanho))
            self.vidas.append(Vida(imagem, 0, 0))

        # Redimensionar corações
        tamanho = int(config.LARGURA_TELA * config.PROPORCAO_CORACAO)
        for vida in self.vidas:
            imagem = pygame.image.load(self.CAMINHO_CORACAO).convert_alpha()
            vida.imagem = pygame.transform.scale(imagem, (tamanho, tamanho))

        self.atualizar_posicoes()

    def desenhar(self, tela):
        for vida in self.vidas:
            tela.blit(
                vida.imagem,
                (vida.x, vida.y)
            )