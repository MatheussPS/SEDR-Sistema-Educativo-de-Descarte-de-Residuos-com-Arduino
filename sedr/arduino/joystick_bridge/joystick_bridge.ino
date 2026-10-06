const int PINO_EIXO_X = A0;
const int PINO_EIXO_Y = A1;
const int PINO_BOTAO = 8;
const int PINO_BOTAO_C = 4;

void setup() {
  pinMode(PINO_BOTAO, INPUT_PULLUP);
  pinMode(PINO_BOTAO_C, INPUT_PULLUP);
  Serial.begin(9600);
}

void loop() {
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

  delay(20);
}
