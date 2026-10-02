import pygame
from pygame.locals import *

import sys

from config import config

from models.sessao import Sessao

from services.residuo_service import ResiduoService
from services.lixeira_service import LixeiraService
from services.background_service import BackgroundService
from services.colisao_service import ColisaoService

from services.vida_service import VidaService

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
sessao = Sessao()

vida_service = VidaService(sessao)

def atualizar_fonte():
    tamanho_fonte = int(config.LARGURA_TELA * config.PROPORCAO_FONTE_PONTUACAO)
    return pygame.font.Font("assets/fonts/Pixelify_Sans/PixelifySans-Bold.ttf", tamanho_fonte)

fonte_hud_pontuacao = atualizar_fonte()

overlay = pygame.Surface(
    (config.LARGURA_TELA, config.ALTURA_TELA),
    pygame.SRCALPHA
)

overlay.fill((0, 0, 0, 80))

# =========================
# BACKGROUND
# =========================

background_service = BackgroundService()
background = background_service.redimensionar()

# =========================
# COLISAO
# =========================

colisao_service = ColisaoService()

# =========================
# LIXEIRA
# =========================

lixeira_service = LixeiraService()
lixeira_service.atualizar_posicoes()

lixeiras = lixeira_service.lixeiras
# =========================
# RESÍDUO
# =========================

residuo_service = ResiduoService()
residuo = residuo_service.escolher_residuo()


# =========================
# LOOP
# =========================

rodando = True

clock = pygame.time.Clock()
tempo_colisao = None

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

            # Atualizar fonte
            fonte_hud_pontuacao = atualizar_fonte()
            
            residuo.atualizar_tamanho()
            
            for lixeira in lixeiras:
                lixeira.atualizar_tamanho()

            lixeira_service.atualizar_posicoes()

            vida_service.atualizar_posicoes()

    # =========================
    # TECLADO
    # =========================

    keys = pygame.key.get_pressed()


    if keys[K_RIGHT]:
        residuo.mover(velocidade_x, 0)

    if keys[K_LEFT]:
        residuo.mover(-velocidade_x, 0)

    if sessao.vidas > 0:

        # =========================
        # QUEDA DO RESÍDUO
        # =========================

        if residuo.ativo:
            residuo.mover(0, velocidade_y)

        lixeira = lixeira_service.obter_lixeira(residuo)

        if lixeira:

            colidiu = colisao_service.verificar_colisao(
                residuo,
                lixeira,
                sessao
            )

            if colidiu:
                if tempo_colisao is None:
                    tempo_colisao = pygame.time.get_ticks()

        if tempo_colisao is not None:

            if pygame.time.get_ticks() - tempo_colisao >= 1000:
                residuo = residuo_service.escolher_residuo()
                background = background_service.atualizar_background(sessao.pontuacao)
                tempo_colisao = None

        if residuo.ativo and residuo.y >= config.ALTURA_TELA:

            residuo.ativo = False
            sessao.decrementar_vidas()

            residuo = residuo_service.escolher_residuo()
            background = background_service.atualizar_background(sessao.pontuacao)
    


    # =========================
    # DESENHO
    # =========================

    margem = config.LARGURA_TELA * config.MARGEM_HUD
    pontuacao_hud = fonte_hud_pontuacao.render(f"Pontuação: {sessao.pontuacao}", True, (255, 255, 255))

    tela.blit(
        background,
        (0, 0)
    )
    

    if residuo.ativo:
        tela.blit(residuo.imagem, (residuo.x, residuo.y))

    for lixeira in lixeiras:
        tela.blit(
            lixeira.imagem,
            (
                lixeira.x,
                lixeira.y
            )
        )
    
    # Desenhar pontuação alinhada com os corações
    tela.blit(
            pontuacao_hud,
            (margem, margem)
        )  

    if sessao.vidas <= 0:
        tela.blit(overlay, (0,0))


    vida_service.atualizar()
    vida_service.desenhar(tela)     

    pygame.display.flip()