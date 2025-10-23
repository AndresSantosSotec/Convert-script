# Procesador de Pagos - v3.1

Sistema de procesamiento de archivos de pagos con interfaz gráfica de usuario (GUI).

## 📋 Descripción

Aplicación que permite procesar archivos Excel y CSV con información de pagos de estudiantes, normalizando y transformando los datos para su análisis y exportación. **Versión 3.2** incluye mejoras significativas en la responsividad de la interfaz, adaptándose automáticamente a cualquier tamaño de pantalla, desde dispositivos móviles hasta monitores de escritorio de alta resolución.

## ✨ Características

- ✅ Interfaz gráfica intuitiva (no requiere conocimientos técnicos)
- ✅ **Diseño responsivo adaptado a todos los tamaños de pantalla**
- ✅ **Optimización automática para móviles, tablets y escritorio**
- ✅ **Ajuste dinámico de tamaños de fuente y botones**
- ✅ Soporte para archivos Excel (.xlsx) y CSV (.csv)
- ✅ Procesamiento automático con validaciones
- ✅ Normalización de carnés (AMS → ASM, eliminación de guiones)
- ✅ Detección de pagos múltiples en una celda
- ✅ Manejo de fechas en múltiples formatos
- ✅ Detección automática de bancos
- ✅ Soporte para montos negativos (reembolsos)
- ✅ División automática en bloques de archivos
- ✅ Barra de progreso y logs en tiempo real
- ✅ Exportación a carpeta personalizada

## 🚀 Inicio Rápido

### Opción 1: Ejecutable (Recomendado para usuarios finales)

1. Descargue el archivo `ProcesadorPagos.exe` de la carpeta `dist/`
2. Haga doble clic en el ejecutable
3. Seleccione su archivo de entrada
4. ¡Procese!

**No requiere instalación de Python ni dependencias.**

### Opción 2: Ejecutar desde código fuente

#### Requisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

#### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/AndresSantosSotec/Convert-script.git
cd Convert-script

# Instalar dependencias
pip install -r requirements.txt
```

#### Ejecución

**Interfaz Gráfica:**
```bash
python interfaz_extraerpagos.py
```

**Línea de comandos:**
```bash
python extraer_pagos.py
```

## 📱 Diseño Responsivo

La versión 3.2 introduce un sistema completo de diseño responsivo que adapta automáticamente la interfaz a cualquier tamaño de pantalla:

### Tipos de Pantalla Soportados

- **📱 Móvil** (< 768px): Interfaz optimizada para pantallas pequeñas con elementos compactos
- **📲 Tablet** (768px - 1024px): Diseño intermedio para tabletas y pantallas medianas
- **💻 Escritorio** (> 1024px): Interfaz completa con espaciado generoso

### Características Responsivas

- **Ajuste automático del tamaño de ventana**: La aplicación detecta el tamaño de tu pantalla y ajusta sus dimensiones iniciales
- **Escalado de fuentes**: Los textos se ajustan automáticamente para mantener la legibilidad
- **Botones adaptativos**: Los botones cambian de tamaño según el espacio disponible
- **Espaciado dinámico**: Los márgenes y padding se ajustan para optimizar el uso del espacio
- **Área de logs escalable**: El área de visualización de logs crece según el tamaño de la pantalla
- **Ventana redimensionable**: Puedes ajustar manualmente el tamaño de la ventana con límites inteligentes

### Compatibilidad Multiplataforma

La aplicación funciona en:
- ✅ Windows (7, 8, 10, 11)
- ✅ macOS (10.13+)
- ✅ Linux (Ubuntu, Debian, Fedora, etc.)
- ⚠️ iOS/iPadOS (requiere Python y tkinter configurado)

**Nota para iOS**: Aunque la interfaz está optimizada para funcionar en pantallas pequeñas, iOS tiene limitaciones con aplicaciones de escritorio. Para usar en iOS/iPadOS, se recomienda ejecutar mediante un entorno Python compatible o usar soluciones de escritorio remoto.

## 📖 Uso de la Interfaz Gráfica

### Paso 1: Seleccionar archivo
- Haga clic en "📁 Seleccionar Archivo"
- Navegue hasta su archivo Excel (.xlsx) o CSV (.csv)
- Seleccione el archivo

### Paso 2: Seleccionar carpeta de salida (Opcional)
- Haga clic en "📂 Seleccionar Carpeta"
- Elija dónde guardar los resultados
- Si no selecciona una carpeta, se usará la misma ubicación del archivo de entrada

### Paso 3: Procesar
- Haga clic en "▶ Procesar Archivo"
- Observe el progreso en tiempo real
- Espere a que aparezca el mensaje de éxito

### Paso 4: Ver resultados
- Haga clic en "📁 Abrir Carpeta de Resultados"
- Revise los archivos generados

## 📁 Estructura de Archivos

```
Convert-script/
├── extraer_pagos.py           # Lógica principal de procesamiento
├── interfaz_extraerpagos.py   # Interfaz gráfica
├── build_executable.py         # Script para generar ejecutable
├── requirements.txt            # Dependencias Python
├── .gitignore                  # Archivos ignorados por Git
├── README.md                   # Este archivo
├── logs/                       # Logs de procesamiento
└── dist/                       # Ejecutables generados
    └── ProcesadorPagos.exe
```

## 🛠️ Generar Ejecutable

Para generar un nuevo ejecutable:

```bash
# Instalar PyInstaller
pip install pyinstaller

# Ejecutar script de construcción
python build_executable.py
```

El ejecutable se generará en la carpeta `dist/`.

### Configuración Manual de PyInstaller

Si prefiere configurar PyInstaller manualmente:

```bash
pyinstaller --onefile --windowed --name=ProcesadorPagos \
  --add-data="extraer_pagos.py:." \
  --hidden-import=pandas --hidden-import=openpyxl \
  --hidden-import=customtkinter --collect-all=customtkinter \
  interfaz_extraerpagos.py
```

## 📊 Formato de Archivo de Entrada

El archivo Excel debe tener la siguiente estructura:

### Encabezados (primeras 2 filas):
- Fila 1: Años (2023, 2024, etc.)
- Fila 2: Nombres de meses y columnas especiales

### Datos de estudiantes (bloques de 4 filas):
1. **Fila de datos principales**: carné, nombre, plan, asesor, empresa, etc.
2. **Fila de cantidades**: montos de pagos
3. **Fila de fechas**: fechas de los pagos
4. **Fila de bancos**: bancos utilizados

### Columnas esperadas:
- Notas de pago
- Carné
- Nombre del estudiante
- Plan de estudios
- Asesor
- Empresa
- Teléfono
- Estatus
- Email
- Nomenclatura
- Mes de inicio
- Valor total
- Columnas especiales: Pago de casos, Certificación, Títulos, Capstone, Graduación
- Columnas de meses (Enero - Diciembre)

## 📝 Características del Procesamiento

### Normalización de Carnés
- Convierte `AMS` a `ASM`
- Elimina todos los guiones y espacios
- Formato compacto: `ASM2020126`

### Detección de Pagos Múltiples
- Detecta pagos separados por `/`
- Valida balance entre boletas, montos, fechas y bancos
- Auto-reconcilia datos desbalanceados

### Manejo de Fechas
- Soporta timestamps de Excel
- Formato `dd/mm/yyyy`
- Formato `d-mmm` (4-ago, 7-sep)
- Detección automática de cambio de año
- Meses en español e inglés

### Detección de Bancos
- BI (Banco Industrial)
- Promerica
- BAC
- Bantrab
- Banrural
- G&T Continental
- NeoLink
- Y más...

### Programas Soportados
- BBA, BBACM, BBABF
- MBA
- MFIN (MFM)
- MPM (MGP)
- MMK (MMKD)
- MHTM (MRRHH)
- MHHRR
- MLDO
- MKD, MKT
- MDGP, MDM
- DBA
- TEMP

## 📤 Archivos de Salida

Los archivos generados contienen:
- **carnet**: Carné normalizado
- **nombre_estudiante**: Nombre completo
- **plan_estudios**: Programa normalizado
- **Notas de pago**: Notas especiales
- **Nomenclatura**: Nomenclatura del estudiante
- **estatus**: Estado (Activo/Inactivo/GRADUADO)
- **numero_boleta**: Número de boleta de pago
- **monto**: Monto del pago
- **fecha_pago**: Fecha en formato YYYY-MM-DD
- **banco**: Banco detectado
- **concepto**: Tipo de pago (Cuota mensual, Pago de casos, etc.)
- **tipo_pago**: Especial o Mensual
- **mes_pago**: Mes correspondiente
- **año**: Año del pago

## 📊 Reportes

Al finalizar el procesamiento, se genera un reporte con:
- Total de estudiantes procesados
- Estudiantes por estado (activos, inactivos, graduados)
- Total de pagos extraídos (mensuales y especiales)
- Carnés normalizados
- Estadísticas de fechas
- Programas detectados
- Bancos utilizados
- Errores encontrados

## 🐛 Solución de Problemas

### El ejecutable no inicia
- Verifique que no esté siendo bloqueado por el antivirus
- Ejecute como administrador
- Revise los logs en la carpeta `logs/`

### Error al procesar archivo
- Verifique que el archivo siga la estructura esperada
- Asegúrese de que el archivo no esté abierto en Excel
- Revise los logs para más detalles

### Archivo muy grande
- El sistema divide automáticamente en bloques de 4000 registros
- Se generarán múltiples archivos de salida

## 📋 Dependencias

- **pandas**: Procesamiento de datos
- **openpyxl**: Lectura/escritura de Excel
- **customtkinter**: Interfaz gráfica moderna
- **pillow**: Procesamiento de imágenes
- **pyinstaller**: Generación de ejecutables

## 👤 Autor

**AndresSantosSotec**
- Versión: 3.2
- Fecha: 2025-10-23
- Mejoras: Diseño responsivo y adaptativo para todas las pantallas

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo licencia MIT.

## 🔄 Changelog

### v3.2 (2025-10-23)
- ✅ **Diseño responsivo completo para todos los tamaños de pantalla**
- ✅ **Detección automática de tipo de dispositivo (móvil/tablet/escritorio)**
- ✅ **Ajuste dinámico de ventana según resolución de pantalla**
- ✅ **Escalado adaptativo de fuentes, botones y espaciados**
- ✅ **Optimización para pantallas pequeñas y grandes**
- ✅ **Soporte mejorado para múltiples resoluciones**
- ✅ **Interfaz táctil amigable para dispositivos móviles**

### v3.1 (2025-01-17)
- ✅ Interfaz gráfica completa
- ✅ Normalización de carnés AMS→ASM sin guiones
- ✅ Soporte para montos negativos
- ✅ División inteligente en bloques
- ✅ Detección de cambio de año
- ✅ Manejo de pagos múltiples mejorado
- ✅ Generación de ejecutable
- ✅ Documentación completa

## 📞 Soporte

Si encuentra algún problema o tiene sugerencias, por favor:
1. Revise la documentación
2. Verifique los logs en la carpeta `logs/`
3. Abra un issue en el repositorio de GitHub
