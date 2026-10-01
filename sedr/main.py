import pygame
from pygame.locals import *

import sys

from config import config

from services.residuo_service import ResiduoService
from services.lixeira_service import LixeiraService
from services.background_service import BackgroundService

pygame.init()

tela = pygame.display.set_mode(
    (
        config.LARGURA_TELA,
        config.ALTURA_TELA
    ),
    pygame.RESIZABLE
)

pygame.display.set_caption("SEDR")

velocidade_x = 10
velocidade_y = 5
pontuacao = 0


# =========================
# BACKGROUND
# =========================

background_service = BackgroundService()
background = background_service.redimensionar()

# =========================
# LIXEIRA
# =========================

lixeira_service = LixeiraService()

lixeiras = lixeira_service.criar_lixeiras()
lixeira_service.atualizar_posicoes(lixeiras)

# =========================
# RESÍDUO
# =========================

residuo_service = ResiduoService()

residuo = residuo_service.escolher_residuo()

residuo.imagem = pygame.transform.scale(
    residuo.imagem_original,
    (
        int(residuo.largura),
        int(residuo.altura)
    )
)

# =========================
# LOOP
# =========================

rodando = True

clock = pygame.time.Clock()


while rodando:

    clock.tick(config.FPS)


    # =========================
    # EVENTOS
    # =========================

    for evento in pygame.event.get():

        if evento.type == QUIT:
            pygame.quit()
            sys.exit()


        if evento.type == VIDEORESIZE:

            config.LARGURA_TELA = evento.w
            config.ALTURA_TELA = evento.h

            tela = pygame.display.set_mode(
                (
                    config.LARGURA_TELA,
                    config.ALTURA_TELA
                ),
                pygame.RESIZABLE
            )

            # Background
            background = background_service.redimensionar()

            
            residuo.atualizar_tamanho()
            residuo.imagem = pygame.transform.scale(
                residuo.imagem_original,
                (
                    int(residuo.largura),
                    int(residuo.altura)
                )
            )
            
            
            for lixeira in lixeiras:
                lixeira.atualizar_tamanho()
                lixeira.imagem = pygame.transform.scale(
                    lixeira.imagem_original,
                    (
                        int(lixeira.largura),
                        int(lixeira.altura)
                    ) 
                )
            lixeira_service.atualizar_posicoes(lixeiras)

    # =========================
    # TECLADO
    # =========================

    keys = pygame.key.get_pressed()


    if keys[K_RIGHT]:
        residuo.mover(velocidade_x, 0)

    if keys[K_LEFT]:
        residuo.mover(-velocidade_x, 0)


    # =========================
    # QUEDA DO RESÍDUO
    # =========================

    residuo.mover(0, velocidade_y)


    if residuo.y >= config.ALTURA_TELA:
        # residuo.y = 0
        residuo = residuo_service.escolher_residuo()
        
        residuo.imagem = pygame.transform.scale(
        residuo.imagem_original,
            (
                int(residuo.largura),
                int(residuo.altura)
            )
        )

        pontuacao+=5
        background = background_service.atualizar_background(pontuacao)
    # =========================
    # DESENHO
    # =========================

    tela.blit(
        background,
        (0, 0)
    )

    tela.blit(
         residuo.imagem,
        (
            residuo.x,
            residuo.y
        )
    )

    for lixeira in lixeiras:
        tela.blit(
            lixeira.imagem,
            (
                lixeira.x,
                lixeira.y
            )
        )


    pygame.display.flip()