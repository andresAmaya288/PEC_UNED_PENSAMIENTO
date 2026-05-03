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
import tempfile
import shutil


def main():
    """Lee todos los CSV y reemplaza Participante con el código del archivo."""
    
    # Construir ruta relativa a data/Respuestas desde la ubicación del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    carpeta = os.path.join(script_dir, '..', 'data', 'Respuestas')
    carpeta = os.path.abspath(carpeta)
    archivos_csv = sorted(glob.glob(os.path.join(carpeta, '*.csv')))
    
    if not archivos_csv:
        print(f"❌ No se encontraron archivos CSV en '{carpeta}'")
        return
    
    print(f"📁 Encontrados {len(archivos_csv)} archivo(s) CSV\n")
    
    for archivo in archivos_csv:
        nombre_archivo = os.path.basename(archivo)
        codigo = nombre_archivo.replace('.csv', '').strip()
        
        try:
            # Leer CSV
            df = pd.read_csv(archivo)
            
            # Obtener el valor anterior
            valor_anterior = df['Participante'].iloc[0] if len(df) > 0 else "???"
            
            # Reemplazar Participante por el código del archivo
            df['Participante'] = codigo
            
            # Guardar a archivo temporal primero, luego mover (más seguro)
            temp_fd, temp_path = tempfile.mkstemp(suffix='.csv', text=True)
            os.close(temp_fd)
            
            df.to_csv(temp_path, index=False)
            shutil.move(temp_path, archivo)
            
            print(f"✓ {nombre_archivo}: {valor_anterior} → {codigo} ({len(df)} registros)")
        except PermissionError as e:
            print(f"⚠️  {nombre_archivo}: Permiso denegado. ¿Está abierto en Excel? Error: {e}")
        except Exception as e:
            print(f"❌ {nombre_archivo}: Error - {e}")
    
    print(f"\n✅ Actualización completada: {len(archivos_csv)} archivo(s)")


if __name__ == '__main__':
    main()
