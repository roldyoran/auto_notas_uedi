"""Logica principal de integracion de notas."""

from dataclasses import dataclass, field
from typing import Any

from src.core.matcher import GradeMatcher, build_matcher
from src.io.csv_handler import leer_csv, escribir_csv
from src.io.paths import PathConfig
from src.utils.normalizers import buscar_columna
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


@dataclass
class RegistroSinMatch:
    """Un registro que no pudo ser relacionado a una nota."""
    id_value: str
    name: str = ""
    username: str = ""


@dataclass
class ResultadoIntegracion:
    """Resultado del proceso de integracion."""
    total_read: int
    updated: int
    unmatched: list[RegistroSinMatch] = field(default_factory=list)


class GradeIntegrator:
    """Integra notas de un archivo a otro basado en el ID del estudiante."""

    def __init__(self, path_config: PathConfig) -> None:
        """Inicializa el integrador."""
        self._paths = path_config

    def run(self) -> ResultadoIntegracion:
        """Ejecuta el proceso de integracion de notas."""
        print_encabezado("SUBIR CALIFICACIONES")
        self._check_files()

        print_paso(1, "Leyendo notas.csv")
        notas_result = leer_csv(self._paths.notas_csv)
        print_substep(f"{len(notas_result.records)} registros leidos")

        print_paso(2, "Leyendo hoja_uedi.csv")
        hoja_result = leer_csv(self._paths.hoja_uedi_csv)
        print_substep(f"{len(hoja_result.records)} registros leidos")

        print_paso(3, "Construyendo mapa de notas")
        matcher = build_matcher(notas_result.records)
        print_substep(f"{matcher.unique_count} unique IDs de notas")

        col_calificacion = buscar_columna(hoja_result.fields, "Calificacion")
        if not col_calificacion:
            msg = f"Columna 'Calificacion' no encontrada. Campos: {hoja_result.fields}"
            print_error(msg)
            raise ValueError(msg)

        col_id = buscar_columna(hoja_result.fields, "Numero de ID")
        if not col_id:
            msg = f"Columna 'Numero de ID' no encontrada. Campos: {hoja_result.fields}"
            print_error(msg)
            raise ValueError(msg)

        print_paso(4, "Actualizando calificaciones...")
        result = self._update_grades(
            hoja_result.records,
            matcher,
            col_id,
            col_calificacion,
        )

        print_substep(f"{result.updated} IDs encontrados y actualizados")
        print_substep(f"{len(result.unmatched)} IDs no encontrados (asignado 0)")

        if result.unmatched:
            print_paso(5, "IDs sin coincidencia:")
            for item in result.unmatched:
                print_substep(f"ID: {item.id_value}")
                if item.name:
                    print_substep(f"  Nombre: {item.name}")
                if item.username:
                    print_substep(f"  Usuario: {item.username}")
            print_advertencia("Revisar manualmente los IDs sin coincidencia")

        print_paso(6, "Escribiendo archivo de salida...")
        escribir_csv(
            self._paths.output_csv,
            hoja_result.records,
            hoja_result.fields,
        )

        print_resumen(
            result.total_read,
            result.updated,
            len(result.unmatched),
            str(self._paths.output_csv),
        )

        return result

    def _check_files(self) -> None:
        """Verifica que los archivos requeridas existan."""
        print_info("Verificando estructura de archivos")

        if not self._paths.datos_dir.exists():
            print_error("No se encontro la carpeta 'datos/'")
            raise FileNotFoundError(
                "Carpeta 'datos/' no encontrada. "
                "Cree una carpeta llamada 'datos' y coloque dentro: "
                "notas.csv, hoja_uedi.csv"
            )

        if not self._paths.notas_csv.exists():
            print_error("No se encontro datos/notas.csv")
            raise FileNotFoundError(
                "Archivo 'datos/notas.csv' no encontrado. "
                "Debe contener columnas: carnet, nota"
            )

        if not self._paths.hoja_uedi_csv.exists():
            print_error("No se encontro datos/hoja_uedi.csv")
            raise FileNotFoundError(
                "Archivo 'datos/hoja_uedi.csv' no encontrado. "
                "Debe contener columnas: Numero de ID, Calificacion"
            )

        print_exito("Archivos encontrados correctamente")

    def _update_grades(
        self,
        records: list[dict[str, Any]],
        matcher: GradeMatcher,
        col_id: str,
        col_grade: str,
    ) -> ResultadoIntegracion:
        """Actualiza las notas en los registros."""
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