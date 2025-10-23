#!/bin/bash
# Script para ejecutar el Procesador de Pagos
# Verifica si Python está instalado y ejecuta la interfaz gráfica

echo "================================"
echo " Procesador de Pagos v3.1"
echo "================================"
echo ""

# Verificar si Python 3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: Python 3 no está instalado en este sistema"
    echo ""
    echo "Por favor:"
    echo "1. Instale Python 3 desde su gestor de paquetes"
    echo "   Ubuntu/Debian: sudo apt install python3 python3-pip python3-tk"
    echo "   macOS: brew install python3"
    echo "2. O use el ejecutable ProcesadorPagos (no requiere Python)"
    echo ""
    exit 1
fi

echo "✓ Python encontrado. Verificando dependencias..."
echo ""

# Intentar instalar dependencias si no están
pip3 install -q -r requirements.txt 2>/dev/null || true

# Ejecutar la aplicación
echo "Iniciando interfaz gráfica..."
echo ""
python3 interfaz_extraerpagos.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ ERROR: No se pudo ejecutar la aplicación"
    echo ""
fi
