class LedService:
    """Aciona, no Arduino, o LED da lixeira que recebeu o descarte correto.

    Cada tipo de lixeira tem um LED de cor correspondente (ver guia de
    montagem elétrica):

        papel    -> LED azul     (pino 11)
        plastico -> LED vermelho (pino 10)
        vidro    -> LED verde    (pino 12)
        metal    -> LED amarelo  (pino  9)

    O jogo envia apenas o comando de texto; os pinos ficam definidos no
    sketch do Arduino (joystick_bridge.ino). O LED apaga sozinho depois de
    1 segundo (mesma pausa do jogo antes do próximo resíduo).
    """

    COMANDOS_LED = {
        "papel": "LED_PAPEL_ON",
        "plastico": "LED_PLASTICO_ON",
        "vidro": "LED_VIDRO_ON",
        "metal": "LED_METAL_ON",
    }

    COMANDO_APAGAR_TODOS = "LEDS_OFF"

    def __init__(self, joystick_serial=None):
        # joystick_serial é None quando o Arduino não está configurado:
        # nesse caso os métodos não fazem nada e o jogo segue normalmente.
        self._joystick_serial = joystick_serial

    def acender_lixeira(self, tipo: str) -> bool:
        """Acende o LED do tipo de lixeira informado (ex.: 'plastico')."""
        comando = self.COMANDOS_LED.get(tipo)

        if comando is None:
            print(f"Aviso: sem LED configurado para o tipo '{tipo}'.")
            return False

        return self._enviar(comando)

    def apagar_todos(self) -> bool:
        """Apaga todos os LEDs (usado ao reiniciar ou encerrar o jogo)."""
        return self._enviar(self.COMANDO_APAGAR_TODOS)

    def _enviar(self, comando: str) -> bool:
        if self._joystick_serial is None:
            return False

        return self._joystick_serial.enviar_linha(comando)
