#!/usr/bin/env python3
"""
Script para analizar y visualizar resultados del experimento de cerillas.
Genera gráficos de frecuencia acumulada de soluciones y tiempo medio de resolución
por tipo de problema, similar a las Figuras 2 y 4 de Knoblich et al. (1999).

Uso:
    python analisis_resultados.py <carpeta_csv> [--output <carpeta_salida>]

Ejemplo:
    python analisis_resultados.py ./datos_csv --output ./graficos
"""

import os
import sys
import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from collections import defaultdict


def cargar_csv_experimento(ruta_carpeta):
    """
    Carga todos los archivos CSV de una carpeta y extrae el código de participante
    del nombre del archivo (P01, P02, etc).
    
    Args:
        ruta_carpeta (str): Ruta a la carpeta con archivos CSV
        
    Returns:
        pd.DataFrame: DataFrame concatenado con todos los datos
    """
    archivos_csv = glob.glob(os.path.join(ruta_carpeta, '*.csv'))
    
    if not archivos_csv:
        print(f"❌ No se encontraron archivos CSV en '{ruta_carpeta}'")
        return None
    
    print(f"📁 Encontrados {len(archivos_csv)} archivo(s) CSV")
    
    dfs = []
    for archivo in archivos_csv:
        df = pd.read_csv(archivo)
        
        # Extraer código de participante del nombre del archivo
        # Formato esperado: P01.csv, P02.csv, etc.
        nombre_archivo = os.path.basename(archivo)
        codigo_participante = nombre_archivo.replace('.csv', '').strip()
        
        # Reemplazar el código de participante en el CSV con el del archivo
        df['Participante'] = codigo_participante
        
        dfs.append(df)
        print(f"   ✓ {nombre_archivo} → {codigo_participante} ({len(df)} registros)")
    
    df_total = pd.concat(dfs, ignore_index=True)
    return df_total


def procesar_datos_por_bloque(df):
    """
    Procesa los datos y los agrupa por bloque y tipo de problema.
    
    Args:
        df (pd.DataFrame): DataFrame con los resultados
        
    Returns:
        dict: Datos procesados por bloque
    """
    datos_por_bloque = {}
    
    for bloque in sorted(df['Bloque'].unique()):
        df_bloque = df[df['Bloque'] == bloque]
        tipos = sorted(df_bloque['Tipo_Problema'].unique())
        
        datos_bloque = {}
        for tipo in tipos:
            df_tipo = df_bloque[df_bloque['Tipo_Problema'] == tipo]
            
            # Convertir tiempo a minutos
            tiempos_min = df_tipo['Tiempo_Segundos'] / 60.0
            
            datos_bloque[tipo] = {
                'resueltos': (df_tipo['Resuelto'] == 'S').sum(),
                'total': len(df_tipo),
                'tiempo_promedio': tiempos_min.mean(),
                'tiempos': tiempos_min.values
            }
        
        datos_por_bloque[bloque] = datos_bloque
    
    return datos_por_bloque


def calcular_frecuencia_acumulada(datos_bloque):
    """
    Calcula la frecuencia acumulada de soluciones a lo largo del tiempo.
    
    Args:
        datos_bloque (dict): Datos de un bloque
        
    Returns:
        dict: Frecuencia acumulada por tipo y tiempo
    """
    frecuencia = {}
    
    for tipo in sorted(datos_bloque.keys()):
        tiempos = datos_bloque[tipo]['tiempos']
        
        # Crear puntos de tiempo: 0 al inicio, luego cada minuto
        tiempo_max = 5.0  # 5 minutos máximo
        puntos_tiempo = np.linspace(0, tiempo_max, 6)  # 0, 1, 2, 3, 4, 5 minutos
        
        freq_acum = []
        for t in puntos_tiempo:
            count = np.sum(tiempos <= t)
            freq_acum.append(count)
        
        frecuencia[tipo] = {
            'tiempo': puntos_tiempo,
            'frecuencia': freq_acum
        }
    
    return frecuencia


def graficar_frecuencia_acumulada(datos_por_bloque, carpeta_salida):
    """
    Genera gráficos de frecuencia acumulada de soluciones por bloque.
    Similar a Figuras 2 y 4 de Knoblich et al. (1999).
    
    Args:
        datos_por_bloque (dict): Datos procesados por bloque
        carpeta_salida (str): Carpeta donde guardar los gráficos
    """
    tipos_marcadores = {
        'A': ('s-', 'Type A'),   # square + line
        'B': ('o--', 'Type B'),  # circle + dashed
        'C': ('o:', 'Type C'),   # circle + dotted
        'D': ('^--', 'Type D')   # triangle + dashed
    }
    
    colores = {
        'A': '#e74c3c',  # Rojo
        'B': '#3498db',  # Azul
        'C': '#2ecc71',  # Verde
        'D': '#f39c12'   # Naranja
    }
    
    for bloque in sorted(datos_por_bloque.keys()):
        datos_bloque = datos_por_bloque[bloque]
        freq_acum = calcular_frecuencia_acumulada(datos_bloque)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Determinar y máximo basado en los datos
        y_max = max([max(f['frecuencia']) for f in freq_acum.values()])
        
        for tipo in sorted(freq_acum.keys()):
            marcador, etiqueta = tipos_marcadores[tipo]
            color = colores[tipo]
            tiempo = freq_acum[tipo]['tiempo']
            frecuencia = freq_acum[tipo]['frecuencia']
            
            ax.plot(tiempo, frecuencia, marcador, label=etiqueta, 
                   color=color, markersize=10, linewidth=2.5)
        
        ax.set_xlabel('Time (min)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Cumulative Frequency of Solutions', fontsize=12, fontweight='bold')
        ax.set_xlim(0, 5)
        ax.set_ylim(0, max(20, y_max + 2))
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend(loc='lower right', fontsize=11, framealpha=0.95)
        
        # Título descriptivo
        num_participantes = len(datos_bloque['A']['tiempos'])
        titulo = f'Cumulative solution rates for Problem Types A-D in Block {bloque}\n(n={num_participantes} participants)'
        ax.set_title(titulo, fontsize=12, fontweight='bold', pad=20)
        
        # Mejorar estilo
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        archivo_salida = os.path.join(carpeta_salida, f'fig_bloque_{bloque}_frecuencia.png')
        plt.tight_layout()
        plt.savefig(archivo_salida, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfico guardado: {archivo_salida}")
        plt.close()


def graficar_tiempo_promedio(datos_por_bloque, carpeta_salida):
    """
    Genera gráficos de tiempo medio de resolución por tipo de problema.
    
    Args:
        datos_por_bloque (dict): Datos procesados por bloque
        carpeta_salida (str): Carpeta donde guardar los gráficos
    """
    colores_tipos = {
        'A': '#e74c3c',  # Rojo
        'B': '#3498db',  # Azul
        'C': '#2ecc71',  # Verde
        'D': '#f39c12'   # Naranja
    }
    
    for bloque in sorted(datos_por_bloque.keys()):
        datos_bloque = datos_por_bloque[bloque]
        
        tipos = sorted(datos_bloque.keys())
        tiempos_promedio = [datos_bloque[t]['tiempo_promedio'] for t in tipos]
        resueltos = [datos_bloque[t]['resueltos'] for t in tipos]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Gráfico 1: Tiempo promedio de resolución
        colores_barras = [colores_tipos[t] for t in tipos]
        barras = ax1.bar(tipos, tiempos_promedio, color=colores_barras, 
                        edgecolor='black', linewidth=2, alpha=0.8)
        ax1.set_ylabel('Mean Time (minutes)', fontsize=11, fontweight='bold')
        ax1.set_xlabel('Problem Type', fontsize=11, fontweight='bold')
        ax1.set_title(f'Block {bloque}: Mean Resolution Time', fontsize=12, fontweight='bold')
        ax1.set_ylim(0, 5.5)
        ax1.grid(True, axis='y', alpha=0.3, linestyle='--')
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        
        # Añadir valores en las barras
        for barra, tiempo in zip(barras, tiempos_promedio):
            altura = barra.get_height()
            ax1.text(barra.get_x() + barra.get_width()/2., altura,
                    f'{tiempo:.1f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        # Gráfico 2: Tasa de resolución
        tasa_resolucion = [r / datos_bloque[t]['total'] * 100 for t, r in zip(tipos, resueltos)]
        barras2 = ax2.bar(tipos, tasa_resolucion, color=colores_barras, 
                         edgecolor='black', linewidth=2, alpha=0.8)
        ax2.set_ylabel('Solution Rate (%)', fontsize=11, fontweight='bold')
        ax2.set_xlabel('Problem Type', fontsize=11, fontweight='bold')
        ax2.set_title(f'Block {bloque}: Solution Rate', fontsize=12, fontweight='bold')
        ax2.set_ylim(0, 110)
        ax2.grid(True, axis='y', alpha=0.3, linestyle='--')
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        
        # Añadir valores en las barras
        for i, (tipo, tasa) in enumerate(zip(tipos, tasa_resolucion)):
            ax2.text(i, tasa + 2, f'{tasa:.0f}%', ha='center', va='bottom', 
                    fontsize=10, fontweight='bold')
        
        archivo_salida = os.path.join(carpeta_salida, f'fig_bloque_{bloque}_tiempo_y_tasa.png')
        plt.tight_layout()
        plt.savefig(archivo_salida, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfico guardado: {archivo_salida}")
        plt.close()


def generar_tabla_resumen(datos_por_bloque):
    """
    Genera una tabla resumen de los datos.
    
    Args:
        datos_por_bloque (dict): Datos procesados por bloque
        
    Returns:
        pd.DataFrame: Tabla con resumen de datos
    """
    datos_resumen = []
    
    for bloque in sorted(datos_por_bloque.keys()):
        for tipo in sorted(datos_por_bloque[bloque].keys()):
            info = datos_por_bloque[bloque][tipo]
            datos_resumen.append({
                'Bloque': bloque,
                'Tipo': tipo,
                'Resueltos': info['resueltos'],
                'Total': info['total'],
                'Tasa (%)': f"{info['resueltos']/info['total']*100:.1f}",
                'Tiempo medio (min)': f"{info['tiempo_promedio']:.2f}",
                'Desv.Est. (min)': f"{np.std(info['tiempos']):.2f}"
            })
    
    return pd.DataFrame(datos_resumen)


def main():
    """Función principal."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    carpeta_csv = sys.argv[1]
    
    # Procesar argumentos opcionales
    carpeta_salida = './gráficos'
    if '--output' in sys.argv:
        idx = sys.argv.index('--output')
        if idx + 1 < len(sys.argv):
            carpeta_salida = sys.argv[idx + 1]
    
    # Crear carpeta de salida
    Path(carpeta_salida).mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("ANÁLISIS DE RESULTADOS - EXPERIMENTO DE CERILLAS")
    print("=" * 60)
    print()
    
    # Cargar datos
    print("📊 Cargando archivos CSV...")
    df = cargar_csv_experimento(carpeta_csv)
    
    if df is None:
        sys.exit(1)
    
    print(f"\n✓ Total de registros: {len(df)}")
    print(f"✓ Participantes únicos: {df['Participante'].nunique()}")
    print()
    
    # Procesar datos
    print("🔄 Procesando datos...")
    datos_por_bloque = procesar_datos_por_bloque(df)
    
    # Generar tabla resumen
    print("\n📋 TABLA RESUMEN:")
    print("-" * 60)
    tabla_resumen = generar_tabla_resumen(datos_por_bloque)
    print(tabla_resumen.to_string(index=False))
    
    # Guardar tabla
    archivo_tabla = os.path.join(carpeta_salida, 'tabla_resumen.csv')
    tabla_resumen.to_csv(archivo_tabla, index=False)
    print(f"\n✓ Tabla guardada en: {archivo_tabla}")
    
    # Generar gráficos
    print("\n📈 Generando gráficos...")
    graficar_frecuencia_acumulada(datos_por_bloque, carpeta_salida)
    graficar_tiempo_promedio(datos_por_bloque, carpeta_salida)
    
    print("\n" + "=" * 60)
    print("✅ ANÁLISIS COMPLETADO")
    print(f"📁 Gráficos guardados en: {carpeta_salida}")
    print("=" * 60)


if __name__ == '__main__':
    main()
