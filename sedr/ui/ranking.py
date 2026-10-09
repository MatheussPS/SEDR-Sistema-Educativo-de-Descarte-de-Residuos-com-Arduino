import pygame
from config import config


class Ranking:
    """
    Tela de ranking que exibe as pontuações em ordem decrescente.
    Calcula dinamicamente quantas pontuações cabem na tela baseado no tamanho da fonte.
    """
    
    def __init__(self, ranking_service):
        self.ranking_service = ranking_service
        self.pontuacoes = []
        self.offset = 0  # Índice de scroll
        self.pontuacao_atual = None  # Pontuação da sessão atual para destacar
        self.indice_pontuacao_atual = -1  # Índice da pontuação a destacar
        
        self.atualizar_fontes()
        self.calcular_area_renderizacao()
    
    def atualizar_fontes(self):
        """Atualiza as fontes baseado no tamanho da tela."""
        self.fonte_titulo = pygame.font.Font(
            "assets/fonts/Pixelify_Sans/PixelifySans-Bold.ttf",
            int(config.LARGURA_TELA * 0.08)
        )
        
        self.fonte_pontuacao = pygame.font.Font(
            "assets/fonts/Pixelify_Sans/PixelifySans-Medium.ttf",
            int(config.LARGURA_TELA * 0.05)
        )
        
        self.fonte_mensagem = pygame.font.Font(
            "assets/fonts/Pixelify_Sans/PixelifySans-Regular.ttf",
            int(config.LARGURA_TELA * 0.04)
        )
    
    def calcular_area_renderizacao(self):
     
        altura = config.ALTURA_TELA
        
        # Define a área de renderização das pontuações
        self.area_inicio_y = altura * 0.25  # Mais espaço após o título
        self.area_fim_y = altura * 0.88     # Antes do rodapé
        self.area_altura = self.area_fim_y - self.area_inicio_y
        
        # Renderiza um texto de exemplo para medir a altura da linha
        texto_exemplo = self.fonte_pontuacao.render("1º    999", True, (255, 255, 255))
        self.altura_linha = texto_exemplo.get_height()
        
        # Adiciona padding entre as linhas (20% da altura da linha)
        self.espacamento_linha = self.altura_linha * 1.2
        
        # Calcula quantas linhas cabem na área disponível
        self.max_visiveis = max(1, int(self.area_altura / self.espacamento_linha))
    
    def carregar_pontuacoes(self, pontuacao_atual=None):
       
        self.pontuacoes = self.ranking_service.obter_pontuacoes()
        self.pontuacao_atual = pontuacao_atual
        self.offset = 0
        
        # Encontra o índice da pontuação atual (primeira ocorrência)
        self.indice_pontuacao_atual = -1
        if self.pontuacao_atual is not None:
            try:
                self.indice_pontuacao_atual = self.pontuacoes.index(self.pontuacao_atual)
            except ValueError:
                pass  # Pontuação não encontrada na lista
    
    def scroll_up(self):
        if self.offset > 0:
            self.offset -= 1
    
    def scroll_down(self):
        # Só permite scroll se houver mais itens do que os visíveis
        if len(self.pontuacoes) > self.max_visiveis:
            max_offset = len(self.pontuacoes) - self.max_visiveis
            if self.offset < max_offset:
                self.offset += 1
    
    def desenhar(self, tela):
        
        largura = config.LARGURA_TELA
        altura = config.ALTURA_TELA
        
        # Fundo escuro semi-transparente sobre o background do jogo
        overlay = pygame.Surface((largura, altura))
        overlay.set_alpha(180)  # Transparência (0=transparente, 255=opaco)
        overlay.fill((0, 0, 0))  # Preto
        tela.blit(overlay, (0, 0))
        
        # Título
        texto_titulo = self.fonte_titulo.render("RANKING", True, (255, 255, 255))
        pos_titulo = texto_titulo.get_rect(center=(largura // 2, altura * 0.1))
        tela.blit(texto_titulo, pos_titulo)
        
        # Se não houver pontuações
        if not self.pontuacoes:
            texto_vazio = self.fonte_mensagem.render(
                "Nenhuma pontuação registrada.",
                True,
                (200, 200, 200)
            )
            pos_vazio = texto_vazio.get_rect(center=(largura // 2, altura // 2 ))
            tela.blit(texto_vazio, pos_vazio)
        else:
            # Desenha as pontuações visíveis dentro da área calculada
            pontuacoes_visiveis = self.pontuacoes[self.offset:self.offset + self.max_visiveis]
            
            for i, pontuacao in enumerate(pontuacoes_visiveis):
                # Posição no ranking (considerando o offset)
                posicao = self.offset + i + 1
                indice_global = self.offset + i
                
                # Renderiza o texto
                texto = self.fonte_pontuacao.render(
                    f"{posicao}º    {pontuacao}",
                    True,
                    (255, 255, 255)
                )
                
                # Calcula a posição Y baseado no espaçamento calculado
                pos_y = self.area_inicio_y + (i * self.espacamento_linha)
                pos_texto = texto.get_rect(center=(largura // 2, pos_y))
                
                # Destaca a pontuação da sessão atual com retângulo laranja
                # Verifica pelo índice global para destacar apenas a primeira ocorrência
                if indice_global == self.indice_pontuacao_atual:
                    # Desenha o retângulo laranja ao redor
                    rect_destaque = pos_texto.inflate(40, 15)
                    pygame.draw.rect(tela, (255, 140, 0), rect_destaque, 4)  # Laranja
                
                tela.blit(texto, pos_texto)
        
        # Instruções no rodapé
        texto_instrucao = self.fonte_mensagem.render(
            "ENTER - Novo Jogo",
            True,
            (180, 180, 180)
        )
        pos_instrucao = texto_instrucao.get_rect(center=(largura // 2, altura * 0.95))
        tela.blit(texto_instrucao, pos_instrucao)
