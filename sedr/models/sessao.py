from config import config


class Sessao:

    def __init__(self, ranking_service=None):
        self.pontuacao = 0
        self.vidas = 3
        self.game_over = False
        self.velocidade_x = config.NIVEIS_JOGO[0]["velocidade_x"]
        self.velocidade_y = config.NIVEIS_JOGO[0]["velocidade_y"]
        self.nivel_atual = 0  # Controla qual nível do jogo estamos
        self.ranking_service = ranking_service
        self.pontuacao_salva = False  # Flag para evitar salvar múltiplas vezes
    
    def atualizar_pontuacao(self, pontos):
        self.pontuacao += pontos
        # Atualiza a velocidade baseado na pontuação
        self.atualizar_velocidade()
    
    def decrementar_vidas(self):
        if self.vidas > 0:
            self.vidas -= 1
            
        if self.vidas <= 0:
            self.game_over = True
            # Salva a pontuação no ranking quando o game over acontece
            if self.ranking_service and not self.pontuacao_salva:
                self.ranking_service.salvar_pontuacao(self.pontuacao)
                self.pontuacao_salva = True
    
    def atualizar_velocidade(self):
        # Percorre os níveis de trás pra frente (do maior para o menor)
        for i in range(len(config.NIVEIS_JOGO) - 1, -1, -1):
            nivel = config.NIVEIS_JOGO[i]
            
            # Se a pontuação atingiu este nível e ainda não está nele
            if self.pontuacao >= nivel["pontuacao"] and i != self.nivel_atual:
                self.nivel_atual = i
                self.velocidade_x = nivel["velocidade_x"]
                self.velocidade_y = nivel["velocidade_y"]
                break
    
    def reiniciar(self):
        self.pontuacao = 0
        self.vidas = 3
        self.game_over = False
        self.velocidade_x = config.NIVEIS_JOGO[0]["velocidade_x"]
        self.velocidade_y = config.NIVEIS_JOGO[0]["velocidade_y"]
        self.nivel_atual = 0
        self.pontuacao_salva = False  # Reseta a flag ao reiniciar
