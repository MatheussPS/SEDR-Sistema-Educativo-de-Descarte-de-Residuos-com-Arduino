import pygame
import time

from pygame.locals import *

from sys import exit

pygame.init()

largura = 640
altura = 480


tela = pygame.display.set_mode((largura, altura), pygame.RESIZABLE)
width, height = tela.get_size()

x = width/2 - 40/2
y = 0


pygame.display.set_caption('SEDR')
frame = pygame.time.Clock()
imagem = pygame.image.load("assets/residuos/metais/parafusos.png")


while True:
    frame.tick(30)
    tela.fill((0, 0, 0))

    if y >= height:
        y = 0
    y+=20

    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            exit()

        if evento.type == VIDEORESIZE:
            width = evento.w
            height = evento.h

            x = width / 2 - 40 / 2
            y = height / 2 - 50 / 2

    keys = pygame.key.get_pressed()
    if keys[ K_RIGHT]:
        x+=20
    if keys[K_LEFT]:
        x-=20
                
    tela.blit(imagem, (x, y))

    pygame.display.flip()
