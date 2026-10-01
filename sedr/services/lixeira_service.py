import os
import pygame

from config import config
from models.lixeira import Lixeira

class LixeiraService:
    
    CAMINHO_LIXEIRAS = "assets/lixeiras"

    def criar_lixeiras(self):
        
        ordem = {
            "papel": 0,
            "plastico": 1,
            "vidro": 2,
            "metal": 3
        }

        # Lista os arquivos ordenados pelo dicionario
        arquivos_lixeiras = sorted(
            os.listdir(self.CAMINHO_LIXEIRAS),
            key=lambda arquivo: ordem.get(arquivo.removesuffix(".png"), 99)
        )
        
        # Espaça lixeiras
        espacamento = config.LARGURA_TELA / (len(arquivos_lixeiras) + 1)
        
        # Cria lista de lixeiras
        lista_lixeiras = []
        
        # Para cada lixeira em arquivos_lixeiras faça:
        for i, arquivo in enumerate(arquivos_lixeiras):
            # Cria imagem da lixeira
            caminho_completo = os.path.join(self.CAMINHO_LIXEIRAS, arquivo)
            imagem = pygame.image.load(caminho_completo).convert_alpha()

            # Define eixos x e y
            pos_x = espacamento * (i + 1)
            pos_y = 0
            
            # Pega tipo pelo nome do arquivo
            tipo = arquivo.removesuffix(".png")
            
            # Instancia do objeto Lixeira
            lixeira = Lixeira(
                tipo, 
                imagem,
                pos_x, 
                pos_y,
            )
            
            # Adiciona objeto a lista
            lista_lixeiras.append(lixeira)

        # Retorna lixeiras
        return lista_lixeiras

    def atualizar_posicoes(self, lista_lixeiras):
        quantidade = len(lista_lixeiras)
        if quantidade == 0:
            return

        # Calcula posicoes das lixeiras
        largura_lixeira = config.LARGURA_TELA * config.PROPORCAO_LIXEIRA
        espacamento = config.LARGURA_TELA * 0.04
        largura_total_bloco = (largura_lixeira * quantidade) + (espacamento * (quantidade - 1))
        inicio_x = (config.LARGURA_TELA - largura_total_bloco) / 2

        for i, lixeira in enumerate(lista_lixeiras):
            lixeira.x = inicio_x + i * (largura_lixeira + espacamento)
            lixeira.y = config.ALTURA_TELA - int(lixeira.altura)