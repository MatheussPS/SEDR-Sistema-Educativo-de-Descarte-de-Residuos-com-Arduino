# SEDR--Sistema-Educativo-de-Descarte-de-Residuos-com-Arduino
O projeto tem como objetivo desenvolver um brinquedo interativo físico com finalidade educativa, buscando ensinar e incentivar a prática de separação correta de resíduos recicláveis de forma lúdica e acessível.

## Acionamento dos LEDs das lixeiras

Quando o jogador descarta o resíduo na lixeira **correta**, o jogo envia um comando
pela serial e o Arduino acende o LED da cor da lixeira (apaga sozinho após 1 s):

| Lixeira  | LED       | Pino | Comando enviado   |
|----------|-----------|------|-------------------|
| Papel    | Azul      | 11   | `LED_PAPEL_ON`    |
| Plástico | Vermelho  | 10   | `LED_PLASTICO_ON` |
| Vidro    | Verde     | 12   | `LED_VIDRO_ON`    |
| Metal    | Amarelo   | 9    | `LED_METAL_ON`    |

Descarte incorreto **não** acende LED. Também existem `LED_<TIPO>_OFF` e `LEDS_OFF`.

Para usar: gravar `sedr/arduino/joystick_bridge/joystick_bridge.ino` no Arduino, montar os
LEDs conforme o guia de montagem elétrica e iniciar o jogo com `SEDR_ARDUINO_PORT` definido
(ex.: `COM3`). Sem Arduino, o jogo continua funcionando normalmente pelo teclado.
