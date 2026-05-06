# Subir Calificaciones UEDi

Script Python para subir calificaciones a UEDi desde un archivo de notas.

## Estructura

```
calificacion_notas_uedi/
├── main.py                    # Entry point
├── src/
│   ├── core/                 # Logica de negocio
│   ├── io/                   # I/O de archivos
│   └── utils/                # Utilidades (Rich)
├── datos/
│   ├── notas.csv             # columnas: carnet, nota
│   └── hoja_uedi.csv        # columnas: Numero de ID, Calificacion
└── hoja_uedi_llenada_con_notas.csv  # Output
```

## Requisitos

- Python 3.11+
- UV (gestor de paquetes)

## Instalación

```bash
uv sync
```

## Uso

```bash
# Ejecutar con archivos por defecto (datos/)
uv run main.py

# Menu interactivo
uv run main.py -menu

# Con rutas personalizadas
uv run main.py -n ruta/notas.csv -h ruta/hoja_uedi.csv
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

## Tests (opcional)

```bash
uv sync --extra dev
uv run pytest
```