# AGENTS.md

## Proyecto: auto_notas_uedi

### Comandos

```bash
# Instalar dependencias
uv sync

# Instalar con tests
uv sync --extra dev

# Ejecutar integracion
uv run main.py

# Menu interactivo
uv run main.py -menu

# Con rutas personalizadas
uv run main.py -n datos/notas.csv -h datos/hoja_uedi.csv

# Ejecutar tests
uv run pytest
```

### Estructura

```
auto_notas_uedi/
├── main.py                    # Entry point
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── integrator.py    # Logica de integracion
│   │   └── matcher.py       # Matching de IDs
│   ├── io/
│   │   ├── csv_handler.py   # Lectura/escritura CSV
│   │   └── paths.py        # Gestion de rutas
│   └── utils/
│       ├── normalizers.py # Normalizacion de texto/IDs
│       └── rich_output.py  # Salida estilizada con Rich
├── datos/
│   ├── notas.csv            # columnas: carnet, nota
│   └── hoja_uedi.csv       # columnas: Numero de ID, Calificacion
└── tests/
    ├── test_normalizers.py
    └── test_matcher.py
```

### Autoría

Desarrollado por @roldyoran

### Notas para agentes

- **Rich**: Dependencia requerida (no opcional)
- **Naming**: Todo el codigo usa nombres en español
- **CLI args**: `-menu`, `-n/--notas`, `-h/--hoja`
- **UTF-8 BOM**: `\ufeff` requerido para Excel
- **Output**: `hoja_uedi_llenada_con_notas.csv` en la raiz
- **Python**: 3.11+ requerido