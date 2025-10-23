@echo off
REM Script para ejecutar el Procesador de Pagos
REM Verifica si Python está instalado y ejecuta la interfaz gráfica

echo ================================
echo  Procesador de Pagos v3.1
echo ================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no está instalado en este sistema
    echo.
    echo Por favor:
    echo 1. Descargue Python desde https://www.python.org/downloads/
    echo 2. O use el ejecutable ProcesadorPagos.exe (no requiere Python)
    echo.
    pause
    exit /b 1
)

echo Python encontrado. Verificando dependencias...
echo.

REM Intentar instalar dependencias si no están
pip install -q -r requirements.txt 2>nul

REM Ejecutar la aplicación
echo Iniciando interfaz gráfica...
echo.
python interfaz_extraerpagos.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: No se pudo ejecutar la aplicación
    echo.
    pause
)
