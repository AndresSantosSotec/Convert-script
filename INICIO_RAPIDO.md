# 🚀 Inicio Rápido - Procesador de Pagos

Guía de 5 minutos para comenzar a usar el Procesador de Pagos.

## 📥 Método 1: Usando el Ejecutable (Recomendado)

### Para usuarios de Windows:

1. **Descargar** el archivo `ProcesadorPagos.exe` de la carpeta `dist/`
2. **Doble clic** en el archivo
3. Si aparece advertencia de Windows:
   - Click en "Más información"
   - Click en "Ejecutar de todas formas"
4. **Listo!** La aplicación se abrirá

### Para usuarios de macOS/Linux:

1. **Descargar** el archivo `ProcesadorPagos`
2. Abrir terminal en la ubicación del archivo
3. Ejecutar: `chmod +x ProcesadorPagos && ./ProcesadorPagos`
4. **Listo!** La aplicación se abrirá

---

## 📥 Método 2: Usando Python (Requiere instalación)

### Paso 1: Instalar Python

**Windows:**
1. Ir a https://www.python.org/downloads/
2. Descargar e instalar Python 3.8+
3. ✅ Marcar "Add Python to PATH"

**macOS:**
```bash
brew install python3
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk
```

### Paso 2: Instalar dependencias

```bash
# Navegar a la carpeta del proyecto
cd Convert-script

# Instalar dependencias
pip install -r requirements.txt
```

### Paso 3: Ejecutar

**Opción A - Usando scripts:**

Windows:
```cmd
ejecutar_gui.bat
```

Linux/macOS:
```bash
./ejecutar_gui.sh
```

**Opción B - Directamente:**

```bash
python interfaz_extraerpagos.py
```

---

## 🎯 Uso Básico en 3 Pasos

### 1️⃣ Seleccionar archivo
```
📁 Seleccionar Archivo → Elegir su archivo .xlsx o .csv
```

### 2️⃣ (Opcional) Elegir carpeta de salida
```
📂 Seleccionar Carpeta → Elegir dónde guardar resultados
```

### 3️⃣ Procesar
```
▶ Procesar Archivo → Esperar a que termine → ¡Listo!
```

---

## 📊 Ejemplo de Uso

### Antes del procesamiento:
```
pagos_originales.xlsx (archivo crudo con 1000 estudiantes)
```

### Después del procesamiento:
```
pagos_originales_procesado.xlsx (archivo normalizado y limpio)
```

Contenido procesado:
- ✅ Carnés normalizados (AMS → ASM, sin guiones)
- ✅ Fechas en formato estándar (YYYY-MM-DD)
- ✅ Bancos detectados automáticamente
- ✅ Programas normalizados
- ✅ Pagos múltiples separados en registros individuales
- ✅ Datos validados y limpios

---

## ⚡ Atajos y Tips

### Para archivos grandes:
- El sistema divide automáticamente en bloques
- No se preocupe, es normal ver múltiples archivos de salida

### Para mejorar rendimiento:
- Cierre otros programas Excel
- Asegúrese de tener suficiente RAM disponible
- Use un disco con espacio libre

### Si algo sale mal:
1. Revise los logs en la carpeta `logs/`
2. Verifique que el archivo siga la estructura correcta
3. Consulte la documentación completa en `README.md`

---

## 🆘 Problemas Comunes

| Problema | Solución |
|----------|----------|
| "Archivo no encontrado" | Cierre Excel y vuelva a seleccionar el archivo |
| "Error al procesar" | Verifique la estructura del archivo (ver README) |
| Ejecutable no abre | Desactive temporalmente el antivirus |
| Python no encontrado | Instale Python 3.8+ y agregue al PATH |

---

## 📚 Más Información

- **Guía completa del usuario**: Ver `GUIA_USUARIO.md`
- **Documentación técnica**: Ver `README.md`
- **Estructura del archivo**: Ver sección en `README.md`

---

## 📞 Soporte

Si tiene problemas, incluya en su reporte:
1. Mensaje de error exacto
2. Archivo de log (carpeta `logs/`)
3. Versión del programa (v3.1)
4. Sistema operativo

---

## ✅ Checklist Pre-Procesamiento

Antes de procesar, verifique:

- [ ] Python instalado (solo si no usa ejecutable)
- [ ] Archivo Excel/CSV listo
- [ ] Archivo no está abierto en Excel
- [ ] Espacio en disco suficiente (mínimo 100 MB)
- [ ] Carpeta de salida seleccionada (opcional)

---

**¡Listo para comenzar! 🎉**

Para una guía más detallada, consulte:
- `GUIA_USUARIO.md` - Manual completo paso a paso
- `README.md` - Documentación técnica completa
