# AGENTS.md

## Proyecto: Integracion de Calificaciones UEDi

### Comandos

```bash
# Crear entorno virtual
uv venv

# Instalar dependencias
uv sync

# Ejecutar integracion
uv run integrar_notas.py
```

### Estructura obligatoria

```
notas-uedi/
├── datos/
│   ├── notas.csv        # columnas: carnet, nota
│   └── hoja_uedi.csv    # columnas: Numero de ID, Calificacion
└── integrar_notas.py
```

### Archivo de salida

`hoja_uedi_llenada_con_notas.csv` se genera en la raiz (no en datos/).

### Notas para agentes

- UTF-8 con BOM (`\ufeff`) requerido para Excel
- Columnas se normalizan (tildes compatibles)
- ID matching intenta multiples normalizaciones (0-leading, trim)
- 2 IDs sin matchson normales (formato UEDi inconsistente)
- No requiere packages externos (solo stdlib)
