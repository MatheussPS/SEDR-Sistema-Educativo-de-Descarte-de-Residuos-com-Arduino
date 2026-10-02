import pygame


def desenhar_game_over(tela, sessao, largura_tela, altura_tela, opcao_selecionada):

    fonte_titulo = pygame.font.Font(
        "assets/fonts/Pixelify_Sans/PixelifySans-Bold.ttf",
        int(largura_tela * 0.08)
    )

    fonte_texto = pygame.font.Font(
        "assets/fonts/Pixelify_Sans/PixelifySans-Medium.ttf",
        int(largura_tela * 0.04)
    )

    # Textos
    texto_game_over = fonte_titulo.render(
        "GAME OVER", True, (255, 50, 50)
    )

    texto_pontuacao = fonte_texto.render(
        f"Pontuação Final: {sessao.pontuacao}",
        True, (255, 255, 255)
    )

    texto_reiniciar = fonte_texto.render(
        "REINICIAR", True, (250, 250, 250)
    )

    texto_sair = fonte_texto.render(
        "VER RANKING", True, (250, 250, 250)
    )

    # Posições
    pos_y_titulo = altura_tela * 0.25
    pos_y_pontuacao = altura_tela * 0.40
    pos_y_sair = altura_tela * 0.55
    pos_y_reiniciar = altura_tela * 0.65

    # Rects das opções
    rect_reiniciar = texto_reiniciar.get_rect(
        center=(largura_tela // 2, pos_y_reiniciar)
    )

    rect_sair = texto_sair.get_rect(
        center=(largura_tela // 2, pos_y_sair)
    )

    if opcao_selecionada == 'r':
        pygame.draw.rect(
            tela,
            (255, 255, 255),
            rect_reiniciar.inflate(30, 15),
            3
        )

    elif opcao_selecionada == 'v':
        pygame.draw.rect(
            tela,
            (255, 255, 255),
            rect_sair.inflate(30, 15),
            3
        )

    tela.blit(
        texto_game_over,
        texto_game_over.get_rect(
            center=(largura_tela // 2, pos_y_titulo)
        )
    )

    tela.blit(
        texto_pontuacao,
        texto_pontuacao.get_rect(
            center=(largura_tela // 2, pos_y_pontuacao)
        )
    )
    
    tela.blit(texto_sair, rect_sair)
    tela.blit(texto_reiniciar, rect_reiniciar)
    