from pathlib import Path
import pygame


class SomService:
    def __init__(self):
        pasta_sons = (
            Path(__file__).resolve().parent.parent
            / "assets"
            / "sounds"
        )

        # self.background = pasta_sons / "background.mp3"

        self.sons = {
            "acerto": pygame.mixer.Sound(
                str(pasta_sons / "acerto.mp3")
            ),
            "erro": pygame.mixer.Sound(
                str(pasta_sons / "erro.mp3")
            ),
            "select": pygame.mixer.Sound(
                str(pasta_sons / "select_menu.mp3")
            ),
            "navegacao": pygame.mixer.Sound(
                str(pasta_sons / "navegacao.mp3")
            )
        }

    # def tocar_background(self):
    #     pygame.mixer.music.load(str(self.background))
    #     pygame.mixer.music.set_volume(0.25)
    #     pygame.mixer.music.play(-1)

    def tocar(self, nome: str, volume: float = 1.0):
        som = self.sons.get(nome)
        if som is not None:
            som.set_volume(volume)
            som.play()
            # print(f"Som '{nome}' tocando com volume {volume}")

    # def parar_background(self):
    #     pygame.mixer.music.stop()