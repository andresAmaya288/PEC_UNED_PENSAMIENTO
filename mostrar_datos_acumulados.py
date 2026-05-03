#!/usr/bin/env python3
"""
Script para mostrar todos los datos de frecuencia acumulada en texto.
Muestra los tiempos individuales y la frecuencia acumulada para cada tipo y bloque.
"""

import os
import glob
import pandas as pd
import numpy as np


def main():
    """Carga datos y muestra estadísticas detalladas."""
    
    carpeta = './Respuestas'
    archivos_csv = sorted(glob.glob(os.path.join(carpeta, '*.csv')))
    
    if not archivos_csv:
        print(f"❌ No se encontraron archivos CSV en '{carpeta}'")
        return
    
    # Cargar todos los datos
    dfs = []
    for archivo in archivos_csv:
        df = pd.read_csv(archivo)
        dfs.append(df)
    
    df_all = pd.concat(dfs, ignore_index=True)
    
    print("=" * 100)
    print("ANÁLISIS DETALLADO DE DATOS ACUMULADOS POR BLOQUE Y TIPO")
    print("=" * 100)
    
    for bloque in sorted(df_all['Bloque'].unique()):
        print(f"\n{'=' * 100}")
        print(f"BLOQUE {bloque}")
        print(f"{'=' * 100}")
        
        df_bloque = df_all[df_all['Bloque'] == bloque]
        
        for tipo in ['A', 'B', 'C', 'D']:
            df_tipo = df_bloque[df_bloque['Tipo_Problema'] == tipo]
            
            if len(df_tipo) == 0:
                print(f"\n❌ No hay datos para Tipo {tipo}")
                continue
            
            # Estadísticas básicas
            resueltos = (df_tipo['Resuelto'] == 'S').sum()
            total = len(df_tipo)
            tasa = resueltos / total * 100
            
            # Tiempos
            tiempos_seg = df_tipo['Tiempo_Segundos'].values
            tiempos_min = tiempos_seg / 60.0
            
            print(f"\n{'-' * 100}")
            print(f"TIPO {tipo} - BLOQUE {bloque}")
            print(f"{'-' * 100}")
            print(f"Total: {total} problemas | Resueltos: {resueltos} | No resueltos: {total - resueltos} | Tasa: {tasa:.1f}%")
            print(f"Tiempo promedio: {tiempos_min.mean():.2f} min | Desv.Est: {tiempos_min.std():.2f} | Min: {tiempos_min.min():.2f} | Max: {tiempos_min.max():.2f}")
            
            # Mostrar cada problema individualmente
            print(f"\n  Problemas individuales (ordenados por participante):")
            print(f"  {'Participante':<15} {'Orden':<8} {'Resuelto':<12} {'Tiempo(seg)':<15} {'Tiempo(min)':<15}")
            print(f"  {'-'*70}")
            
            for idx, row in df_tipo.iterrows():
                resuelto_str = "SÍ" if row['Resuelto'] == 'S' else "NO"
                print(f"  {row['Participante']:<15} {row['Orden_Presentacion']:<8} {resuelto_str:<12} {row['Tiempo_Segundos']:<15.0f} {tiempos_min[list(df_tipo.index).index(idx)]:<15.2f}")
            
            # Cálculo detallado de frecuencia acumulada
            print(f"\n  FRECUENCIA ACUMULADA DE SOLUCIONES:")
            print(f"  {'Tiempo(min)':<20} {'Cantidad resueltos':<20} {'Descripcion':<50}")
            print(f"  {'-'*90}")
            
            puntos_tiempo = [0, 1, 2, 3, 4, 5]
            for t in puntos_tiempo:
                count = np.sum(tiempos_min <= t)
                descripcion = f"<= {t} minutos"
                print(f"  {t:<20} {count:<20} {descripcion:<50}")
            
            # Tabla de valores exactos
            print(f"\n  VALORES DETALLADOS:")
            tiempos_ordenados = sorted(tiempos_min)
            print(f"  Tiempos ordenados (minutos): {[f'{t:.2f}' for t in tiempos_ordenados]}")
            
            # Análisis de cuartiles
            q1 = np.percentile(tiempos_min, 25)
            q2 = np.percentile(tiempos_min, 50)  # mediana
            q3 = np.percentile(tiempos_min, 75)
            
            print(f"\n  CUARTILES:")
            print(f"    Q1 (25%): {q1:.2f} min")
            print(f"    Q2 (50%/Mediana): {q2:.2f} min")
            print(f"    Q3 (75%): {q3:.2f} min")
    
    # COMPARATIVA ENTRE TIPOS DEL MISMO BLOQUE
    print(f"\n\n{'=' * 100}")
    print("COMPARATIVA DE TIPOS POR BLOQUE")
    print(f"{'=' * 100}")
    
    for bloque in sorted(df_all['Bloque'].unique()):
        print(f"\n{'*' * 100}")
        print(f"BLOQUE {bloque} - RESUMEN COMPARATIVO" + " " * (98 - len(f"BLOQUE {bloque} - RESUMEN COMPARATIVO")))
        print(f"{'*' * 100}")
        
        df_bloque = df_all[df_all['Bloque'] == bloque]
        
        print(f"\n{'Tipo':<8} {'Resueltos':<15} {'Tasa(%)':<12} {'Media(min)':<15} {'Mediana(min)':<15} {'Desv.Est':<12}")
        print(f"{'-'*87}")
        
        for tipo in ['A', 'B', 'C', 'D']:
            df_tipo = df_bloque[df_bloque['Tipo_Problema'] == tipo]
            
            if len(df_tipo) == 0:
                continue
            
            resueltos = (df_tipo['Resuelto'] == 'S').sum()
            total = len(df_tipo)
            tasa = resueltos / total * 100
            tiempos_min = df_tipo['Tiempo_Segundos'] / 60.0
            
            media = tiempos_min.mean()
            mediana = np.median(tiempos_min)
            desv_est = tiempos_min.std()
            
            print(f"{tipo:<8} {resueltos}/{total:<13} {tasa:<12.1f} {media:<15.2f} {mediana:<15.2f} {desv_est:<12.2f}")
        
        # Tabla de frecuencia acumulada consolidada
        print(f"\n  TABLA DE FRECUENCIA ACUMULADA POR TIPO:")
        print(f"  {'Tiempo':<12}", end="")
        for tipo in ['A', 'B', 'C', 'D']:
            print(f"{tipo:<12}", end="")
        print()
        print(f"  {'-'*60}")
        
        for t in [0, 1, 2, 3, 4, 5]:
            print(f"  <= {t} min  ", end="")
            for tipo in ['A', 'B', 'C', 'D']:
                df_tipo = df_bloque[df_bloque['Tipo_Problema'] == tipo]
                tiempos_min = df_tipo['Tiempo_Segundos'] / 60.0
                count = np.sum(tiempos_min <= t)
                print(f"{count:<12}", end="")
            print()
    
    print(f"\n{'=' * 100}\n")


if __name__ == '__main__':
    main()
