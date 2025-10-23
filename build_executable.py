#!/usr/bin/env python3
"""
Script para generar el ejecutable del procesador de pagos
"""

import subprocess
import sys
import shutil
from pathlib import Path


def main():
    """Genera el ejecutable usando PyInstaller"""
    
    print("="*70)
    print("🚀 Generador de Ejecutable - Procesador de Pagos v3.1")
    print("="*70)
    print()
    
    # Verificar que PyInstaller esté instalado
    try:
        import PyInstaller
        print("✓ PyInstaller instalado")
    except ImportError:
        print("❌ PyInstaller no está instalado")
        print("   Ejecute: pip install pyinstaller")
        return 1
    
    # Limpiar builds anteriores
    print("\n🧹 Limpiando builds anteriores...")
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if Path(dir_name).exists():
            shutil.rmtree(dir_name)
            print(f"   ✓ Eliminado: {dir_name}/")
    
    # Buscar archivos .spec
    spec_files = list(Path('.').glob('*.spec'))
    for spec_file in spec_files:
        spec_file.unlink()
        print(f"   ✓ Eliminado: {spec_file}")
    
    print("\n📦 Generando ejecutable...")
    print("   Esto puede tomar varios minutos...")
    print()
    
    # Comando de PyInstaller
    cmd = [
        'pyinstaller',
        '--onefile',                    # Un solo archivo ejecutable
        '--windowed',                   # Sin consola (para GUI)
        '--name=ProcesadorPagos',      # Nombre del ejecutable
        '--icon=NONE',                  # Sin icono (puede agregarse después)
        '--add-data=extraer_pagos.py:.',  # Incluir el script principal
        '--hidden-import=pandas',
        '--hidden-import=openpyxl',
        '--hidden-import=customtkinter',
        '--hidden-import=PIL',
        '--hidden-import=PIL._tkinter_finder',
        '--collect-all=customtkinter',
        '--noconfirm',                  # No preguntar confirmación
        'interfaz_extraerpagos.py'
    ]
    
    # Ejecutar PyInstaller
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        
        print()
        print("="*70)
        print("✅ EJECUTABLE GENERADO EXITOSAMENTE")
        print("="*70)
        print()
        print("📂 Ubicación del ejecutable:")
        
        # Buscar el ejecutable generado
        dist_dir = Path('dist')
        if dist_dir.exists():
            exe_files = list(dist_dir.glob('ProcesadorPagos*'))
            if exe_files:
                for exe in exe_files:
                    print(f"   ✓ {exe.absolute()}")
                    print(f"   Tamaño: {exe.stat().st_size / (1024*1024):.2f} MB")
            else:
                print("   ⚠️ No se encontró el ejecutable en dist/")
        else:
            print("   ⚠️ No se encontró el directorio dist/")
        
        print()
        print("📝 Notas:")
        print("   • El ejecutable es portable (no requiere instalación)")
        print("   • No requiere tener Python instalado")
        print("   • Incluye todas las dependencias necesarias")
        print("   • Puede distribuirse directamente a usuarios finales")
        print()
        
        return 0
        
    except subprocess.CalledProcessError as e:
        print()
        print("="*70)
        print("❌ ERROR AL GENERAR EJECUTABLE")
        print("="*70)
        print(f"   {str(e)}")
        return 1
    except Exception as e:
        print()
        print("="*70)
        print(f"❌ ERROR INESPERADO: {str(e)}")
        print("="*70)
        return 1


if __name__ == "__main__":
    sys.exit(main())
