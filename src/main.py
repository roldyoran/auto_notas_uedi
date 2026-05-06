"""Paquete UEDI para subir calificaciones a UEDi."""

from pathlib import Path

from src.core.integrator import GradeIntegrator
from src.io.paths import PathConfig
from src.utils.logger import Logger


def main() -> int:
    """Ejecuta la subida de calificaciones.

    Returns:
        Codigo de salida (0 exito, 1 error).
    """
    logger = Logger()

    try:
        base_dir = Path(__file__).parent.parent
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
    import sys
    sys.exit(main())