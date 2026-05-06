"""Utilidades de configuracion y validacion de rutas."""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class TipoArchivo(Enum):
    """Enumeracion de tipos de archivo."""
    NOTAS_CSV = "notas.csv"
    HOJA_UEDI_CSV = "hoja_uedi.csv"
    OUTPUT_CSV = "hoja_uedi_llenada_con_notas.csv"


@dataclass(frozen=True)
class ConfigArchivo:
    """Configuracion para una ruta de archivo.

    Attributes:
        name: Nombre del archivo.
        required: Si el archivo es requerido.
        description: Descripcion legible para humanos.
    """
    name: str
    required: bool = True
    description: str = ""


RUTAS = {
    TipoArchivo.NOTAS_CSV: ConfigArchivo(
        name="notas.csv",
        required=True,
        description="Archivo con columnas: carnet, nota",
    ),
    TipoArchivo.HOJA_UEDI_CSV: ConfigArchivo(
        name="hoja_uedi.csv",
        required=True,
        description="Archivo exportado de UEDi",
    ),
    TipoArchivo.OUTPUT_CSV: ConfigArchivo(
        name="hoja_uedi_llenada_con_notas.csv",
        required=False,
        description="Archivo de salida",
    ),
}


@dataclass
class PathConfig:
    """Configuracion de rutas para el integrador."""
    base_dir: Path
    datos_dir: Path
    notas_csv: Path
    hoja_uedi_csv: Path
    output_csv: Path

    @classmethod
    def from_base(cls, base_dir: Path) -> "PathConfig":
        """Crea configuracion de rutas desde el directorio base.

        Args:
            base_dir: El directorio base del proyecto.

        Returns:
            Instancia de PathConfig con todas las rutas configuradas.
        """
        datos_dir = base_dir / "datos"
        return cls(
            base_dir=base_dir,
            datos_dir=datos_dir,
            notas_csv=datos_dir / "notas.csv",
            hoja_uedi_csv=datos_dir / "hoja_uedi.csv",
            output_csv=base_dir / "hoja_uedi_llenada_con_notas.csv",
        )


def validar_rutas(config: PathConfig) -> list[TipoArchivo]:
    """Valida que las rutas requeridas existan.

    Args:
        config: Configuracion de rutas a validar.

    Returns:
        Lista de tipos de archivo faltantes.
    """
    missing: list[TipoArchivo] = []

    if not config.datos_dir.exists():
        missing.append(TipoArchivo.NOTAS_CSV)
        missing.append(TipoArchivo.HOJA_UEDI_CSV)
        return missing

    for kind in TipoArchivo:
        if kind == TipoArchivo.OUTPUT_CSV:
            continue
        file_path = getattr(config, f"{kind.name.lower()}_csv".replace("_csv", ""))
        if not file_path.exists():
            missing.append(kind)

    return missing