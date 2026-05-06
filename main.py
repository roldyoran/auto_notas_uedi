#!/usr/bin/env python3
"""Script principal para subir calificaciones a UEDi."""

import sys
import shutil
from pathlib import Path

from src.core.integrator import GradeIntegrator
from src.io.paths import PathConfig
from src.utils.logger import Logger


def mostrar_menu(logger: Logger) -> tuple[Path | None, Path | None]:
    """Muestra el menú interactivo para configurar rutas."""
    logger.separator()
    logger.header("MENU DE CONFIGURACION")
    logger.separator()

    opciones = [
        "Ejecutar con archivos por defecto (datos/)",
        "Especificar ruta de notas.csv",
        "Especificar ruta de hoja_uedi.csv",
        "Especificar ambas rutas",
        "Salir",
    ]

    for i, opcion in enumerate(opciones, 1):
        logger.info(f"{i}. {opcion}")

    logger.separator()

    while True:
        try:
            eleccion = input("Seleccione una opcion: ").strip()
            if not eleccion.isdigit():
                logger.warning("Debe ingresar un numero valido.")
                continue

            opcion = int(eleccion)

            if opcion == 1:
                return None, None
            elif opcion == 2:
                ruta = pedir_ruta_csv(logger, "notas")
                return ruta, None
            elif opcion == 3:
                ruta = pedir_ruta_csv(logger, "hoja")
                return None, ruta
            elif opcion == 4:
                ruta_notas = pedir_ruta_csv(logger, "notas")
                ruta_hoja = pedir_ruta_csv(logger, "hoja")
                return ruta_notas, ruta_hoja
            elif opcion == 5:
                logger.info("Saliendo...")
                sys.exit(0)
            else:
                logger.warning("Opcion fuera de rango.")

        except (KeyboardInterrupt, EOFError):
            logger.info("\nSaliendo...")
            sys.exit(0)


def pedir_ruta_csv(logger: Logger, tipo: str) -> Path:
    """Pide una ruta de archivo CSV al usuario."""
    while True:
        logger.info(f"\nIngrese la ruta al archivo {tipo}.csv:")
        logger.info("(Ejemplo: datos/mis_notas.csv)")

        ruta_str = input(">>> ").strip().strip('"').strip("'")

        if not ruta_str:
            logger.warning("Ruta vacia. Intente de nuevo.")
            continue

        ruta = Path(ruta_str)

        if not ruta.exists():
            logger.error(f"El archivo no existe: {ruta}")
            continue

        if ruta.suffix.lower() != ".csv":
            logger.warning("El archivo debe terminar en .csv")
            continue

        return ruta


def copiar_a_datos(origen: Path, destino: Path) -> Path:
    """Copia un archivo a la carpeta datos/."""
    destino.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(origen, destino)
    return destino


def main() -> int:
    """Ejecuta la subida de calificaciones."""
    logger = Logger()
    args = sys.argv[1:]

    ruta_notas = None
    ruta_hoja = None

    if "-menu" in args:
        ruta_notas, ruta_hoja = mostrar_menu(logger)
    else:
        for i, arg in enumerate(args):
            if arg in ("-n", "--notas") and i + 1 < len(args):
                ruta_notas = Path(args[i + 1].strip('"').strip("'"))
            elif arg in ("-h", "--hoja") and i + 1 < len(args):
                ruta_hoja = Path(args[i + 1].strip('"').strip("'"))

    try:
        base_dir = Path(__file__).parent

        if ruta_notas or ruta_hoja:
            datos_dir = base_dir / "datos"
            datos_dir.mkdir(exist_ok=True)

            path_notas = path_hoja = None

            if ruta_notas:
                path_notas = copiar_a_datos(ruta_notas, datos_dir / "notas.csv")
                logger.success("notas.csv copiado a datos/")
            if ruta_hoja:
                path_hoja = copiar_a_datos(ruta_hoja, datos_dir / "hoja_uedi.csv")
                logger.success("hoja_uedi.csv copiado a datos/")

            path_config = PathConfig(
                base_dir=base_dir,
                datos_dir=datos_dir,
                notas_csv=path_notas or datos_dir / "notas.csv",
                hoja_uedi_csv=path_hoja or datos_dir / "hoja_uedi.csv",
                output_csv=base_dir / "hoja_uedi_llenada_con_notas.csv",
            )
        else:
            path_config = PathConfig.from_base(base_dir)

        integrator = GradeIntegrator(path_config, logger)
        integrator.run()

        return 0

    except FileNotFoundError as e:
        logger.error(str(e))
        return 1

    except ValueError as e:
        logger.error(str(e))
        return 1

    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())