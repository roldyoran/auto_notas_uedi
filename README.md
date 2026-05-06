# Integracion de Calificaciones UEDI

Script Python para integrar calificaciones a UEDI
Este script lee los archivos `notas.csv`, un archivo que usted como aux debe crear y `hoja_uedi.csv`, que es el archivo exportado de UEDi con el nombre cambiado para un uso mas sencillo.

## Estructura de Archivos

```
notas-uedi/
├── datos/
│   ├── notas.csv        # Archivo con carnet y notas
│   └── hoja_uedi.csv   # Archivo exportado de UEDi
├── integrar_notas.py    # Script de integracion
├── .venv/             # Entorno virtual
└── hoja_uedi_llenada_con_notas.csv  # Archivo de salida
```

## Requisitos

- Python 3.10+
- UV (administrador de paquetes)

## Instalacion

1. Crear el entorno virtual:
   ```bash
   uv sync
   uv venv
   ```

2. No es necesario instalar paquetes adicionales (solo stdlib)

## Uso

1. Colocar los archivos CSV en la carpeta `datos/`:
   - `datos/notas.csv` - Debe tener columnas: `carnet`, `nota`
   - `datos/hoja_uedi.csv` - Archivo exportado de UEDi

2. Ejecutar el script:
   ```bash
   uv run integrar_notas.py
   ```

3. El archivo de salida `hoja_uedi_llenada_con_notas.csv` se generara en la raiz

## Formato de Archivo notas.csv

```csv
carnet,nota
199622440,100.00
201602659,85.00
```

## Formato de Archivo hoja_uedi.csv

El archivo debe contener las columnas:
- `Numero de ID` - Identificador del estudiante
- `Calificacion` - Columna a actualizar (puede estar vacia)

## Mensajes en Consola

El script mostrara:
- Cantidad de registros leidos
- IDs encontrados y actualizados
- IDs sin coincidencia (si los hay)
- Advertencia si hay archivos que revisar manualmente

## Solucionar Problemas

### "No se encontro la carpeta 'datos/'"
- Crear una carpeta llamada `datos` en la raiz del proyecto
- Colocar `notas.csv` y `hoja_uedi.csv` dentro

### "No se encontro la columna 'Calificacion'"
- Verificar que el archivo tenga exactamente esa columna
- El nombre es sensible a mayusculas/minusculas pero soporta tildes

### IDs sin coincidencia
- Revisar manualmente los IDs listados en la salida
- Puede haber errores de formato entre los sistemas
