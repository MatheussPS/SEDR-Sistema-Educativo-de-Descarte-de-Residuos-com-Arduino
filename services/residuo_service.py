import os
import random
import pygame

from models.residuo import Residuo

class ResiduoService:

    CAMINHO_RESIDUOS = "assets/residuos"

    def escolher_residuo(self, centro_x):

        # Escolhe o tipo de resíduo
        tipo = random.choice(os.listdir(self.CAMINHO_RESIDUOS))

        # Monta o caminho da pasta
        caminho_tipo = os.path.join(self.CAMINHO_RESIDUOS, tipo)

        # Lista os resíduos daquele tipo
        residuos = os.listdir(caminho_tipo)

        # Escolhe um resíduo
        arquivo = random.choice(residuos)

        # Caminho completo da imagem
        caminho_imagem = os.path.join(
            caminho_tipo,
            arquivo
        )

        imagem = pygame.image.load(caminho_imagem).convert_alpha()

        return Residuo(
            tipo,
            imagem,
            centro_x
        )