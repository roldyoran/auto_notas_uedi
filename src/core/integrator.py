"""Logica principal de integracion de notas."""

from dataclasses import dataclass, field
from typing import Any

from src.core.matcher import GradeMatcher, build_matcher
from src.io.csv_handler import leer_csv, escribir_csv
from src.io.paths import PathConfig
from src.utils.logger import Logger
from src.utils.normalizers import buscar_columna

try:
    from src.utils.rich_output import print_resumen
    RICH_DISPONIBLE = True
except ImportError:
    RICH_DISPONIBLE = False


@dataclass
class RegistroSinMatch:
    """Un registro que no pudo ser relacionado a una nota.

    Attributes:
        id_value: El ID del estudiante.
        name: El nombre del estudiante si esta disponible.
        username: El nombre de usuario si esta disponible.
    """
    id_value: str
    name: str = ""
    username: str = ""


@dataclass
class ResultadoIntegracion:
    """Resultado del proceso de integracion.

    Attributes:
        total_read: Total de registros procesados.
        updated: Numero de registros con notas actualizadas.
        unmatched: Lista de registros sin coincidencia.
    """
    total_read: int
    updated: int
    unmatched: list[RegistroSinMatch] = field(default_factory=list)


class GradeIntegrator:
    """Integra notas de un archivo a otro basado en el ID del estudiante."""

    def __init__(
        self,
        path_config: PathConfig,
        logger: Logger | None = None,
    ) -> None:
        """Inicializa el integrador.

        Args:
            path_config: Configuracion de rutas.
            logger: Instancia de Logger (opcional).
        """
        self._paths = path_config
        self._logger = logger or Logger()

    def run(self) -> ResultadoIntegracion:
        """Ejecuta el proceso de integracion de notas.

        Returns:
            ResultadoIntegracion con totales y registros sin match.
        """
        self._logger.header("SUBIR CALIFICACIONES")
        self._check_files()

        self._logger.step(1, "Leyendo notas.csv")
        notas_result = leer_csv(self._paths.notas_csv)
        self._logger.substep(f"{len(notas_result.records)} registros leidos")

        self._logger.step(2, "Leyendo hoja_uedi.csv")
        hoja_result = leer_csv(self._paths.hoja_uedi_csv)
        self._logger.substep(f"{len(hoja_result.records)} registros leidos")

        self._logger.step(3, "Construyendo mapa de notas")
        matcher = build_matcher(notas_result.records)
        self._logger.substep(f"{matcher.unique_count} unique IDs de notas")

        col_calificacion = buscar_columna(hoja_result.fields, "Calificacion")
        if not col_calificacion:
            msg = f"Columna 'Calificacion' no encontrada. Campos: {hoja_result.fields}"
            self._logger.error(msg)
            raise ValueError(msg)

        col_id = buscar_columna(hoja_result.fields, "Numero de ID")
        if not col_id:
            msg = f"Columna 'Numero de ID' no encontrada. Campos: {hoja_result.fields}"
            self._logger.error(msg)
            raise ValueError(msg)

        self._logger.step(4, "Actualizando calificaciones...")
        result = self._update_grades(
            hoja_result.records,
            matcher,
            col_id,
            col_calificacion,
        )

        self._logger.substep(f"{result.updated} IDs encontrados y actualizados")
        self._logger.substep(
            f"{len(result.unmatched)} IDs no encontrados (asignado 0)"
        )

        if result.unmatched:
            self._logger.step(5, "IDs sin coincidencia:")
            for item in result.unmatched:
                self._logger.substep(f"ID: {item.id_value}")
                if item.name:
                    self._logger.substep(f"  Nombre: {item.name}")
                if item.username:
                    self._logger.substep(f"  Usuario: {item.username}")
            self._logger.separator()
            self._logger.warning(
                "Revisar manualmente los IDs sin coincidencia"
            )
            self._logger.separator()

        self._logger.step(6, "Escribiendo archivo de salida...")
        escribir_csv(
            self._paths.output_csv,
            hoja_result.records,
            hoja_result.fields,
        )

        if RICH_DISPONIBLE:
            print_resumen(
                result.total_read,
                result.updated,
                len(result.unmatched),
                str(self._paths.output_csv),
            )
        else:
            self._logger.separator()
            self._logger.header("RESUMEN")
            self._logger.success(f" Total de registros: {result.total_read}")
            self._logger.success(f"Actualizados: {result.updated}")
            if result.unmatched:
                self._logger.warning(f"Sin coincidencia: {len(result.unmatched)}")
            self._logger.separator()
            self._logger.banner(" Proceso completado exitosamente! ")
            self._logger.success(f"{self._paths.output_csv}")

        return result

    def _check_files(self) -> None:
        """Verifica que los archivos requeridos existan."""
        self._logger.info("Verificando estructura de archivos")

        if not self._paths.datos_dir.exists():
            self._logger.error("No se encontro la carpeta 'datos/'")
            raise FileNotFoundError(
                "Carpeta 'datos/' no encontrada. "
                "Cree una carpeta llamada 'datos' y coloque dentro: "
                "notas.csv, hoja_uedi.csv"
            )

        if not self._paths.notas_csv.exists():
            self._logger.error("No se encontro datos/notas.csv")
            raise FileNotFoundError(
                "Archivo 'datos/notas.csv' no encontrado. "
                "Debe contener columnas: carnet, nota"
            )

        if not self._paths.hoja_uedi_csv.exists():
            self._logger.error("No se encontro datos/hoja_uedi.csv")
            raise FileNotFoundError(
                "Archivo 'datos/hoja_uedi.csv' no encontrado. "
                "Debe contener columnas: Numero de ID, Calificacion"
            )

        self._logger.success("Archivos encontrados correctamente")

    def _update_grades(
        self,
        records: list[dict[str, Any]],
        matcher: GradeMatcher,
        col_id: str,
        col_grade: str,
    ) -> ResultadoIntegracion:
        """Actualiza las notas en los registros.

        Args:
            records: Lista de registros a actualizar.
            matcher: Matcher con notas.
            col_id: Nombre de columna para el ID del estudiante.
            col_grade: Nombre de columna para la nota.

        Returns:
            ResultadoIntegracion con estadisticas de actualizacion.
        """
        updated = 0
        unmatched: list[RegistroSinMatch] = []

        for registro in records:
            id_value = registro.get(col_id, "").strip()
            result = matcher.find_grade(id_value)

            if result.found:
                registro[col_grade] = result.grade
                updated += 1
            else:
                registro[col_grade] = "0"
                unmatched.append(RegistroSinMatch(
                    id_value=id_value,
                    name=registro.get("Nombre completo", ""),
                    username=registro.get("Usuario", ""),
                ))

        return ResultadoIntegracion(
            total_read=len(records),
            updated=updated,
            unmatched=unmatched,
        )