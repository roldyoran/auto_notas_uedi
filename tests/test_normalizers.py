"""Tests para el modulo de normalizers."""

import pytest

from src.utils.normalizers import (
    normalizar_nombre_columna,
    buscar_columna,
    normalizar_id,
    obtener_variantes_id,
)


class TestNormalizarNombreColumna:
    """Tests para normalizar_nombre_columna."""

    def test_sin_acentos(self) -> None:
        """Test que nombres sin acentos retornan igual."""
        assert normalizar_nombre_columna("Calificacion") == "Calificacion"

    def test_con_acentos(self) -> None:
        """Test que acentos se eliminan."""
        assert normalizar_nombre_columna("Calificación") == "Calificacion"
        assert normalizar_nombre_columna("Número") == "Numero"
        assert normalizar_nombre_columna("Acción") == "Accion"

    def test_acentos_mayusculas(self) -> None:
        """Test que acentos mayusculas se manejan."""
        assert normalizar_nombre_columna("CALIFICACIÓN") == "CALIFICACION"
        assert normalizar_nombre_columna("ÁÉÍÓÚ") == "AEIOU"

    def test_ñ(self) -> None:
        """Test que ñ se maneja."""
        assert normalizar_nombre_columna("año") == "ano"
        assert normalizar_nombre_columna("AÑo") == "ANo"


class TestBuscarColumna:
    """Tests para buscar_columna."""

    def test_exact_match(self) -> None:
        """Test coincidencia exacta de columna."""
        campos = ["carnet", "nota", "Calificacion"]
        assert buscar_columna(campos, "Calificacion") == "Calificacion"

    def test_accent_match(self) -> None:
        """Test coincidencia de columna con diferencia de acento."""
        campos = ["carnet", "nota", "Calificación"]
        assert buscar_columna(campos, "Calificacion") == "Calificación"

    def test_no_match(self) -> None:
        """Test que columna no existente retorna None."""
        campos = ["carnet", "nota"]
        assert buscar_columna(campos, "Inexistente") is None


class TestNormalizarId:
    """Tests para normalizar_id."""

    def test_leading_zeros(self) -> None:
        """Test que ceros a la izquierda se eliminan."""
        assert normalizar_id("0199622440") == "199622440"
        assert normalizar_id("00123456") == "123456"
        assert normalizar_id("00000001") == "1"

    def test_no_leading_zeros(self) -> None:
        """Test IDs sin ceros a la izquierda."""
        assert normalizar_id("199622440") == "199622440"
        assert normalizar_id("123456") == "123456"

    def test_none_input(self) -> None:
        """Test que None retorna cadena vacia."""
        assert normalizar_id(None) == ""

    def test_whitespace(self) -> None:
        """Test que whitespace se corta."""
        assert normalizar_id("  199622440  ") == "199622440"


class TestObtenerVariantesId:
    """Tests para obtener_variantes_id."""

    def test_nine_digit_id_starting_1(self) -> None:
        """Test ID de 9 digitos comenzando con 1."""
        variantes = obtener_variantes_id("199622440")
        assert "199622440" in variantes
        assert "099622440" in variantes

    def test_nine_digit_id_starting_0(self) -> None:
        """Test ID de 9 digitos comenzando con 0."""
        variantes = obtener_variantes_id("0199622440")
        assert "0199622440" in variantes
        assert "199622440" in variantes

    def test_eight_digit_id(self) -> None:
        """Test ID de 8 digitos."""
        variantes = obtener_variantes_id("19962244")
        assert "19962244" in variantes
        assert "119962244" in variantes