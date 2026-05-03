#!/usr/bin/env python3
"""
Script para rellenar la plantilla Excel con los resultados del experimento.
Lee los archivos CSV (P01.csv, P02.csv, etc.) y rellena la plantilla
blanco_registro_experimento_insight(1).xlsx con datos individuales por tipo y bloque.

La plantilla tiene 8 hojas (TipoA/B/C/D x Bloque1/2) que se rellenan con:
- Orden de presentación
- Resuelto (1=sí, 0=no)
- Tiempo en segundos
- Observaciones

Uso:
    python rellenar_plantilla.py <carpeta_csv> <archivo_plantilla>

Ejemplo:
    python rellenar_plantilla.py ./Respuestas "./plantilla en blanco_registro_experimento_insight(1).xlsx"
"""

import os
import sys
import glob
import pandas as pd
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from datetime import datetime


def cargar_datos_csv(ruta_carpeta):
    """
    Carga todos los archivos CSV de participantes.
    
    Args:
        ruta_carpeta (str): Ruta a la carpeta con archivos CSV
        
    Returns:
        dict: Datos por participante (P01, P02, etc.) con DataFrames
    """
    archivos_csv = sorted(glob.glob(os.path.join(ruta_carpeta, 'P*.csv')))
    
    if not archivos_csv:
        print(f"❌ No se encontraron archivos CSV (P01.csv, P02.csv, etc.) en '{ruta_carpeta}'")
        return None
    
    print(f"📁 Encontrados {len(archivos_csv)} archivo(s) CSV")
    
    datos_participantes = {}
    for archivo in archivos_csv:
        nombre_archivo = os.path.basename(archivo)
        codigo = nombre_archivo.replace('.csv', '').strip()
        
        df = pd.read_csv(archivo)
        datos_participantes[codigo] = df
        print(f"   ✓ {nombre_archivo} ({len(df)} registros)")
    
    return datos_participantes


def rellenar_excel(datos_participantes, archivo_plantilla, carpeta_salida='./'):
    """
    Rellena la plantilla Excel con datos individuales por tipo y bloque.
    
    Args:
        datos_participantes (dict): Datos cargados de los CSVs
        archivo_plantilla (str): Ruta a la plantilla Excel
        carpeta_salida (str): Carpeta donde guardar el archivo relleno
    """
    if not os.path.exists(archivo_plantilla):
        print(f"❌ No se encontró la plantilla: {archivo_plantilla}")
        return
    
    print(f"\n📄 Cargando plantilla: {archivo_plantilla}")
    
    # Copiar plantilla
    nombre_salida = f"registro_resultados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    ruta_salida = os.path.join(carpeta_salida, nombre_salida)
    
    # Leer la plantilla original
    wb = openpyxl.load_workbook(archivo_plantilla)
    
    print(f"✓ Plantilla cargada: {len(wb.sheetnames)} hojas encontradas")
    
    total_registros_rellenados = 0
    
    # Procesar cada hoja (TipoA-Bloque1, TipoB-Bloque1, etc.)
    for nombre_hoja in wb.sheetnames:
        ws = wb[nombre_hoja]
        
        # Extraer tipo y bloque del nombre de la hoja (ej: "TipoA-Bloque1" -> A, 1)
        if 'Tipo' in nombre_hoja:
            tipo = nombre_hoja.split('Tipo')[1][0]  # A, B, C, o D
            bloque = int(nombre_hoja.split('Bloque')[1])  # 1 o 2
        else:
            continue
        
        print(f"   ├─ Procesando {nombre_hoja} (Tipo {tipo}, Bloque {bloque})...")
        
        # Fila actual para datos (comienza en 2, después del encabezado)
        fila_datos = 2
        
        # Procesar cada participante
        for codigo_participante in sorted(datos_participantes.keys()):
            df = datos_participantes[codigo_participante]
            
            # Filtrar por tipo y bloque
            df_filtrado = df[(df['Tipo_Problema'] == tipo) & (df['Bloque'] == bloque)]
            
            if len(df_filtrado) > 0:
                # Debe haber exactamente 1 registro para este tipo/bloque
                registro = df_filtrado.iloc[0]
                
                # Asignar participante en columna A si no está ya
                ws[f'A{fila_datos}'] = codigo_participante
                
                # Columna B: Orden de presentación
                ws[f'B{fila_datos}'] = int(registro['Orden_Presentacion'])
                
                # Columna C: Resuelto (1=S, 0=N)
                resuelto = 1 if registro['Resuelto'] == 'S' else 0
                ws[f'C{fila_datos}'] = resuelto
                
                # Columna D: Tiempo en segundos
                ws[f'D{fila_datos}'] = int(registro['Tiempo_Segundos'])
                
                # Columna E: Descripción solución (vacío por defecto)
                ws[f'E{fila_datos}'] = None
                
                # Columna F: Observaciones
                obs = str(registro['Observaciones']) if pd.notna(registro['Observaciones']) else ""
                ws[f'F{fila_datos}'] = obs
                
                total_registros_rellenados += 1
                fila_datos += 1
        
        print(f"      ✓ {fila_datos - 2} participante(s) rellenados")
    
    # Guardar archivo
    Path(carpeta_salida).mkdir(parents=True, exist_ok=True)
    wb.save(ruta_salida)
    
    print(f"\n✓ Archivo generado: {ruta_salida}")
    print(f"✓ Total de registros rellenados: {total_registros_rellenados}")
    return ruta_salida


def generar_resumen_texto(datos_participantes):
    """
    Genera un resumen en texto de los datos cargados.
    
    Args:
        datos_participantes (dict): Datos de los participantes
    """
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE DATOS CARGADOS")
    print("=" * 70)
    
    for codigo, df in sorted(datos_participantes.items()):
        resueltos = (df['Resuelto'] == 'S').sum()
        total = len(df)
        tasa = resueltos / total * 100
        
        print(f"\n{codigo}:")
        print(f"  ├─ Total: {total} problemas")
        print(f"  ├─ Resueltos: {resueltos}/{total} ({tasa:.1f}%)")
        
        for bloque in sorted(df['Bloque'].unique()):
            df_bloque = df[df['Bloque'] == bloque]
            tipos_str = ', '.join(sorted(df_bloque['Tipo_Problema'].unique()))
            resueltos_bloque = (df_bloque['Resuelto'] == 'S').sum()
            print(f"  ├─ Bloque {bloque}: {resueltos_bloque}/{len(df_bloque)} (Tipos: {tipos_str})")
    
    print("\n" + "=" * 70)


def main():
    """Función principal."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    carpeta_csv = sys.argv[1]
    archivo_plantilla = sys.argv[2] if len(sys.argv) > 2 else "plantilla en blanco_registro_experimento_insight(1).xlsx"
    
    print("=" * 70)
    print("RELLENAR PLANTILLA EXCEL - EXPERIMENTO DE CERILLAS")
    print("=" * 70)
    print()
    
    # Cargar datos CSV
    print("📊 Cargando archivos CSV...")
    datos_participantes = cargar_datos_csv(carpeta_csv)
    
    if datos_participantes is None:
        sys.exit(1)
    
    # Generar resumen
    generar_resumen_texto(datos_participantes)
    
    # Rellenar plantilla
    print("\n📝 Rellenando plantilla Excel...")
    rellenar_excel(datos_participantes, archivo_plantilla, carpeta_salida='./registro_excel')
    
    print("\n✅ PROCESO COMPLETADO")


if __name__ == '__main__':
    main()
