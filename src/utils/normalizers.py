"""Utilidades de normalizacion de texto para nombres de columnas y IDs de estudiantes."""


CARACTERES_CON_TILDE: dict[str, str] = {
    "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
    "Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U",
    "ñ": "n", "Ñ": "N",
}


def normalizar_nombre_columna(nombre: str) -> str:
    """Elimina los acentos de un nombre de columna.

    Args:
        nombre: El nombre de la columna a normalizar.

    Returns:
        El nombre de columna normalizado sin acentos.

    Ejemplo:
        >>> normalizar_nombre_columna("Calificación")
        'Calificacion'
    """
    resultado = nombre
    for tilde, sin_tilde in CARACTERES_CON_TILDE.items():
        resultado = resultado.replace(tilde, sin_tilde)
    return resultado


def buscar_columna(campos: list[str], nombre_base: str) -> str | None:
    """Busca una columna por nombre base con o sin acentos.

    Args:
        campos: Lista de nombres de columnas disponibles.
        nombre_base: El nombre base a buscar.

    Returns:
        El nombre de columna real si se encuentra, None si no.
    """
    nombre_normalizado = normalizar_nombre_columna(nombre_base)
    for campo in campos:
        if normalizar_nombre_columna(campo) == nombre_normalizado:
            return campo
    return None


def normalizar_id(id_valor: str | None) -> str:
    """Normaliza el ID del estudiante eliminando ceros a la izquierda.

    Args:
        id_valor: El ID del estudiante a normalizar.

    Returns:
        El ID normalizado sin ceros a la izquierda.

    Ejemplo:
        >>> normalizar_id("0199622440")
        '199622440'
    """
    if id_valor is None:
        return ""
    id_str = str(id_valor).strip()
    if len(id_str) > 9:
        id_str = id_str[-9:]
    while len(id_str) > 1 and id_str.startswith("0"):
        id_str = id_str[1:]
    return id_str


def obtener_variantes_id(id_valor: str) -> list[str]:
    """Genera todas las variantes posibles de ID para matching.

    Args:
        id_valor: El ID del estudiante para generar variantes.

    Returns:
        Lista de todas las variantes posibles de ID.

    Ejemplo:
        >>> obtener_variantes_id("0199622440")
        ['0199622440', '199622440', '199622440']
    """
    variantes: set[str] = {id_valor}

    if len(id_valor) > 9:
        ultimos_9 = id_valor[-9:]
        variantes.add(ultimos_9)

    id_norm = normalizar_id(id_valor)
    if id_norm != id_valor:
        variantes.add(id_norm)

    if len(id_valor) == 9:
        if id_valor.startswith("00"):
            variantes.add("1" + id_valor[1:])
        elif id_valor[0] == "0":
            variantes.add("1" + id_valor[1:])
        elif id_valor[0] == "1":
            variantes.add("0" + id_valor[1:])

    if len(id_valor) == 9 and id_valor.startswith("00"):
        variantes.add("19" + id_valor[2:])

    if len(id_valor) == 8:
        variantes.add("1" + id_valor)

    return list(variantes)