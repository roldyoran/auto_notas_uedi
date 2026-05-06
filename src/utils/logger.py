"""Utilidades de logging estructurado."""

import sys
from enum import Enum
from typing import TextIO


class NivelLog(Enum):
    """Enumeracion de niveles de log."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"


class Logger:
    """Logger estructurado simple para salida a consola."""

    def __init__(self, output: TextIO | None = None) -> None:
        """Inicializa el logger con flujo de salida opcional.

        Args:
            output: Flujo de salida (default: sys.stdout)
        """
        self._output = output or sys.stdout

    def _print(self, level: NivelLog, message: str) -> None:
        """Imprime un mensaje de log con prefijo de nivel.

        Args:
            level: Nivel de log.
            message: Mensaje a imprimir.
        """
        prefix = f"[{level.value}]"
        print(f"{prefix} {message}", file=self._output)

    def debug(self, message: str) -> None:
        """Log mensaje de debug."""
        self._print(NivelLog.DEBUG, message)

    def info(self, message: str) -> None:
        """Log mensaje de info."""
        self._print(NivelLog.INFO, message)

    def warning(self, message: str) -> None:
        """Log mensaje de warning."""
        self._print(NivelLog.WARNING, message)

    def error(self, message: str) -> None:
        """Log mensaje de error."""
        self._print(NivelLog.ERROR, message)

    def success(self, message: str) -> None:
        """Log mensaje de success."""
        self._print(NivelLog.SUCCESS, message)

    def header(self, title: str, width: int = 76) -> None:
        """Imprime un encabezado.

        Args:
            title: Titulo del encabezado.
            width: Ancho total del encabezado.
        """
        print("=" * width, file=self._output)
        print(title, file=self._output)
        print("=" * width, file=self._output)

    def separator(self, width: int = 76) -> None:
        """Imprime una linea de separador.

        Args:
            width: Ancho del separador.
        """
        print("=" * width, file=self._output)

    def step(self, step_num: int, message: str) -> None:
        """Imprime un mensaje de paso.

        Args:
            step_num: Numero de paso.
            message: Mensaje del paso.
        """
        print(f"\n[{step_num}] {message}", file=self._output)

    def substep(self, message: str) -> None:
        """Imprime un mensaje de sub-paso.

        Args:
            message: Mensaje de sub-paso.
        """
        print(f"     - {message}", file=self._output)


LOGGER_DEFAULT = Logger()