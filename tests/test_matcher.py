"""Tests para el modulo de matcher."""

import pytest

from src.core.matcher import GradeMatcher, build_matcher, ResultadoMatch


class TestGradeMatcher:
    """Tests para GradeMatcher."""

    def test_add_grade(self) -> None:
        """Test agregando una nota."""
        matcher = GradeMatcher()
        matcher.add_grade("199622440", "100.00")

        result = matcher.find_grade("199622440")
        assert result.found is True
        assert result.grade == "100.00"

    def test_find_grade_normalized(self) -> None:
        """Test buscando nota con ID normalizado."""
        matcher = GradeMatcher()
        matcher.add_grade("199622440", "85.00")

        result = matcher.find_grade("0199622440")
        assert result.found is True
        assert result.grade == "85.00"

    def test_find_grade_not_found(self) -> None:
        """Test buscando nota inexistente."""
        matcher = GradeMatcher()
        matcher.add_grade("199622440", "100.00")

        result = matcher.find_grade("000000000")
        assert result.found is False
        assert result.grade == ""

    def test_unique_count(self) -> None:
        """Test propiedad unique_count."""
        matcher = GradeMatcher()
        matcher.add_grade("199622440", "100.00")
        matcher.add_grade("199622441", "90.00")

        assert matcher.unique_count == 4


class TestBuildMatcher:
    """Tests para build_matcher."""

    def test_from_records(self) -> None:
        """Test construyendo matcher desde registros."""
        records = [
            {"carnet": "199622440", "nota": "100.00"},
            {"carnet": "201602659", "nota": "85.00"},
        ]

        matcher = build_matcher(records)

        result = matcher.find_grade("199622440")
        assert result.found is True
        assert result.grade == "100.00"

        result = matcher.find_grade("201602659")
        assert result.found is True
        assert result.grade == "85.00"

    def test_empty_carnet(self) -> None:
        """Test que carnet vacio se ignora."""
        records = [
            {"carnet": "199622440", "nota": "100.00"},
            {"carnet": "", "nota": "90.00"},
        ]

        matcher = build_matcher(records)
        assert matcher.unique_count == 2

    def test_whitespace_carnet(self) -> None:
        """Test que carnet solo con whitespace se ignora."""
        records = [
            {"carnet": "199622440", "nota": "100.00"},
            {"carnet": "   ", "nota": "90.00"},
        ]

        matcher = build_matcher(records)
        assert matcher.unique_count == 2