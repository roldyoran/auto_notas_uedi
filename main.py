#!/usr/bin/env python3
"""Script principal para subir calificaciones a UEDi."""

import shutil
from pathlib import Path

from src.core.integrator import GradeIntegrator
from src.io.paths import PathConfig
from src.utils.rich_output import (
    print_encabezado,
    print_paso,
    print_info,
    print_exito,
    print_advertencia,
    print_error,
    print_substep,
    print_resumen,
    mostrar_menu,
    pedir_ruta,
)


def copiar_a_datos(origen: Path, destino: Path) -> Path:
    """Copia un archivo a la carpeta datos/."""
    destino.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(origen, destino)
    return destino


def main() -> int:
    """Ejecuta la subida de calificaciones."""
    import sys
    args = sys.argv[1:]

    ruta_notas = None
    ruta_hoja = None

    if "-menu" in args:
        ruta_notas, ruta_hoja = mostrar_menu()
    else:
        for i, arg in enumerate(args):
            if arg in ("-n", "--notas") and i + 1 < len(args):
                ruta_notas = Path(args[i + 1].strip('"').strip("'"))
            elif arg in ("-h", "--hoja") and i + 1 < len(args):
                ruta_hoja = Path(args[i + 1].strip('"').strip("'"))

    try:
        base_dir = Path(__file__).parent
        print_encabezado("SUBIR CALIFICACIONES")

        if ruta_notas or ruta_hoja:
            datos_dir = base_dir / "datos"
            datos_dir.mkdir(exist_ok=True)

            path_notas = path_hoja = None

            if ruta_notas:
                path_notas = copiar_a_datos(ruta_notas, datos_dir / "notas.csv")
                print_exito("notas.csv copiado a datos/")
            if ruta_hoja:
                path_hoja = copiar_a_datos(ruta_hoja, datos_dir / "hoja_uedi.csv")
                print_exito("hoja_uedi.csv copiado a datos/")

            path_config = PathConfig(
                base_dir=base_dir,
                datos_dir=datos_dir,
                notas_csv=path_notas or datos_dir / "notas.csv",
                hoja_uedi_csv=path_hoja or datos_dir / "hoja_uedi.csv",
                output_csv=base_dir / "hoja_uedi_llenada_con_notas.csv",
            )
        else:
            path_config = PathConfig.from_base(base_dir)

        integrator = GradeIntegrator(path_config)
        result = integrator.run()

        return 0

    except FileNotFoundError as e:
        print_error(str(e))
        return 1

    except ValueError as e:
        print_error(str(e))
        return 1

    except Exception as e:
        print_error(f"Error inesperado: {e}")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())