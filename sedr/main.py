import pygame
from pygame.locals import *

import sys

from config import config

from services.residuo_service import ResiduoService

pygame.init()


tela = pygame.display.set_mode(
    (
        config.LARGURA_TELA,
        config.ALTURA_TELA
    ),
    pygame.RESIZABLE
)

pygame.display.set_caption("SEDR")


# =========================
# BACKGROUND
# =========================

img_bkg_original = pygame.image.load(
    "assets/background/bg_park_dirt_00.jpeg"
).convert()

img_bkg = pygame.transform.scale(
    img_bkg_original,
    (
        config.LARGURA_TELA,
        config.ALTURA_TELA
    )
)


# =========================
# RESÍDUO
# =========================

residuo_service = ResiduoService()

residuo = residuo_service.escolher_residuo(
    config.LARGURA_TELA / 2
)

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

            img_bkg = pygame.transform.scale(
                img_bkg_original,
                (
                    config.LARGURA_TELA,
                    config.ALTURA_TELA
                )
            )

            # Objetos

            residuo.atualizar_tamanho()
            residuo.centralizar_x()

            residuo.imagem = pygame.transform.scale(
                            residuo.imagem_original,
                            (
                                int(residuo.largura),
                                int(residuo.altura)
                            )
                        )

    # =========================
    # TECLADO
    # =========================

    keys = pygame.key.get_pressed()


    if keys[K_RIGHT]:
        residuo.mover(10, 0)

    if keys[K_LEFT]:
        residuo.mover(-10, 0)


    # =========================
    # QUEDA DO RESÍDUO
    # =========================

    residuo.mover(0, 5)


    if residuo.y >= config.ALTURA_TELA:
        # residuo.y = 0
        residuo = residuo_service.escolher_residuo(config.LARGURA_TELA / 2)
        
        residuo.imagem = pygame.transform.scale(
        residuo.imagem_original,
            (
                int(residuo.largura),
                int(residuo.altura)
            )
        )

    # =========================
    # DESENHO
    # =========================

    tela.blit(
        img_bkg,
        (0, 0)
    )


    tela.blit(
         residuo.imagem,
        (
            residuo.x,
            residuo.y
        )
    )


    pygame.display.flip()