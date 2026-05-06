"""Utilidades para matching de IDs de estudiantes."""

from dataclasses import dataclass
from typing import Any

from src.utils.normalizers import (
    obtener_variantes_id,
    normalizar_id,
)


@dataclass
class ResultadoMatch:
    """Resultado de una operacion de matching de nota.

    Attributes:
        found: Si la nota fue encontrada.
        grade: El valor de la nota si se encontro, cadena vacia si no.
    """
    found: bool
    grade: str


class GradeMatcher:
    """Hace matching de IDs de estudiantes a notas con multiples estrategias de normalizacion."""

    def __init__(self) -> None:
        """Inicializa el matcher con un mapa de notas vacio."""
        self._grades: dict[str, str] = {}

    def add_grade(self, student_id: str, grade: str) -> None:
        """Agrega una nota al matcher.

        Args:
            student_id: El ID del estudiante.
            grade: El valor de la nota.
        """
        self._grades[student_id] = grade

        for variante in obtener_variantes_id(student_id):
            if variante and variante != student_id:
                self._grades[variante] = grade

    def find_grade(self, student_id: str) -> ResultadoMatch:
        """Busca una nota para un ID de estudiante.

        Args:
            student_id: El ID del estudiante a buscar.

        Returns:
            ResultadoMatch con la nota si se encontro.
        """
        if student_id in self._grades:
            return ResultadoMatch(found=True, grade=self._grades[student_id])

        id_norm = normalizar_id(student_id)
        if id_norm in self._grades:
            return ResultadoMatch(found=True, grade=self._grades[id_norm])

        variantes = obtener_variantes_id(student_id)
        for variante in variantes:
            if variante in self._grades:
                return ResultadoMatch(found=True, grade=self._grades[variante])

        return ResultadoMatch(found=False, grade="")

    @property
    def unique_count(self) -> int:
        """Obtiene el numero de IDs unicos de estudiantes."""
        return len(self._grades)


def build_matcher(records: list[dict[str, Any]]) -> GradeMatcher:
    """Construye un GradeMatcher desde registros de notas.

    Args:
        records: Lista de registros con campos 'carnet' y 'nota'.

    Returns:
        Instancia de GradeMatcher configurada.
    """
    matcher = GradeMatcher()

    for registro in records:
        carnet = registro.get("carnet", "").strip()
        nota = registro.get("nota", "0")
        if carnet and carnet != "":
            matcher.add_grade(carnet, nota)

    return matcher