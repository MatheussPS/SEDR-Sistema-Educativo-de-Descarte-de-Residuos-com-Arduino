import pygame
from config import config

class Introducao:
    
    def __init__(self):
        # Carrega as imagens originais (guardadas para redimensionar)
        self.imagem_original_0 = pygame.image.load("assets/background/niveis/niveL00.jpeg").convert()
        self.imagem_original_1 = pygame.image.load("assets/background/niveis/niveL01.jpeg").convert()
        
        # Imagens redimensionadas (usadas para desenhar)
        self.imagem_0 = None
        self.imagem_1 = None
        
        # Redimensiona para o tamanho da tela
        self.redimensionar()
        
        # Começa na tela 0
        self.tela_atual = 0
        
        # Controle do texto piscante
        self.tempo_piscar = 0
        self.mostrar_texto = True
    
    def redimensionar(self):
        self.imagem_0 = pygame.transform.scale(
            self.imagem_original_0, 
            (config.LARGURA_TELA, config.ALTURA_TELA)
        )
        self.imagem_1 = pygame.transform.scale(
            self.imagem_original_1, 
            (config.LARGURA_TELA, config.ALTURA_TELA)
        )
        
        # Recria a fonte quando redimensiona
        tamanho_fonte = int(config.LARGURA_TELA * 0.03)  # 3% da largura da tela
        self.fonte = pygame.font.Font("assets/fonts/Pixelify_Sans/PixelifySans-Bold.ttf", tamanho_fonte)
    
    def atualizar(self):
        self.tempo_piscar += 1
        
        # Alterna entre mostrar e esconder a cada 30 frames (meio segundo a 60 FPS)
        if self.tempo_piscar >= 30:
            self.mostrar_texto = not self.mostrar_texto
            self.tempo_piscar = 0
    
    def desenhar(self, screen):
        if self.tela_atual == 0:
            screen.blit(self.imagem_0, (0, 0))
            
            # Desenha o texto piscante apenas na primeira tela
            if self.mostrar_texto:
                texto = self.fonte.render("Pressione ENTER para iniciar", True, (255, 255, 255))
                
                # Centraliza o texto na parte inferior da tela
                texto_rect = texto.get_rect()
                texto_rect.centerx = config.LARGURA_TELA // 2
                texto_rect.centery = config.ALTURA_TELA // 2 + config.ALTURA_TELA // 6
                
                # Desenha um fundo preto semi-transparente atrás do texto
                fundo = pygame.Surface((texto_rect.width + 20, texto_rect.height + 10))
                fundo.set_alpha(150)
                fundo.fill((0, 0, 0))
                screen.blit(fundo, (texto_rect.x - 10, texto_rect.y - 5))
                
                # Desenha o texto
                screen.blit(texto, texto_rect)
        else:
            screen.blit(self.imagem_1, (0, 0))
    
    def avancar(self):
        if self.tela_atual == 0:
            self.tela_atual = 1
            return True  # Ainda há mais telas
        else:
            return False  # Acabou, pode iniciar o jogo
    
    def resetar(self):
        self.tela_atual = 0
        self.tempo_piscar = 0
        self.mostrar_texto = True
