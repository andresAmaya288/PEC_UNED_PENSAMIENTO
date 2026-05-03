#!/usr/bin/env python3
"""
Script para reemplazar la columna Participante por el código del archivo.
Por ejemplo, sosio7020 → P01, etc.

Uso:
    python actualizar_participantes.py
"""

import os
import glob
import pandas as pd


def main():
    """Lee todos los CSV y reemplaza Participante con el código del archivo."""
    
    carpeta = './Respuestas'
    archivos_csv = sorted(glob.glob(os.path.join(carpeta, '*.csv')))
    
    if not archivos_csv:
        print(f"❌ No se encontraron archivos CSV en '{carpeta}'")
        return
    
    print(f"📁 Encontrados {len(archivos_csv)} archivo(s) CSV\n")
    
    for archivo in archivos_csv:
        nombre_archivo = os.path.basename(archivo)
        codigo = nombre_archivo.replace('.csv', '').strip()
        
        # Leer CSV
        df = pd.read_csv(archivo)
        
        # Obtener el valor anterior
        valor_anterior = df['Participante'].iloc[0] if len(df) > 0 else "???"
        
        # Reemplazar Participante por el código del archivo
        df['Participante'] = codigo
        
        # Guardar
        df.to_csv(archivo, index=False)
        
        print(f"✓ {nombre_archivo}: {valor_anterior} → {codigo} ({len(df)} registros)")
    
    print(f"\n✅ Actualización completada: {len(archivos_csv)} archivo(s)")


if __name__ == '__main__':
    main()
