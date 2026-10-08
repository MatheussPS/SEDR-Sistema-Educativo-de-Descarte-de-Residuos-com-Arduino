from dataclasses import dataclass


@dataclass(frozen=True)
class EstadoJoystick:
    x: int = 512
    y: int = 512
    botao: bool = False
    botao_c: bool = False


class JoystickSerial:
    BAUD_RATE = 9600

    def __init__(self, porta: str):
        try:
            import serial
        except ImportError:
            print(
                "Aviso: pyserial não está instalado. "
                "O jogo continuará sem o joystick."
            )
            self._serial = None
            self._buffer = bytearray()
            self._estado = EstadoJoystick()
            self._registro_invalido_reportado = False
            return

        try:
            self._serial = serial.Serial(
                porta,
                self.BAUD_RATE,
                timeout=0
            )
        except (serial.SerialException, OSError) as erro:
            print(
                f"Aviso: não foi possível abrir a porta {porta} "
                f"({erro}). O jogo continuará usando o teclado."
            )
            self._serial = None
        self._buffer = bytearray()
        self._estado = EstadoJoystick()
        self._registro_invalido_reportado = False

    def ler_estado(self) -> EstadoJoystick:
        if self._serial is None:
            return self._estado

        import serial

        while True:
            try:
                bytes_disponiveis = self._serial.in_waiting
                if not bytes_disponiveis:
                    break
                self._buffer.extend(self._serial.read(bytes_disponiveis))
            except (serial.SerialException, OSError) as erro:
                print(
                    f"Aviso: conexão com o Arduino perdida ({erro}). "
                    "O jogo continuará usando o teclado."
                )
                self._serial = None
                self._buffer.clear()
                self._estado = EstadoJoystick()
                return self._estado

        while b"\n" in self._buffer:
            linha, _, restante = self._buffer.partition(b"\n")
            self._buffer = bytearray(restante)
            try:
                self._estado = self._interpretar_linha(linha)
            except ValueError as erro:
                if not self._registro_invalido_reportado:
                    print(f"Aviso: {erro}. Registro serial ignorado.")
                    self._registro_invalido_reportado = True
            else:
                self._registro_invalido_reportado = False

        return self._estado

    @staticmethod
    def _interpretar_linha(linha: bytes) -> EstadoJoystick:
        try:
            campos = linha.decode("ascii").strip().split(",")
            if len(campos) == 3:
                x_texto, y_texto, botao_texto = campos
                botao_c_texto = "0"
            elif len(campos) == 4:
                x_texto, y_texto, botao_texto, botao_c_texto = campos
            else:
                raise ValueError("Quantidade inesperada de campos")

            x = int(x_texto)
            y = int(y_texto)
            botao = int(botao_texto)
            botao_c = int(botao_c_texto)
        except (UnicodeDecodeError, ValueError) as erro:
            raise ValueError(
                f"Dados inválidos recebidos do Arduino: {linha!r}"
            ) from erro

        if (
            not 0 <= x <= 1023
            or not 0 <= y <= 1023
            or botao not in (0, 1)
            or botao_c not in (0, 1)
        ):
            raise ValueError(
                f"Valores fora da faixa recebidos do Arduino: {linha!r}"
            )

        return EstadoJoystick(
            x=x,
            y=y,
            botao=bool(botao),
            botao_c=bool(botao_c)
        )

    def fechar(self) -> None:
        if self._serial is not None:
            self._serial.close()
