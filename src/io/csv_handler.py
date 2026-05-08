"""Utilidades para lectura y escritura de archivos CSV."""

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any


UTF8_BOM: str = "\ufeff"


@dataclass
class ResultadoCSV:
    """Resultado de una operacion de lectura de CSV.

    Attributes:
        records: Lista de registros como diccionarios.
        fields: Lista de nombres de campos.
    """
    records: list[dict[str, str]]
    fields: list[str]


def leer_csv(ruta: str | Path) -> ResultadoCSV:
    """Lee un archivo CSV y retorna registros como diccionarios.

    Args:
        ruta: Ruta al archivo CSV.

    Returns:
        ResultadoCSV conteniendo registros y nombres de campos.

    Raises:
        FileNotFoundError: Si el archivo no existe.
    """
    path = Path(ruta)
    registros: list[dict[str, str]] = []

    with open(path, mode="r", encoding="utf-8-sig") as archivo:
        lector = csv.DictReader(archivo)
        campos = lector.fieldnames or []
        for fila in lector:
            registros.append(dict(fila))

    return ResultadoCSV(records=registros, fields=list(campos))


def escribir_csv(
    ruta: str | Path,
    registros: list[dict[str, Any]],
    campos: list[str],
) -> None:
    """Escribe registros a un archivo CSV con UTF-8 BOM para Excel.

    Args:
        ruta: Ruta al archivo CSV de salida.
        registros: Lista de registros a escribir.
        campos: Lista de nombres de campos.
    """
    path = Path(ruta)

    with open(path, mode="w", encoding="utf-8-sig", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(registros)