# Script de Análisis de Resultados - Experimento de Cerillas

Este script genera gráficos descriptivos similares a las Figuras 2 y 4 del artículo de Knoblich et al. (1999) a partir de los datos CSV descargados del experimento de cerillas.

## Requisitos

- Python 3.7+
- pandas
- matplotlib
- numpy

## Instalación de dependencias

```bash
pip install pandas matplotlib numpy
```

O, si tienes un archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Uso

### Forma básica

Por defecto, guarda los gráficos en una carpeta llamada `gráficos/`:

```bash
python analisis_resultados.py <carpeta_con_csvs>
```

**Ejemplo:**
```bash
python analisis_resultados.py ./datos_csv
```

Esto creará automáticamente `./gráficos/` con todos los resultados.

### Especificar carpeta de salida personalizada

```bash
python analisis_resultados.py <carpeta_con_csvs> --output <carpeta_salida>
```

**Ejemplo:**
```bash
python analisis_resultados.py ./datos_csv --output ./mis_graficos
```

## Estructura de carpetas esperada

```
proyecto/
├─ analisis_resultados.py
├─ datos_csv/
│  ├─ knoblich_P01_1234567890.csv
│  ├─ knoblich_P02_1234567891.csv
│  └─ ...
└─ gráficos/  (creada automáticamente)
   ├─ fig_bloque_1_frecuencia.png
   ├─ fig_bloque_2_frecuencia.png
   ├─ fig_bloque_1_tiempo_y_tasa.png
   ├─ fig_bloque_2_tiempo_y_tasa.png
   └─ tabla_resumen.csv
```

## Archivos CSV esperados

Los archivos CSV deben ser los descargados directamente desde la aplicación con nombre `knoblich_P01_*.csv`, `knoblich_P02_*.csv`, etc.

**El código de participante se extrae automáticamente del nombre del archivo** (P01, P02, P03, etc.), reemplazando cualquier código diferente que haya dentro del CSV.

Estructura esperada del CSV:
```
Participante, Bloque, Tipo_Problema, Orden_Presentacion, Resuelto, Tiempo_Segundos, Observaciones
```

## Gráficos generados

### 1. Frecuencia acumulada de soluciones (por bloque)

- Eje X: Tiempo (minutos)
- Eje Y: Frecuencia acumulada de soluciones
- Líneas para cada tipo (A, B, C, D)
- Similar a las Figuras 2 y 4 del artículo

**Archivos:**
- `fig_bloque_1_frecuencia.png`
- `fig_bloque_2_frecuencia.png`

### 2. Tiempo medio de resolución y tasa de resolución (por bloque)

- Gráfico izquierdo: Tiempo promedio por tipo de problema
- Gráfico derecho: Porcentaje de resolución por tipo
- Barras de colores (azul = resueltos, rojo = no resueltos)

**Archivos:**
- `fig_bloque_1_tiempo_y_tasa.png`
- `fig_bloque_2_tiempo_y_tasa.png`

### 3. Tabla de resumen

- CSV con estadísticas por bloque y tipo
- Incluye: resueltos, total, tasa %, tiempo medio, desviación estándar

**Archivo:**
- `tabla_resumen.csv`

## Ejemplo de salida

El script mostrará algo como:

```
============================================================
ANÁLISIS DE RESULTADOS - EXPERIMENTO DE CERILLAS
============================================================

📊 Cargando archivos CSV...
📁 Encontrados 3 archivo(s) CSV
   ✓ knoblich_P01_1234567890.csv → P01 (8 registros)
   ✓ knoblich_P02_1234567891.csv → P02 (8 registros)
   ✓ knoblich_P03_1234567892.csv → P03 (8 registros)

✓ Total de registros: 24
✓ Participantes únicos: 3

🔄 Procesando datos...

📋 TABLA RESUMEN:
------------------------------------------------------------
 Bloque Tipo Resueltos Total Tasa (%) Tiempo medio (min) Desv.Est. (min)
      1    A         3     3    100.0               1.23           0.45
      1    B         2     3     66.7               2.15           1.20
      ...

✓ Tabla guardada en: ./gráficos/tabla_resumen.csv

📈 Generando gráficos...
✓ Gráfico guardado: ./gráficos/fig_bloque_1_frecuencia.png
✓ Gráfico guardado: ./gráficos/fig_bloque_2_frecuencia.png
✓ Gráfico guardado: ./gráficos/fig_bloque_1_tiempo_y_tasa.png
✓ Gráfico guardado: ./gráficos/fig_bloque_2_tiempo_y_tasa.png

============================================================
✅ ANÁLISIS COMPLETADO
📁 Gráficos guardados en: ./gráficos
============================================================
```

## Notas importantes

1. **Múltiples participantes:** El script automáticamente agrega los datos de todos los participantes en la carpeta CSV.

2. **Código de participante:** Se extrae del **nombre del archivo** (P01, P02, etc.), reemplazando cualquier código diferente que esté en el CSV.
   - Archivo: `knoblich_P01_1234567890.csv` → Participante: P01
   - Archivo: `knoblich_P02_1234567891.csv` → Participante: P02

3. **Sin análisis inferenciales:** Los gráficos son puramente descriptivos. No incluyen pruebas estadísticas (ANOVA, etc.), ya que el objetivo es interpretar el patrón general de los datos.

4. **Frecuencia acumulada:** Los valores muestran cuántos problemas han sido resueltos acumulativamente hasta cada punto en el tiempo.

5. **Tiempo máximo:** El gráfico de frecuencia muestra datos hasta 5 minutos (límite del experimento).

6. **Resolución de imágenes:** Los gráficos se guardan a 300 DPI, adecuados para impresión y presentaciones.

## Personalización

Si necesitas modificar colores, fuentes, tamaños o estilos, puedes editar las siguientes funciones en el script:

- `graficar_frecuencia_acumulada()`: Controla el gráfico de frecuencia acumulada
- `graficar_tiempo_promedio()`: Controla los gráficos de tiempo y tasa
- Variables `tipos_marcadores` y `colores`: Marcadores y colores de líneas

## Solución de problemas

### "No se encontraron archivos CSV"
- Verifica que los archivos tengan el formato `knoblich_*.csv`
- Asegúrate de que están en la carpeta correcta
- Los archivos deben descargarse directamente desde la aplicación web

### Errores de columnas
- Comprueba que el CSV tiene las columnas exactas (case-sensitive):
  - `Participante`, `Bloque`, `Tipo_Problema`, `Orden_Presentacion`, `Resuelto`, `Tiempo_Segundos`, `Observaciones`

### Importar módulos no encontrados
```bash
pip install --upgrade pandas matplotlib numpy
```

## Contacto y soporte

Cualquier duda o problema, contacta con el investigador responsable.
