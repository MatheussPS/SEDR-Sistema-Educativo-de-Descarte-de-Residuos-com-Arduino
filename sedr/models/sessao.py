class Sessao:

    def __init__(self):
        self.pontuacao = 0
        self.vidas = 3
    
    def atualizar_pontuacao(self, pontos):
        self.pontuacao+=pontos
    def decrementar_vidas(self):
        self.vidas-=1

        print(self.vidas)