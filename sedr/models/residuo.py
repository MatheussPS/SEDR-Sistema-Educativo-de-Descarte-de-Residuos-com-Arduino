from config.config import Config


class Residuo:

    def __init__(self, tipo, centro_x):
        self.tipo = tipo

        self.largura = self.calcular_tamanho()
        self.altura = self.calcular_tamanho()

        self.x = centro_x - self.largura / 2
        self.y = 0

        self.ativo = True

    def calcular_tamanho(self):
        return Config.LARGURA_TELA * Config.PROPORCAO_RESIDUO

    def atualizar_tamanho(self):
        centro_x = self.x + self.largura / 2

        self.largura = self.calcular_tamanho()
        self.altura = self.calcular_tamanho()

        self.x = centro_x - self.largura / 2

    def centralizar_x(self):
        centro_x = Config.LARGURA_TELA / 2

        self.x = centro_x - self.largura / 2

    def mover(self, dx, dy):
        self.x += dx
        self.y += dy