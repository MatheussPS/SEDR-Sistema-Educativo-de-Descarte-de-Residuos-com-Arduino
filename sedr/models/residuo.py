from config import config


class Residuo:

    def __init__(self, tipo, imagem, centro_x):
        self.tipo = tipo

        self.imagem_original = imagem
        self.imagem = imagem

        self.largura, self.altura = self.calcular_tamanho()

        self.x = centro_x - self.largura / 2
        self.y = 0

        self.ativo = True

    def calcular_tamanho(self):
        largura = config.LARGURA_TELA * config.PROPORCAO_RESIDUO

        proporcao = self.imagem_original.get_width() / self.imagem_original.get_height()
        
        altura = largura/proporcao
        
        return largura, altura

    def atualizar_tamanho(self):
        centro_x = self.x + self.largura / 2

        self.largura, self.altura = self.calcular_tamanho()

        self.x = centro_x - self.largura / 2

    def centralizar_x(self):
        centro_x = config.LARGURA_TELA / 2

        self.x = centro_x - self.largura / 2

    def mover(self, dx, dy):
        self.x += dx
        self.y += dy