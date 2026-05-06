# Subir Calificaciones UEDi

Script Python para subir calificaciones a UEDi desde un archivo de notas.

## Estructura

```
calificacion_notas_uedi/
├── main.py                    # Entry point
├── src/                      # Paquete modular
│   ├── core/                 # Lógica de negocio
│   ├── io/                   # I/O de archivos
│   └── utils/                # Utilidades
├── datos/
│   ├── notas.csv             # columnas: carnet, nota
│   └── hoja_uedi.csv        # columnas: Numero de ID, Calificacion
└── hoja_uedi_llenada_con_notas.csv  # Output
```

## Requisitos

- Python 3.11+
- UV

## Instalación

```bash
uv sync --extra dev
```

## Uso

```bash
uv run main.py
```

## Formato de notas.csv

```csv
carnet,nota
199622440,100.00
201602659,85.00
```

## Formato de hoja_uedi.csv

Columnas requeridas:
- `Numero de ID` - Identificador del estudiante
- `Calificacion` - Columna a actualizar

## tests

```bash
uv run pytest
```