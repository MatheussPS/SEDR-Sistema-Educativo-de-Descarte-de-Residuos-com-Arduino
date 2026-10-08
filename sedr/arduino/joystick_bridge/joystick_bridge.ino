// =====================================================================
// SEDR - Ponte Arduino <-> Jogo (Python/Pygame)
//
// Arduino -> Python : estado do joystick  "x,y,botao,botaoC\n"
// Python  -> Arduino: comandos de LED     "LED_<TIPO>_ON\n"
//
// LEDs das lixeiras (conforme guia de montagem elétrica):
//   Pino 12 = LED verde    = VIDRO
//   Pino 11 = LED azul     = PAPEL
//   Pino 10 = LED vermelho = PLASTICO
//   Pino  9 = LED amarelo  = METAL
//
// O Joystick Shield usa os pinos D2-D8 e A0/A1, portanto os pinos 9 a 12
// ficam livres e não entram em conflito com os botões do shield.
//
// Comandos aceitos (terminados em '\n'):
//   LED_PAPEL_ON | LED_PLASTICO_ON | LED_VIDRO_ON | LED_METAL_ON
//   LED_PAPEL_OFF | LED_PLASTICO_OFF | LED_VIDRO_OFF | LED_METAL_OFF
//   LEDS_OFF  (apaga todos)
// =====================================================================

// ---------- Joystick Shield ----------
const int PINO_EIXO_X = A0;
const int PINO_EIXO_Y = A1;
const int PINO_BOTAO = 8;
const int PINO_BOTAO_C = 4;

// ---------- LEDs das lixeiras ----------
struct LedLixeira {
  const char* tipo;   // nome do tipo de resíduo (igual ao usado no comando)
  uint8_t pino;       // pino digital do LED
};

const LedLixeira LEDS[] = {
  {"PAPEL",    11},   // azul
  {"PLASTICO", 10},   // vermelho
  {"VIDRO",    12},   // verde
  {"METAL",     9},   // amarelo
};
const uint8_t QTD_LEDS = sizeof(LEDS) / sizeof(LEDS[0]);

// Tempo máximo que um LED permanece aceso sem novo comando.
// Corresponde à pausa de 1 s do jogo após o descarte e funciona como
// proteção: se o jogo fechar/travar, o LED não fica aceso para sempre.
const unsigned long DURACAO_LED_MS = 1000;

// ---------- Temporização ----------
const unsigned long INTERVALO_ENVIO_MS = 20;   // período do envio do joystick

// ---------- Estado ----------
unsigned long instanteUltimoEnvio = 0;
unsigned long instanteLedAceso = 0;
bool algumLedAceso = false;

// Buffer de recepção dos comandos vindos do Python
const uint8_t TAM_BUFFER = 24;
char bufferComando[TAM_BUFFER];
uint8_t tamanhoComando = 0;
bool descartandoLinha = false;   // true se a linha estourou o buffer

// ---------------------------------------------------------------------
// LEDs
// ---------------------------------------------------------------------
void apagarTodosLeds() {
  for (uint8_t i = 0; i < QTD_LEDS; i++) {
    digitalWrite(LEDS[i].pino, LOW);
  }
  algumLedAceso = false;
}

void acenderLed(uint8_t indice) {
  // Só um resíduo é descartado por vez: apaga os demais antes de acender.
  apagarTodosLeds();
  digitalWrite(LEDS[indice].pino, HIGH);
  instanteLedAceso = millis();
  algumLedAceso = true;
}

void apagarLed(uint8_t indice) {
  digitalWrite(LEDS[indice].pino, LOW);
}

// Apaga automaticamente o LED após DURACAO_LED_MS (sem bloquear o loop).
void atualizarTemporizadorLed() {
  if (algumLedAceso && (millis() - instanteLedAceso >= DURACAO_LED_MS)) {
    apagarTodosLeds();
  }
}

// ---------------------------------------------------------------------
// Comandos recebidos pela serial
// ---------------------------------------------------------------------
// Interpreta "LED_<TIPO>_ON", "LED_<TIPO>_OFF" ou "LEDS_OFF".
// Comandos desconhecidos são ignorados (nenhum LED é acionado por engano).
void processarComando(const char* comando) {
  if (strcmp(comando, "LEDS_OFF") == 0) {
    apagarTodosLeds();
    return;
  }

  if (strncmp(comando, "LED_", 4) != 0) {
    return;
  }

  for (uint8_t i = 0; i < QTD_LEDS; i++) {
    const size_t tamTipo = strlen(LEDS[i].tipo);

    // O trecho após "LED_" precisa começar com o tipo exato...
    if (strncmp(comando + 4, LEDS[i].tipo, tamTipo) != 0) {
      continue;
    }

    // ...seguido de "_ON" ou "_OFF" (evita confundir tipos de nomes parecidos).
    const char* sufixo = comando + 4 + tamTipo;
    if (strcmp(sufixo, "_ON") == 0) {
      acenderLed(i);
    } else if (strcmp(sufixo, "_OFF") == 0) {
      apagarLed(i);
    }
    return;
  }
}

// Lê os bytes disponíveis sem bloquear e monta o comando até o '\n'.
void lerComandosSerial() {
  while (Serial.available() > 0) {
    const char c = (char)Serial.read();

    if (c == '\r') {
      continue;
    }

    if (c == '\n') {
      if (!descartandoLinha && tamanhoComando > 0) {
        bufferComando[tamanhoComando] = '\0';
        processarComando(bufferComando);
      }
      tamanhoComando = 0;
      descartandoLinha = false;
      continue;
    }

    if (descartandoLinha) {
      continue;
    }

    if (tamanhoComando < TAM_BUFFER - 1) {
      bufferComando[tamanhoComando++] = c;
    } else {
      // Linha maior que o buffer: descarta até o próximo '\n'.
      descartandoLinha = true;
      tamanhoComando = 0;
    }
  }
}

// ---------------------------------------------------------------------
// Joystick
// ---------------------------------------------------------------------
void enviarEstadoJoystick() {
  const int eixoX = analogRead(PINO_EIXO_X);
  const int eixoY = analogRead(PINO_EIXO_Y);
  const int botaoPressionado = digitalRead(PINO_BOTAO) == LOW ? 1 : 0;
  const int botaoCP = digitalRead(PINO_BOTAO_C) == LOW ? 1 : 0;

  Serial.print(eixoX);
  Serial.print(',');
  Serial.print(eixoY);
  Serial.print(',');
  Serial.print(botaoPressionado);
  Serial.print(',');
  Serial.println(botaoCP);
}

// ---------------------------------------------------------------------
void setup() {
  pinMode(PINO_BOTAO, INPUT_PULLUP);
  pinMode(PINO_BOTAO_C, INPUT_PULLUP);

  for (uint8_t i = 0; i < QTD_LEDS; i++) {
    pinMode(LEDS[i].pino, OUTPUT);
    digitalWrite(LEDS[i].pino, LOW);
  }

  Serial.begin(9600);
}

void loop() {
  lerComandosSerial();
  atualizarTemporizadorLed();

  // Mesmo período de 20 ms de antes, mas sem delay(): o loop continua livre
  // para receber comandos de LED com baixa latência.
  const unsigned long agora = millis();
  if (agora - instanteUltimoEnvio >= INTERVALO_ENVIO_MS) {
    instanteUltimoEnvio = agora;
    enviarEstadoJoystick();
  }
}
