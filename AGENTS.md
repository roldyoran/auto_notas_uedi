# AGENTS.md

## Proyecto: Subir Calificaciones UEDi

### Comandos

```bash
# Instalar dependencias (incluye dev para tests)
uv sync --extra dev

# Ejecutar integracion
uv run main.py

# Ejecutar tests
uv run pytest

# Ejecutar un test especifico
uv run pytest tests/test_normalizers.py -v
```

### Estructura

```
calificacion_notas_uedi/
├── main.py                    # Entry point (delega a src/)
├── src/
│   ├── __init__.py
│   ├── main.py               # Funcion principal
│   ├── core/
│   │   ├── integrator.py    # Logica de integracion
│   │   └── matcher.py       # Matching de IDs a notas
│   ├── io/
│   │   ├── csv_handler.py   # Lectura/escritura CSV
│   │   └── paths.py       # Gestión de rutas
│   └── utils/
│       ├── normalizers.py  # Normalizacion de texto/IDs
│       └── logger.py      # Logging estructurado
├── datos/
│   ├── notas.csv         # columnas: carnet, nota
│   └── hoja_uedi.csv     # columnas: Numero de ID, Calificacion
└── tests/
    ├── test_normalizers.py
    └── test_matcher.py
```

### Notas para agentes

- **Naming**: Todo el código usa nombres en español (`leer_csv`, `buscar_columna`, `normalizar_id`, etc.)
- **UTF-8 BOM**: `\ufeff` requerido para Excel
- **Normalización**: columnas con tildes compatibles, IDs con múltiples variantes (0-leading, trim)
- **Output**: `hoja_uedi_llenada_con_notas.csv` se genera en la raíz
- **Dependencias**: solo stdlib + pytest (dev)
- **Python**: 3.11+ requerido