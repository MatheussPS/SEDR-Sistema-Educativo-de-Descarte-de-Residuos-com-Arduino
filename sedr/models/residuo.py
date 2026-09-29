import pygame

class Residuo:
    def __init__(self, caminho_imagem, x, y, tipo_material):
        # Carrega a imagem e otimiza a transparência
        self.imagem = pygame.image.load(caminho_imagem).convert_alpha()
        
        # Coordenadas atuais na tela
        self.x = x
        self.y = y
        
        # Cria o retângulo com o tamanho exato da imagem
        self.rect = self.imagem.get_rect()
        # Posiciona o retângulo nas coordenadas iniciais
        self.rect.topleft = (self.x, self.y)
        
        # Define se é "plastico", "metal", "vidro" ou "papel"
        self.tipo_material = tipo_material
        
        # Controle para saber se o lixo ainda está em jogo ou já foi descartado
        self.ativo = True

    def desenhar(self, tela):
        # Só desenha se o resíduo estiver ativo
        if self.ativo:
            tela.blit(self.imagem, (self.x, self.y))

    def atualizar_posicao(self, novo_x, novo_y):
        # Atualiza o X e Y da imagem
        self.x = novo_x
        self.y = novo_y
        
        # Sincroniza o retângulo invisível com a nova posição da imagem
        # Isso é fundamental para a colisão com a lixeira funcionar no lugar certo
        self.rect.topleft = (self.x, self.y)

    def obter_rect(self):
        # Retorna o retângulo atualizado para checar a colisão no GameManager
        return self.rect