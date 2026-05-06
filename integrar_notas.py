#!/usr/bin/env python3
"""
Script para integrar calificaciones en UEDI
Los archivos deben estar en la carpeta 'datos' con los nombres 'notas.csv' y 'hoja_uedi.csv'.
CSV tipo de separacion por comas.

Estructura de archivos:
    datos/
        notas.csv       -> Contiene carnet y nota
        hoja_uedi.csv   -> Contiene los datos de UEDI solo que se cambia por el nombre de hoja_uedi

Relaciona por carnet/Numero de ID y actualiza la columna Calificacion.

Uso:
    uv run python integrar_notas.py

Salida:
    hoja_uedi_llenada_con_notas.csv -> Archivo actualizado en la raiz con el formato que acepta UEDI para ser subido
"""

import csv
import sys
from pathlib import Path


def leer_csv(ruta: str) -> list[dict]:
    """Lee un archivo CSV y retorna una lista de diccionarios."""
    registros = []
    with open(ruta, mode="r", encoding="utf-8-sig") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            registros.append(fila)
    return registros


def escribir_csv(ruta: str, registros: list[dict], campos: list[str]):
    """Escribe una lista de diccionarios a un archivo CSV con UTF-8 BOM para Excel."""
    with open(ruta, mode="w", encoding="utf-8-sig", newline="") as archivo:
        archivo.write("\ufeff")
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(registros)


def normalizar_columna(nombre: str) -> str:
    """Normaliza un nombre de columna quitando tildes."""
    replacements = {
        "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
        "Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U",
        "ñ": "n", "Ñ": "N"
    }
    resultado = nombre
    for original, reemplazo in replacements.items():
        resultado = resultado.replace(original, reemplazo)
    return resultado


def buscar_columna(campos: list[str], nombre_base: str) -> str | None:
    """Busca una columna usando nombre base con o sin tildes."""
    nombre_normalizado = normalizar_columna(nombre_base)
    for campo in campos:
        if normalizar_columna(campo) == nombre_normalizado:
            return campo
    return None


def normalizar_id(id_valor: str) -> str:
    """Normaliza el ID: elimina ceros a la izquierda."""
    if id_valor is None:
        return ""
    id_str = str(id_valor).strip()
    while len(id_str) > 1 and id_str.startswith("0"):
        id_str = id_str[1:]
    return id_str


def buscar_nota(id_busqueda: str, mapa: dict) -> str | None:
    """Busca nota en el mapa intentando multiples normalizaciones."""
    if id_busqueda in mapa:
        return mapa[id_busqueda]

    id_norm = normalizar_id(id_busqueda)
    if id_norm in mapa:
        return mapa[id_norm]

    if len(id_busqueda) == 9 and id_busqueda.startswith("0"):
        id_try = "1" + id_busqueda[1:]
        if id_try in mapa:
            return mapa[id_try]

    if len(id_norm) == 8:
        id_try = "1" + id_norm
        if id_try in mapa:
            return mapa[id_try]

    if len(id_busqueda) == 9:
        if id_busqueda[0] == "0":
            id_try = "1" + id_busqueda[1:]
            if id_try in mapa:
                return mapa[id_try]
        if id_busqueda[0] == "1":
            id_try = "0" + id_busqueda[1:]
            if id_try in mapa:
                return mapa[id_try]

    return None
    """Busca nota en el mapa intentando multiples normalizaciones."""
    if id_busqueda in mapa:
        return mapa[id_busqueda]

    id_norm = normalizar_id(id_busqueda)
    if id_norm in mapa:
        return mapa[id_norm]

    if len(id_busqueda) == 9 and id_busqueda.startswith("0"):
        id_try = "1" + id_busqueda[1:]
        if id_try in mapa:
            return mapa[id_try]

    if len(id_norm) == 8:
        id_try = "1" + id_norm
        if id_try in mapa:
            return mapa[id_try]

    if len(id_busqueda) == 9:
        if id_busqueda[0] == "0":
            id_try = "1" + id_busqueda[1:]
            if id_try in mapa:
                return mapa[id_try]
        if id_busqueda[0] == "1":
            id_try = "0" + id_busqueda[1:]
            if id_try in mapa:
                return mapa[id_try]

    return None


def main():
    BASE_DIR = Path(__file__).parent
    DATOS_DIR = BASE_DIR / "datos"
    NOTAS_CSV = DATOS_DIR / "notas.csv"
    HOJA_UEDI_CSV = DATOS_DIR / "hoja_uedi.csv"
    HOJA_UEDI_OUTPUT = BASE_DIR / "hoja_uedi_llenada_con_notas.csv"

    print("=" * 76)
    print("INTEGRACION DE CALIFICACIONES")
    print("=" * 76)

    print("\n[INFO] Verificando estructura de archivos")
    print("       Carpeta esperada: datos/")
    print("       Archivos necesarios dentro de 'datos/':")
    print("         - notas.csv       (debe tener columnas: carnet, nota)")
    print("         - hoja_uedi.csv  (debe tener columnas: Numero de ID, Calificacion)")

    if not DATOS_DIR.exists():
        print("\n[ERROR] No se encontro la carpeta 'datos/'")
        print("        Cree una carpeta llamada 'datos' y coloque dentro:")
        print("          - notas.csv")
        print("          - hoja_uedi.csv")
        sys.exit(1)

    if not NOTAS_CSV.exists():
        print("\n[ERROR] No se encontro el archivo 'datos/notas.csv'")
        print("        Este archivo debe contener:")
        print("          - Columna 'carnet': numero de identificacion del estudiante")
        print("          - Columna 'nota': calificacion obtenida")
        print("        Ejemplo contenido:")
        print("          carnet,nota")
        print("          199622440,100.00")
        print("          201602659,85.00")
        sys.exit(1)

    if not HOJA_UEDI_CSV.exists():
        print("\n[ERROR] No se encontro el archivo 'datos/hoja_uedi.csv'")
        print("        Este archivo debe contener:")
        print("          - Columna 'Numero de ID': identificacion del estudiante")
        print("          - Columna 'Calificacion': columna a actualizar")
        print("        El archivo debe tener el formato exportado de UEDI")
        sys.exit(1)

    print("\n[OK] Archivos encontrados correctamente")
    print("     - datos/notas.csv")
    print("     - datos/hoja_uedi.csv")

    print("\n[1] Leyendo notas.csv")
    notas_registros = leer_csv(str(NOTAS_CSV))
    print(f"     - {len(notas_registros)} registros leidos")

    print("\n[2] Leyendo hoja_uedi.csv")
    hoja_registros = leer_csv(str(HOJA_UEDI_CSV))
    print(f"     - {len(hoja_registros)} registros leidos")

    print("\n[3] Construyendo mapa de notas")
    mapa_notas = {}
    for registro in notas_registros:
        carnet = registro.get("carnet", "").strip()
        nota = registro.get("nota", "0")
        if carnet:
            mapa_notas[carnet] = nota

            id_norm = normalizar_id(carnet)
            if id_norm != carnet:
                mapa_notas[id_norm] = nota

            if len(carnet) == 9:
                if carnet[0] == "1":
                    mapa_notas["0" + carnet[1:]] = nota

            if len(id_norm) == 8:
                mapa_notas["1" + id_norm] = nota

    print(f"     - {len(mapa_notas)} unique IDs de notas")

    campos = list(hoja_registros[0].keys()) if hoja_registros else []

    col_calificacion = buscar_columna(campos, "Calificacion")
    if not col_calificacion:
        print("\n[ERROR] No se encontro la columna 'Calificacion' en hoja_uedi.csv")
        print("        Verifique que el archivo tenga una columna llamada 'Calificacion'")
        print(f"        Columnas disponibles: {campos}")
        sys.exit(1)

    col_id = buscar_columna(campos, "Numero de ID")
    if not col_id:
        print(f"\n[ERROR] No se encontro la columna 'Numero de ID' en hoja_uedi.csv")
        print("        Verifique que el archivo tenga una columna llamada 'Numero de ID'")
        print(f"        Columnas disponibles: {campos}")
        sys.exit(1)

    print("\n[4] Actualizando calificaciones...")
    actualizados = 0
    no_encontrados = 0
    ids_sin_match = []

    for registro in hoja_registros:
        id_original = registro.get(col_id, "").strip()
        nota_encontrada = buscar_nota(id_original, mapa_notas)

        if nota_encontrada:
            registro[col_calificacion] = nota_encontrada
            actualizados += 1
        else:
            registro[col_calificacion] = "0"
            no_encontrados += 1
            ids_sin_match.append({
                "id": id_original,
                "nombre": registro.get("Nombre completo", ""),
                "usuario": registro.get("Usuario", "")
            })

    print(f"     - {actualizados} IDs encontrados y actualizados")
    print(f"     - {no_encontrados} IDs no encontrados (asignado 0)")

    if ids_sin_match:
        print("\n[5] IDs sin coincidencia:")
        print("     (Estos se asignaron 0 por no encontrar coincidencia)")
        for item in ids_sin_match:
            print(f"     - ID: {item['id']}")
            print(f"       Nombre: {item['nombre']}")
            print(f"       Usuario: {item['usuario']}")

        print("\n" + "=" * 76)
        print("ADVERTENCIA: Revisar y comparar manualmente los siguientes IDs")
        print("Pueden existir errores en UEDI con los carnet/nombres")
        print("o diferencias en el formato de los identificadores")
        print("=" * 76)

    print("\n[6] Escribiendo archivo de salida...\n\n")
    escribir_csv(str(HOJA_UEDI_OUTPUT), hoja_registros, campos)

    print("=" * 28, "PROCESO COMPLETADO", "=" * 28)
    print()
    print(f"Archivo de salida: {HOJA_UEDI_OUTPUT}")
    print("=" * 76)


if __name__ == "__main__":
    main()
