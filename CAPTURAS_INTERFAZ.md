# Capturas de Pantalla - Interfaz Gráfica

## 🖼️ Vista Principal

```
┌────────────────────────────────────────────────────────────────────┐
│  Procesador de Pagos                                          ⊡ ⊟ ✕ │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│                      Procesador de Pagos                           │
│                                                                    │
│              Versión 3.1 - Procesamiento de archivos               │
│                        Excel y CSV                                 │
│                                                                    │
│ ┌────────────────────────────────────────────────────────────────┐ │
│ │ 1. Seleccionar archivo de entrada:                            │ │
│ │                                                                │ │
│ │  ┌─────────────────────────┐                                  │ │
│ │  │  📁 Seleccionar Archivo  │  Ningún archivo seleccionado    │ │
│ │  └─────────────────────────┘                                  │ │
│ └────────────────────────────────────────────────────────────────┘ │
│                                                                    │
│ ┌────────────────────────────────────────────────────────────────┐ │
│ │ 2. Seleccionar carpeta de salida:                             │ │
│ │                                                                │ │
│ │  ┌──────────────────────────┐                                 │ │
│ │  │  📂 Seleccionar Carpeta   │  Se usará carpeta actual       │ │
│ │  └──────────────────────────┘  por defecto                    │ │
│ └────────────────────────────────────────────────────────────────┘ │
│                                                                    │
│ ┌────────────────────────────────────────────────────────────────┐ │
│ │ 3. Procesamiento:                                              │ │
│ │                                                                │ │
│ │  ┌──────────────────────────────────────────────────────────┐ │ │
│ │  │░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│ │ │
│ │  └──────────────────────────────────────────────────────────┘ │ │
│ │                                                                │ │
│ │  ┌──────────────────────────────────────────────────────────┐ │ │
│ │  │✓ Interfaz lista. Seleccione un archivo para comenzar.   │ │ │
│ │  │                                                          │ │ │
│ │  │                                                          │ │ │
│ │  │                                                          │ │ │
│ │  │                                                          │ │ │
│ │  └──────────────────────────────────────────────────────────┘ │ │
│ └────────────────────────────────────────────────────────────────┘ │
│                                                                    │
│  ┌──────────────────┐ ┌──────────────────────┐  ┌──────────────┐  │
│  │  ▶ Procesar      │ │ 📁 Abrir Carpeta de  │  │  🔄 Limpiar  │  │
│  │    Archivo       │ │    Resultados        │  │              │  │
│  └──────────────────┘ └──────────────────────┘  └──────────────┘  │
│         (verde)              (azul)                  (gris)        │
└────────────────────────────────────────────────────────────────────┘
```

## 🎨 Elementos de la Interfaz

### Colores del Tema
- **Fondo principal**: Gris claro (#F0F0F0)
- **Botón Procesar**: Verde (#2ecc71) → Verde oscuro (#27ae60) al pasar mouse
- **Botón Abrir Carpeta**: Azul (#3498db) → Azul oscuro (#2980b9) al pasar mouse
- **Botón Limpiar**: Gris (#95a5a6) → Gris oscuro (#7f8c8d) al pasar mouse
- **Texto confirmación**: Verde (#2ecc71)
- **Texto normal**: Gris oscuro
- **Barra de progreso**: Azul animado

### Tipografía
- **Título principal**: Sans-serif, 28pt, negrita
- **Subtítulo**: Sans-serif, 14pt, regular, color gris
- **Secciones**: Sans-serif, 16pt, negrita
- **Botones**: Sans-serif, 14-16pt, negrita
- **Logs**: Monospace (Courier), 11pt

### Espaciado
- **Padding externo**: 20px
- **Espaciado entre secciones**: 10px
- **Padding interno de frames**: 15px
- **Altura de botones principales**: 40-50px
- **Ancho de ventana**: 800px
- **Alto de ventana**: 600px

## 📱 Estados de la Interfaz

### Estado Inicial
```
✓ Interfaz lista
📁 Seleccionar Archivo - ACTIVO
📂 Seleccionar Carpeta - ACTIVO
▶ Procesar Archivo - DESHABILITADO (gris)
📁 Abrir Carpeta - DESHABILITADO (gris)
🔄 Limpiar - ACTIVO
```

### Estado con Archivo Seleccionado
```
Texto: "✓ pagos_originales.xlsx" (verde)
📁 Seleccionar Archivo - ACTIVO
📂 Seleccionar Carpeta - ACTIVO
▶ Procesar Archivo - HABILITADO (verde brillante)
📁 Abrir Carpeta - DESHABILITADO
🔄 Limpiar - ACTIVO
```

### Estado Procesando
```
Barra de progreso: ANIMADA (azul pulsante)
Logs: Mostrando progreso en tiempo real
📁 Seleccionar Archivo - DESHABILITADO
📂 Seleccionar Carpeta - DESHABILITADO
▶ Procesar Archivo - DESHABILITADO
📁 Abrir Carpeta - DESHABILITADO
🔄 Limpiar - DESHABILITADO
```

### Estado Completado
```
Barra de progreso: DETENIDA (vacía)
Logs: "✅ PROCESO COMPLETADO EXITOSAMENTE"
📁 Seleccionar Archivo - ACTIVO
📂 Seleccionar Carpeta - ACTIVO
▶ Procesar Archivo - HABILITADO
📁 Abrir Carpeta - HABILITADO (azul brillante)
🔄 Limpiar - ACTIVO
```

## 💬 Diálogos y Ventanas Emergentes

### Diálogo de Selección de Archivo
```
┌─────────────────────────────────────────────┐
│ Seleccionar archivo de pagos          ✕    │
├─────────────────────────────────────────────┤
│ Buscar en: ▼ Mis documentos                │
│ ┌─────────────────────────────────────────┐ │
│ │ 📁 Carpeta 1                            │ │
│ │ 📁 Carpeta 2                            │ │
│ │ 📄 pagos_originales.xlsx                │ │
│ │ 📄 datos_2024.csv                       │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ Nombre: [pagos_originales.xlsx        ]    │
│ Tipo:   [Archivos Excel (*.xlsx) ▼]        │
│                                             │
│              [Abrir] [Cancelar]             │
└─────────────────────────────────────────────┘
```

### Ventana de Éxito
```
┌─────────────────────────────────────────┐
│ ✓ Éxito                            ✕   │
├─────────────────────────────────────────┤
│                                         │
│  ✅  Procesamiento completado!          │
│                                         │
│  Pagos procesados: 1,234                │
│  Archivos generados: 1                  │
│                                         │
│  Ubicación:                             │
│  C:\Users\Usuario\Documents\resultados  │
│                                         │
│              [Aceptar]                  │
└─────────────────────────────────────────┘
```

### Ventana de Error
```
┌─────────────────────────────────────────┐
│ ✕ Error                            ✕   │
├─────────────────────────────────────────┤
│                                         │
│  ❌  Ocurrió un error durante el        │
│      procesamiento:                     │
│                                         │
│  Archivo no encontrado:                 │
│  'pagos_originales.xlsx'                │
│                                         │
│  Por favor verifique que el archivo     │
│  existe y vuelva a intentar.            │
│                                         │
│              [Aceptar]                  │
└─────────────────────────────────────────┘
```

## 📊 Vista Durante el Procesamiento

```
┌────────────────────────────────────────────────────────────────────┐
│  Procesador de Pagos                                          ⊡ ⊟ ✕ │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│ ┌────────────────────────────────────────────────────────────────┐ │
│ │ 1. Seleccionar archivo de entrada:                            │ │
│ │                                                                │ │
│ │  [📁 Seleccionar Archivo]  ✓ pagos_originales.xlsx (VERDE)    │ │
│ └────────────────────────────────────────────────────────────────┘ │
│                                                                    │
│ ┌────────────────────────────────────────────────────────────────┐ │
│ │ 2. Seleccionar carpeta de salida:                             │ │
│ │                                                                │ │
│ │  [📂 Seleccionar Carpeta]  ✓ C:\Users\...\Documents (VERDE)   │ │
│ └────────────────────────────────────────────────────────────────┘ │
│                                                                    │
│ ┌────────────────────────────────────────────────────────────────┐ │
│ │ 3. Procesamiento:                                              │ │
│ │                                                                │ │
│ │  ████████████████▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ (ANIMADO) │ │
│ │                                                                │ │
│ │  ┌──────────────────────────────────────────────────────────┐ │ │
│ │  │============================================              │ │ │
│ │  │🚀 INICIANDO PROCESAMIENTO...                            │ │ │
│ │  │============================================              │ │ │
│ │  │📄 Archivo entrada: pagos_originales.xlsx                │ │ │
│ │  │📂 Carpeta salida: C:\Users\...\Documents                │ │ │
│ │  │                                                          │ │ │
│ │  │⏳ Procesando archivo...                                  │ │ │
│ │  │INFO: 📖 Leyendo archivo Excel con doble encabezado...   │ │ │
│ │  │INFO: 📋 Archivo cargado | filas_totales=1002           │ │ │
│ │  │INFO: 👤 Procesando carnet=ASM2020126                   │ │ │
│ │  │INFO: ✅ Procesado exitosamente | pagos=12              │ │ │
│ │  │INFO: 👤 Procesando carnet=MBA2021045                   │ │ │
│ │  │INFO: ✅ Procesado exitosamente | pagos=8               │ │ │
│ │  │...                                                       │ │ │
│ │  └──────────────────────────────────────────────────────────┘ │ │
│ └────────────────────────────────────────────────────────────────┘ │
│                                                                    │
│  [▶ Procesar Archivo] [📁 Abrir Carpeta] [🔄 Limpiar]            │
│  (TODOS DESHABILITADOS - gris claro)                             │
└────────────────────────────────────────────────────────────────────┘
```

## 🎯 Características Visuales

### Animaciones
1. **Barra de progreso**: Movimiento suave de izquierda a derecha
2. **Hover en botones**: Cambio suave de color (300ms)
3. **Transiciones**: Fade in/out suave para mensajes

### Íconos Usados
- 📁 Archivo/Carpeta
- 📂 Carpeta abierta
- ▶ Play/Ejecutar
- 🔄 Recargar/Limpiar
- ✓ Confirmación
- ❌ Error
- ⚠️ Advertencia
- 🚀 Inicio
- ⏳ Procesando
- 📊 Estadísticas
- 📦 Paquete/Bloque
- 👤 Usuario/Estudiante
- 💰 Pago
- 📅 Fecha

### Responsive
- **Ventana mínima**: 700x500px
- **Ventana inicial**: 800x600px
- **Redimensionable**: Sí
- **Auto-scroll en logs**: Sí

## 🌓 Soporte de Temas

La interfaz detecta automáticamente el tema del sistema:
- **Modo claro**: Fondo claro, texto oscuro
- **Modo oscuro**: Fondo oscuro, texto claro
- **Sistema**: Se adapta al tema del sistema operativo

---

**Nota**: Las capturas de pantalla reales se generarán al ejecutar la aplicación en un entorno con interfaz gráfica. Estas son representaciones en ASCII del diseño implementado.
