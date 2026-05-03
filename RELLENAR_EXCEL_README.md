# Script para Rellenar Plantilla Excel - Experimento de Cerillas

Este script lee los archivos CSV con los resultados de los participantes (P01.csv, P02.csv, etc.) y rellena automáticamente la plantilla Excel `blanco_registro_experimento_insight(1).xlsx` con los datos consolidados.

## Requisitos previos

- Python 3.7+
- pandas
- openpyxl
- matplotlib
- numpy

Instala las dependencias con:
```bash
pip install -r requirements.txt
```

## Uso

### Relleno automático de plantilla Excel

```bash
python rellenar_plantilla.py <carpeta_csv> <archivo_plantilla>
```

**Ejemplo:**
```bash
python rellenar_plantilla.py ./Respuestas "plantilla en blanco_registro_experimento_insight(1).xlsx"
```

**Salida esperada:**
- Se crea una carpeta `./registro_excel/` (automáticamente)
- Se genera un archivo Excel con nombre: `registro_resultados_YYYYMMDD_HHMMSS.xlsx`

## Estructura esperada

### Archivos CSV de entrada

Los archivos deben estar en una carpeta (ej. `Respuestas/`) con nombres simples:
```
Respuestas/
├── P01.csv
├── P02.csv
├── P03.csv
├── P04.csv
├── P05.csv
├── P06.csv
├── P07.csv
├── P08.csv
└── ...
```

Cada CSV debe contener las columnas:
```
Participante, Bloque, Tipo_Problema, Orden_Presentacion, Resuelto, Tiempo_Segundos, Observaciones
```

### Archivo plantilla Excel

El archivo `blanco_registro_experimento_insight(1).xlsx` debe tener:
- Primera hoja con nombre descriptivo (ej: "TipoA-Bloque1")
- Encabezados en las primeras filas
- Espacio para datos de participantes a partir de la fila 3 aproximadamente

## Datos que se rellenan

El script calcula y rellena automáticamente:

| Dato | Ubicación | Descripción |
|------|-----------|-------------|
| Código participante | Col A | P01, P02, etc. |
| Total de problemas | Col B | Número total de problemas (8) |
| Problemas resueltos | Col C | Cantidad resueltos |
| Tasa de resolución (%) | Col D | Porcentaje de éxito |
| Tiempo promedio (min) | Col E | Tiempo medio en minutos |
| Bloque 1 - Tipo A | Col F | Formato: resueltos/total |
| Bloque 1 - Tipo B | Col G | Formato: resueltos/total |
| Bloque 1 - Tipo C | Col H | Formato: resueltos/total |
| Bloque 1 - Tipo D | Col I | Formato: resueltos/total |
| Bloque 2 - Tipo A | Col J | Formato: resueltos/total |
| Bloque 2 - Tipo B | Col K | Formato: resueltos/total |
| Bloque 2 - Tipo C | Col L | Formato: resueltos/total |
| Bloque 2 - Tipo D | Col M | Formato: resueltos/total |

## Ejemplo de ejecución

```
======================================================================
RELLENAR PLANTILLA EXCEL - EXPERIMENTO DE CERILLAS
======================================================================

📊 Cargando archivos CSV...
📁 Encontrados 8 archivo(s) CSV
   ✓ P01.csv (8 registros)
   ✓ P02.csv (8 registros)
   ✓ P03.csv (8 registros)
   ✓ P04.csv (8 registros)
   ✓ P05.csv (8 registros)
   ✓ P06.csv (8 registros)
   ✓ P07.csv (8 registros)
   ✓ P08.csv (8 registros)

======================================================================
📊 RESUMEN DE RESULTADOS
======================================================================

P01:
  ├─ Resueltos: 4/8 (50.0%)
  ├─ Bloque 1: 2/4
  └─ Bloque 2: 2/4

P02:
  ├─ Resueltos: 4/8 (50.0%)
  ├─ Bloque 1: 2/4
  └─ Bloque 2: 2/4

[... más participantes ...]

======================================================================
📈 ESTADÍSTICAS GLOBALES:
   Participantes: 8
   Total resueltos: 42/64
   Tasa global: 65.6%
======================================================================

📝 Rellenando plantilla Excel...
📄 Cargando plantilla: plantilla en blanco_registro_experimento_insight(1).xlsx
✓ Plantilla cargada: TipoA-Bloque1
✓ P01: 4/8 resueltos (50.0%)
✓ P02: 4/8 resueltos (50.0%)
[... más participantes ...]

✓ Archivo generado: ./registro_excel\registro_resultados_20260503_121650.xlsx

✅ PROCESO COMPLETADO
```

## Archivos generados

### 1. Archivo Excel rellenado
- Ubicación: `./registro_excel/registro_resultados_YYYYMMDD_HHMMSS.xlsx`
- Contiene todos los datos consolidados de los participantes

## Flujo de trabajo completo

1. **Recolectar datos**: Los participantes descargan sus CSV desde la aplicación web
2. **Renombrar archivos**: Renombrar a `P01.csv`, `P02.csv`, etc.
3. **Generar análisis**:
   ```bash
   python analisis_resultados.py ./Respuestas
   ```
   → Genera gráficos en `./gráficos/`

4. **Rellenar plantilla**:
   ```bash
   python rellenar_plantilla.py ./Respuestas "plantilla en blanco_registro_experimento_insight(1).xlsx"
   ```
   → Genera Excel en `./registro_excel/`

## Customización

Si necesitas ajustar dónde se rellenan los datos en la plantilla, edita el script `rellenar_plantilla.py`:

- `fila_inicio = 3`: Cambia el número de fila donde comienzan los datos
- Columnas A-M: Ajusta según el diseño de tu plantilla

## Solución de problemas

### "No se encontró la plantilla"
- Verifica que el nombre del archivo sea exacto (con espacios)
- Coloca la plantilla en la misma carpeta del script o usa la ruta completa

### "No se encontraron archivos CSV"
- Verifica que los archivos se llamen P01.csv, P02.csv, etc.
- Asegúrate de que están en la carpeta correcta

### Error de openpyxl
```bash
pip install --upgrade openpyxl
```

## Archivos relacionados

- `analisis_resultados.py`: Genera gráficos de frecuencia acumulada y tiempo
- `rellenar_plantilla.py`: Rellena la plantilla Excel (este archivo)
- `requirements.txt`: Dependencias necesarias

## Contacto y soporte

Cualquier duda o problema, contacta con el investigador responsable.
