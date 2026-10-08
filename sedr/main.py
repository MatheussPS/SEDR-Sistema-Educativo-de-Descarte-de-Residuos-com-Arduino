import pygame
from pygame.locals import *

import os
import sys

from config import config
from ui.game_over import desenhar_game_over
from ui.introducao import Introducao

from models.sessao import Sessao

from services.residuo_service import ResiduoService
from services.lixeira_service import LixeiraService
from services.background_service import BackgroundService
from services.colisao_service import ColisaoService
from services.vida_service import VidaService
from services.joystick_serial import JoystickSerial
from services.led_service import LedService

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
# ESTADOS DO JOGO
# =========================
# "introducao" - mostra telas de introdução
# "jogando" - jogo rodando
# "game_over" - jogo terminou

estado_jogo = "introducao"
introducao = Introducao()

sessao = Sessao()

def atualizar_fonte():
    tamanho_fonte = int(config.LARGURA_TELA * config.PROPORCAO_FONTE_PONTUACAO)
    return pygame.font.Font("assets/fonts/Pixelify_Sans/PixelifySans-Bold.ttf", tamanho_fonte)

fonte_hud_pontuacao = atualizar_fonte()

# =========================
# INICIALIZAÇÃO DOS SERVICES
# =========================

vida_service = VidaService(sessao)
background_service = BackgroundService()
background = background_service.redimensionar()

lixeira_service = LixeiraService()
lixeira_service.atualizar_posicoes()
lixeiras = lixeira_service.lixeiras

residuo_service = ResiduoService()
residuo = residuo_service.escolher_residuo()

opcao_selecionada = 'v'

porta_arduino = os.getenv("SEDR_ARDUINO_PORT")
if porta_arduino:
    joystick_serial = JoystickSerial(porta_arduino)
    print(f"Joystick Arduino conectado na porta {porta_arduino}.")
else:
    joystick_serial = None
    print(
        "Joystick Arduino desativado. Defina SEDR_ARDUINO_PORT "
        "(por exemplo, COM3) antes de iniciar o jogo."
    )
botao_joystick_anterior = False
botao_c_anterior = False

# LEDs das lixeiras (no Arduino). Sem Arduino conectado, não faz nada.
led_service = LedService(joystick_serial)

# Quando o jogador acerta a lixeira, acende o LED da cor correspondente
colisao_service = ColisaoService(
    ao_acertar=lambda lixeira: led_service.acender_lixeira(lixeira.tipo)
)


def reiniciar_jogo():
    global residuo, background, tempo_colisao, opcao_selecionada, estado_jogo
    
    led_service.apagar_todos()

    # Volta para a introdução
    estado_jogo = "introducao"
    introducao.resetar()
    
    sessao.reiniciar()
    
    # Resetar o background service
    background_service.game_over = False
    background_service.nivel_atual = 5
    
    residuo = residuo_service.escolher_residuo()
    background = background_service.redimensionar()
    tempo_colisao = None
    opcao_selecionada = 'v'

def ver_ranking():
    pass

acoes = {
    'r': reiniciar_jogo,
    'v': ver_ranking
}

# =========================
# LOOP PRINCIPAL
# =========================

rodando = True
clock = pygame.time.Clock()
tempo_colisao = None

while rodando:

    clock.tick(config.FPS)

    estado_joystick = (
        joystick_serial.ler_estado()
        if joystick_serial
        else None
    )
    botao_joystick_pressionado = (
        estado_joystick.botao
        and not botao_joystick_anterior
        if estado_joystick
        else False
    )
    botao_joystick_anterior = (
        estado_joystick.botao if estado_joystick else False
    )
    botao_c_pressionado = (
        estado_joystick.botao_c
        and not botao_c_anterior
        if estado_joystick
        else False
    )
    botao_c_anterior = (
        estado_joystick.botao_c if estado_joystick else False
    )
    botao_confirmacao_pressionado = (
        botao_joystick_pressionado or botao_c_pressionado
    )

    # =========================
    # EVENTOS
    # =========================

    for evento in pygame.event.get():

        if evento.type == QUIT:
            led_service.apagar_todos()
            if joystick_serial:
                joystick_serial.fechar()
            pygame.quit()
            sys.exit()

        if evento.type == KEYDOWN:
            
            # Se está na introdução, Enter avança as telas
            if estado_jogo == "introducao" and (evento.key == K_RETURN or evento.key == K_SPACE):
                continua_introducao = introducao.avancar()
                if not continua_introducao:
                    # Acabou a introdução, começa o jogo
                    estado_jogo = "jogando"
            
            elif sessao.game_over and evento.key == K_r:
                reiniciar_jogo()

            # Confirmar opção selecionada no game over
            elif sessao.game_over and (
                evento.key == K_SPACE or evento.key == K_RETURN
            ):
                acoes.get(opcao_selecionada, lambda: None)()
            
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

            # Atualizar elementos
            introducao.redimensionar()  # Redimensiona as telas de introdução
            background = background_service.redimensionar()
            fonte_hud_pontuacao = atualizar_fonte()
            
            residuo.atualizar_tamanho()
            
            for lixeira in lixeiras:
                lixeira.atualizar_tamanho()

            lixeira_service.atualizar_posicoes()
            vida_service.atualizar_posicoes()

    keys = pygame.key.get_pressed()

    if botao_confirmacao_pressionado:
        if estado_jogo == "introducao":
            continua_introducao = introducao.avancar()
            if not continua_introducao:
                estado_jogo = "jogando"
        elif sessao.game_over:
            acoes.get(opcao_selecionada, lambda: None)()
    
    # =========================
    # LÓGICA DO JOGO - só roda se estiver jogando
    # =========================
    
    if estado_jogo == "jogando" and not sessao.game_over:
        # Controle do resíduo com as setas
        if keys[K_RIGHT] or (
            estado_joystick and estado_joystick.x > 650
        ):
            residuo.mover(sessao.velocidade_x, 0)

        if keys[K_LEFT] or (
            estado_joystick and estado_joystick.x < 350
        ):
            residuo.mover(-sessao.velocidade_x, 0)

        # Movimento vertical automático do resíduo
        if residuo.ativo:
            residuo.mover(0, sessao.velocidade_y)

        # Verifica colisão com lixeira
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

        # Aguarda 1 segundo após colisão antes de gerar novo resíduo
        if tempo_colisao is not None:
            if pygame.time.get_ticks() - tempo_colisao >= 1000:
                # Verifica se entrou em game over após a colisão
                if sessao.game_over:
                    background = background_service.disparar_game_over(sessao.pontuacao)
                else:
                    residuo = residuo_service.escolher_residuo()
                    background = background_service.atualizar_background(sessao.pontuacao)
                tempo_colisao = None

        # Resíduo caiu fora da tela
        if residuo.ativo and residuo.y >= config.ALTURA_TELA:
            residuo.ativo = False
            sessao.decrementar_vidas()

            # Verifica se entrou em game over
            if sessao.game_over:
                background = background_service.disparar_game_over(sessao.pontuacao)
            else:
                # Só gera novo resíduo se ainda tiver vidas
                residuo = residuo_service.escolher_residuo()
                background = background_service.atualizar_background(sessao.pontuacao)

    # =========================
    # DESENHO
    # =========================

    # Se está na introdução, só desenha a tela de introdução
    if estado_jogo == "introducao":
        introducao.atualizar()  # Atualiza o efeito de piscar
        introducao.desenhar(tela)
    
    # Se está jogando ou em game over, desenha o jogo
    else:
        if sessao.game_over and not background_service.game_over:
            background = background_service.disparar_game_over(sessao.pontuacao)

        margem = config.LARGURA_TELA * config.MARGEM_HUD
        

        tela.blit(background, (0, 0))
        
        # Desenhar resíduo
        if residuo.ativo and not sessao.game_over:
            tela.blit(residuo.imagem, (residuo.x, residuo.y))

        
        if not sessao.game_over:
            pontuacao_hud = fonte_hud_pontuacao.render(f"Pontuação: {sessao.pontuacao}", True, (255, 255, 255))
            tela.blit(pontuacao_hud, (margem, margem))

            for lixeira in lixeiras:
                tela.blit(
                    lixeira.imagem,
                    (lixeira.x, lixeira.y)
                )
        

        vida_service.atualizar()
        vida_service.desenhar(tela)
        
        if sessao.game_over:
            
            if keys[K_UP] or (
                estado_joystick and estado_joystick.y > 650
            ):
                opcao_selecionada = 'v'
            
            if keys[K_DOWN] or (
                estado_joystick and estado_joystick.y < 350
            ):
                opcao_selecionada = 'r'
            
            desenhar_game_over(tela, sessao, config.LARGURA_TELA, config.ALTURA_TELA, opcao_selecionada)
        

    pygame.display.flip()