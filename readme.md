# Experimento de Cerillas: Psicología del Pensamiento (UNED)

Tarea de **insight** basada en el experimento clásico de Knoblich et al. (1999) sobre resolución de problemas mediante movimiento de cerillas y numeración romana.

---

## 📋 Contenidos

- [Para Participantes](#-para-participantes)
- [Para Investigadores](#-para-investigadores)
  - [Estructura del Proyecto](#estructura-del-proyecto)
  - [Configuración Inicial](#configuración-inicial)
  - [Procesamiento de Datos](#procesamiento-de-datos)
  - [Análisis de Resultados](#análisis-de-resultados)
  - [Automatización Excel](#automatización-excel)

---

## 🎯 Para Participantes

### ¿Qué es?

Esta es una práctica de la asignatura de **Psicología del Pensamiento** de UNED. Se trata de una tarea de insight que requiere resolver problemas moviendo cerillas en ecuaciones de numeración romana.

### Cómo Participar

**URL:** https://andresamaya288.github.io/PEC_UNED_PENSAMIENTO/

#### Instrucciones Paso a Paso

1. Abre el enlace anterior en tu navegador (se recomienda **ordenador** o móvil con zoom)
2. Introduce tu **código de participante** (ej: P01, P02, etc.)
3. Pulsa **Iniciar experimento**

#### Para Cada Problema

- **Selecciona cerilla:** Haz clic en una cerilla para resaltarla
- **Coloca cerilla:** Haz clic en un hueco verde para colocar la cerilla
- **Si cometes error:** Pulsa **↺ Reiniciar** para volver a empezar
- **Comprueba solución:** Pulsa **Comprobar** cuando creas que es correcta, o **Abandonar** si decides no continuar
- **Observaciones:** Es muy importante anotar tus pensamientos:
  - ¿Te bloqueaste?
  - ¿Qué te hizo cambiar de estrategia?
  - ¿Cuándo viste la solución?
  - Cualquier dato relevante
- **Siguiente:** Pulsa **Siguiente →** para continuar

#### Finalización

5. Al terminar los 8 problemas, aparecerá una pantalla con resultados
6. Pulsa **Descargar CSV** para descargar el archivo de datos
7. **Envía el archivo** por WhatsApp, correo u otro medio

### Notas Importantes

- ⏱️ **Límite de tiempo:** 5 minutos por problema. Si se agota, se marca como no resuelto
- 🎯 **Solo 1 cerilla:** No puedes mover más de una cerilla por problema
- 📝 **Observaciones detalladas:** Son fundamentales para la investigación
- 📥 **CSV obligatorio:** Debes descargar y enviar este archivo

---

## 👨‍🔬 Para Investigadores

### Estructura del Proyecto

```
PEC_UNED_PENSAMIENTO/
│
├── README.md                                    (este archivo)
├── requirements.txt                             (dependencias Python)
│
├── app/                                         (aplicación web)
│   ├── index.html                              (experimento interactivo)
│   └── demo.html                               (demo técnica)
│
├── scripts/                                    (procesamiento de datos)
│   ├── actualizar_participantes.py             (normaliza códigos)
│   ├── analisis_resultados.py                  (genera gráficos)
│   ├── rellenar_plantilla.py                   (rellena Excel)
│   └── mostrar_datos_acumulados.py             (valida datos)
│
├── data/
│   ├── Respuestas/                             (CSVs de participantes)
│   │   ├── P01.csv
│   │   ├── P02.csv
│   │   └── ...
│   ├── gráficos/                               (generados automáticamente)
│   │   ├── fig_bloque_1_frecuencia.png
│   │   ├── fig_bloque_2_frecuencia.png
│   │   ├── fig_bloque_1_tiempo_y_tasa.png
│   │   ├── fig_bloque_2_tiempo_y_tasa.png
│   │   └── tabla_resumen.csv
│   └── registro_excel/                         (generados automáticamente)
│       └── registro_resultados_*.xlsx
│
└── docs/
    ├── plantilla en blanco_registro_experimento_insight(1).xlsx
    └── WHATSAPP_MENSAJE.txt
```

### Configuración Inicial

#### Requisitos Previos

- Python 3.7+
- pip (gestor de paquetes)

#### Instalación de Dependencias

```bash
pip install -r requirements.txt
```

**Dependencias:**
- pandas (≥1.3.0) - procesamiento de datos
- matplotlib (≥3.4.0) - generación de gráficos
- numpy (≥1.21.0) - cálculos numéricos
- openpyxl (≥3.0.0) - manipulación de Excel

---

## 📊 Procesamiento de Datos

### Flujo General de Trabajo

```
1. Participantes descarguen CSV desde app web
2. Renombrar archivos: P01.csv, P02.csv, etc.
3. Ponerlos en: data/Respuestas/
4. Ejecutar scripts en este orden:
   a) actualizar_participantes.py
   b) analisis_resultados.py
   c) rellenar_plantilla.py
```

### Paso 1: Actualizar Códigos de Participantes

Normaliza los códigos de participante en los CSVs según el nombre del archivo.

```bash
python scripts/actualizar_participantes.py
```

**Entrada:** `data/Respuestas/P0X.csv` (con códigos originales)
**Salida:** `data/Respuestas/P0X.csv` (con códigos normalizados P01-P10, etc.)

**Ejemplo:**
- P09.csv con contenido "Primo1" → renombra a "P09"
- P10.csv con contenido "Hermanapri" → renombra a "P10"

---

## 📈 Análisis de Resultados

### Generación de Gráficos (Knoblich et al., 1999)

Genera gráficos descriptivos similares a las Figuras 2 y 4 del artículo original.

```bash
python scripts/analisis_resultados.py data/Respuestas
```

**Salida automática:** `data/gráficos/`

#### Gráficos Generados

| Archivo | Descripción |
|---------|-------------|
| `fig_bloque_1_frecuencia.png` | Frecuencia acumulada de soluciones - Bloque 1 |
| `fig_bloque_2_frecuencia.png` | Frecuencia acumulada de soluciones - Bloque 2 |
| `fig_bloque_1_tiempo_y_tasa.png` | Tiempo promedio y tasa de solución - Bloque 1 |
| `fig_bloque_2_tiempo_y_tasa.png` | Tiempo promedio y tasa de solución - Bloque 2 |
| `tabla_resumen.csv` | Tabla resumen con estadísticas por tipo y bloque |

#### Gráficos Detallados

**Frecuencia Acumulada de Soluciones:**
- Eje X: Tiempo (minutos, 0-5)
- Eje Y: Frecuencia acumulada
- Líneas por tipo (A, B, C, D) con estilos diferenciados:
  - Tipo A: Rojo (━━), cuadrado
  - Tipo B: Azul (┄┄), círculo
  - Tipo C: Verde (⋯⋯), triángulo
  - Tipo D: Naranja (┊╱), diamante
- Resolución: 300 DPI

**Tiempo Promedio y Tasa:**
- Gráfico dual por bloque
- Barras agrupadas por tipo
- Valores en minutos y porcentaje

#### Estructura de CSV Esperada

Los archivos deben tener estas columnas:
```
Participante, Bloque, Tipo_Problema, Orden_Presentacion, Resuelto, Tiempo_Segundos, Observaciones
```

---

## 📝 Automatización Excel

### Relleno Automático de Plantilla

Carga datos de CSVs y rellena automáticamente la plantilla Excel consolidando resultados.

```bash
python scripts/rellenar_plantilla.py data/Respuestas "docs/plantilla en blanco_registro_experimento_insight(1).xlsx"
```

**Salida automática:** `data/registro_excel/registro_resultados_YYYYMMDD_HHMMSS.xlsx`

#### Estructura de Plantilla Excel

La plantilla debe tener 8 hojas con nombres:
```
TipoA-Bloque1, TipoB-Bloque1, TipoC-Bloque1, TipoD-Bloque1
TipoA-Bloque2, TipoB-Bloque2, TipoC-Bloque2, TipoD-Bloque2
```

---

## 🔍 Validación de Datos

### Script de Validación

Para verificar integridad de datos antes de generar análisis:

```bash
python scripts/mostrar_datos_acumulados.py data/Respuestas
```

---

## 🎨 Especificaciones Técnicas

### Parámetros del Experimento

| Parámetro | Valor |
|-----------|-------|
| Total de problemas | 8 |
| Problemas por bloque | 4 |
| Tipos de problemas | A, B, C, D |
| Tiempo máximo por problema | 5 minutos |
| Máximo de movimientos | 1 cerilla |
| Participantes esperados | 10+ |

---

## 📋 Guía de Referencia Rápida

### Ejecución Completa (10+ participantes)

```bash
# 1. Actualizar códigos
python scripts/actualizar_participantes.py

# 2. Generar gráficos y análisis
python scripts/analisis_resultados.py data/Respuestas

# 3. Llenar plantilla Excel
python scripts/rellenar_plantilla.py data/Respuestas "docs/plantilla en blanco_registro_experimento_insight(1).xlsx"

# 4. Validar datos (opcional)
python scripts/mostrar_datos_acumulados.py data/Respuestas
```

### Ubicación de Salidas

- **Gráficos PNG:** `data/gráficos/`
- **Tabla CSV:** `data/gráficos/tabla_resumen.csv`
- **Excel:** `data/registro_excel/registro_resultados_*.xlsx`

---

## 📚 Referencias

- Knoblich, G., Ohlsson, S., Haider, H., & Rhenius, D. (1999). Constraint relaxation and chunk decomposition in insight problem solving. *Journal of Experimental Psychology: Learning, Memory, and Cognition*, 25(6), 1534–1555.

---

## 🔗 Enlaces Importantes

- **Experimento:** https://andresamaya288.github.io/PEC_UNED_PENSAMIENTO/
- **GitHub:** https://github.com/andresAmaya288/PEC_UNED_PENSAMIENTO

---

**Última actualización:** Mayo 2026 | Participantes: 10
