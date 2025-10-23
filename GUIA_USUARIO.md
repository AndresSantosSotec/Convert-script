# Guía de Usuario - Procesador de Pagos v3.1

## 📘 Manual de Usuario para la Interfaz Gráfica

Esta guía explica paso a paso cómo utilizar el **Procesador de Pagos** con su interfaz gráfica.

---

## 🖥️ Requisitos del Sistema

- **Sistema Operativo**: Windows 7 o superior / macOS 10.12+ / Linux
- **RAM**: 4 GB mínimo (8 GB recomendado)
- **Espacio en disco**: 100 MB libres
- **Resolución de pantalla**: 1024x768 o superior

---

## 🚀 Instalación y Ejecución

### Método 1: Ejecutable (Sin instalación)

1. **Descargue** el archivo `ProcesadorPagos.exe` (Windows) o `ProcesadorPagos` (Linux/macOS)
2. **Ubique** el archivo en una carpeta de su preferencia
3. **Doble clic** en el ejecutable para iniciar la aplicación

> ⚠️ **Nota para Windows**: Si aparece una advertencia de SmartScreen:
> - Haga clic en "Más información"
> - Luego en "Ejecutar de todas formas"

### Método 2: Desde código fuente (Requiere Python)

1. Abra una terminal/consola
2. Navegue a la carpeta del proyecto
3. Ejecute: `python interfaz_extraerpagos.py`

---

## 📖 Uso de la Aplicación

### Interfaz Principal

Al abrir la aplicación, verá la ventana principal con tres secciones:

```
┌─────────────────────────────────────────┐
│   Procesador de Pagos                   │
│   Versión 3.1                           │
├─────────────────────────────────────────┤
│ 1. Seleccionar archivo de entrada:     │
│    [📁 Seleccionar Archivo]             │
├─────────────────────────────────────────┤
│ 2. Seleccionar carpeta de salida:      │
│    [📂 Seleccionar Carpeta]             │
├─────────────────────────────────────────┤
│ 3. Procesamiento:                       │
│    [Barra de progreso]                  │
│    [Área de logs]                       │
├─────────────────────────────────────────┤
│ [▶ Procesar] [📁 Abrir] [🔄 Limpiar]   │
└─────────────────────────────────────────┘
```

---

## 🔧 Paso a Paso

### Paso 1: Seleccionar Archivo de Entrada

1. Haga clic en el botón **"📁 Seleccionar Archivo"**
2. Navegue en su computadora hasta la ubicación del archivo
3. Seleccione un archivo con extensión:
   - `.xlsx` (Excel)
   - `.csv` (CSV)
4. Haga clic en **"Abrir"**

**Resultado esperado:**
- El nombre del archivo aparecerá en verde con un ✓
- Se habilitará el botón "▶ Procesar Archivo"

---

### Paso 2: Seleccionar Carpeta de Salida (Opcional)

1. Haga clic en el botón **"📂 Seleccionar Carpeta"**
2. Navegue hasta la carpeta donde desea guardar los resultados
3. Seleccione la carpeta
4. Haga clic en **"Seleccionar carpeta"**

**¿Es obligatorio?**
- ❌ No, es opcional
- Si no selecciona una carpeta, los resultados se guardarán en la misma ubicación que el archivo de entrada

---

### Paso 3: Procesar el Archivo

1. Haga clic en el botón **"▶ Procesar Archivo"**
2. La aplicación comenzará a procesar:
   - La barra de progreso se activará
   - Aparecerán mensajes en el área de logs
   - Los botones se deshabilitarán temporalmente

**Durante el procesamiento verá:**
```
====================================
🚀 INICIANDO PROCESAMIENTO...
====================================
📄 Archivo entrada: pagos_originales.xlsx
📂 Carpeta salida: C:/Users/.../resultados
⏳ Procesando archivo...
👤 Procesando estudiante: ASM2020126
✅ Procesado exitosamente
...
====================================
✅ PROCESO COMPLETADO EXITOSAMENTE
====================================
📊 Total de pagos procesados: 1234
📦 Archivos generados: 1
   ✓ pagos_normalizados_procesado.xlsx
```

---

### Paso 4: Ver Resultados

Una vez completado el procesamiento:

1. Aparecerá un mensaje emergente con el resumen:
   - Total de pagos procesados
   - Número de archivos generados
   - Ubicación de los archivos

2. Haga clic en **"📁 Abrir Carpeta de Resultados"** para:
   - Abrir automáticamente la carpeta con los archivos generados
   - Ver y acceder a los archivos Excel resultantes

3. Los archivos generados tendrán nombres como:
   - `pagos_normalizados_procesado.xlsx` (si cabe en un archivo)
   - `pagos_normalizados_procesado_parte_1_de_3.xlsx` (si se divide en bloques)

---

## 📊 Entendiendo los Resultados

### Archivos Generados

Los archivos Excel generados contienen las siguientes columnas:

| Columna | Descripción | Ejemplo |
|---------|-------------|---------|
| carnet | Carné normalizado | ASM2020126 |
| nombre_estudiante | Nombre completo | Juan Pérez García |
| plan_estudios | Programa | MBA |
| Notas de pago | Observaciones | Beca 50% |
| Nomenclatura | Código interno | MBA-2020-126 |
| estatus | Estado actual | Activo |
| numero_boleta | Número de boleta | 12345678 |
| monto | Monto del pago | 2500.00 |
| fecha_pago | Fecha (YYYY-MM-DD) | 2024-03-15 |
| banco | Banco detectado | BI |
| concepto | Tipo de concepto | Cuota mensual |
| tipo_pago | Categoría | Mensual |
| mes_pago | Mes | Marzo |
| año | Año | 2024 |

### División en Bloques

Si su archivo es muy grande (más de 4000 registros), el sistema:
- ✅ Divide automáticamente en múltiples archivos
- ✅ Mantiene la integridad (un estudiante nunca se divide entre archivos)
- ✅ Nombra los archivos secuencialmente

Ejemplo:
```
pagos_procesado_parte_1_de_3.xlsx
pagos_procesado_parte_2_de_3.xlsx
pagos_procesado_parte_3_de_3.xlsx
```

---

## 🔄 Reiniciar el Proceso

Para procesar otro archivo:

1. Haga clic en el botón **"🔄 Limpiar"**
2. Esto restablecerá:
   - La selección de archivo
   - La selección de carpeta
   - Los logs
   - El estado de los botones

3. Repita el proceso desde el Paso 1

---

## ⚠️ Mensajes de Error Comunes

### "Archivo no encontrado"
- **Causa**: El archivo fue movido o eliminado
- **Solución**: Vuelva a seleccionar el archivo

### "Error al procesar archivo"
- **Causa**: El archivo no tiene el formato esperado
- **Solución**: Verifique que el archivo siga la estructura correcta (ver README.md)

### "No se pudieron extraer pagos"
- **Causa**: El archivo está vacío o no tiene datos válidos
- **Solución**: Revise el archivo de entrada

### "Archivo en uso"
- **Causa**: El archivo está abierto en Excel u otro programa
- **Solución**: Cierre el archivo antes de procesarlo

---

## 💡 Consejos y Mejores Prácticas

### Antes de Procesar
✅ Cierre el archivo Excel si está abierto
✅ Verifique que el archivo tenga la estructura correcta
✅ Haga una copia de seguridad del archivo original
✅ Asegúrese de tener espacio suficiente en disco

### Durante el Procesamiento
✅ No cierre la aplicación mientras procesa
✅ No mueva o elimine el archivo de entrada
✅ Observe los logs para detectar advertencias

### Después de Procesar
✅ Revise los archivos generados
✅ Verifique las estadísticas en los logs
✅ Conserve los logs para referencia futura

---

## 📁 Ubicación de los Logs

Los logs detallados se guardan automáticamente en:

```
logs/procesamiento_pagos_v3.1_YYYYMMDD_HHMMSS.log
```

Estos logs contienen:
- Fecha y hora de cada operación
- Detalles de cada estudiante procesado
- Advertencias y errores encontrados
- Estadísticas detalladas

**Útil para:**
- Depurar problemas
- Auditoría del procesamiento
- Soporte técnico

---

## 🛡️ Seguridad y Privacidad

- ✅ La aplicación no envía datos a internet
- ✅ Todos los archivos se procesan localmente
- ✅ No se almacena información personal en la nube
- ✅ Los logs son locales y privados

---

## 📞 Obtener Ayuda

Si tiene problemas:

1. **Revise los logs**: Contienen información detallada del error
2. **Consulte el README.md**: Documentación técnica completa
3. **Reporte el problema**: Incluya:
   - Descripción del error
   - Mensaje de error exacto
   - Archivo de log relevante
   - Captura de pantalla (si es posible)

---

## 📝 Características Especiales

### Normalización Automática de Carnés
- `AMS-2020126` → `ASM2020126`
- Elimina guiones y espacios
- Convierte a mayúsculas

### Detección Inteligente de Bancos
- Reconoce abreviaciones: BI, BAC, G&T
- Normaliza nombres variantes
- Maneja casos especiales

### Manejo Robusto de Fechas
- Múltiples formatos soportados
- Detección de cambio de año
- Corrección automática de fechas inválidas

### Pagos Múltiples
- Detecta pagos separados por `/`
- Auto-reconcilia datos desbalanceados
- Genera registros individuales

---

## ✅ Lista de Verificación Rápida

Antes de procesar un archivo, verifique:

- [ ] El archivo está en formato Excel (.xlsx) o CSV (.csv)
- [ ] El archivo sigue la estructura esperada
- [ ] El archivo no está abierto en otro programa
- [ ] Tiene espacio suficiente en disco
- [ ] Ha seleccionado el archivo correcto
- [ ] Ha seleccionado la carpeta de salida (opcional)

---

## 📈 Estadísticas del Procesamiento

Al finalizar, verá estadísticas como:

```
👥 ESTUDIANTES:
   • Procesados: 150
   • Activos: 120
   • Inactivos: 20
   • Graduados: 10
   
💰 PAGOS:
   • Total extraídos: 1,234
   • Pagos mensuales: 1,200
   • Pagos especiales: 34
   
📅 FECHAS:
   • Parseadas: 1,234
   • Tasa de éxito: 98.5%
```

---

## 🎯 Casos de Uso

### Caso 1: Archivo Pequeño (< 1000 registros)
- Tiempo estimado: 30 segundos - 1 minuto
- Archivo de salida: 1 archivo

### Caso 2: Archivo Mediano (1000-5000 registros)
- Tiempo estimado: 1-3 minutos
- Archivo de salida: 1-2 archivos

### Caso 3: Archivo Grande (> 5000 registros)
- Tiempo estimado: 3-10 minutos
- Archivo de salida: 2-4 archivos

---

## 🔍 Preguntas Frecuentes

**P: ¿Puedo procesar archivos CSV?**
R: Sí, el sistema soporta tanto Excel (.xlsx) como CSV (.csv)

**P: ¿Se modifica el archivo original?**
R: No, el archivo original nunca se modifica. Solo se generan nuevos archivos.

**P: ¿Puedo cancelar el procesamiento?**
R: No actualmente. Si necesita detenerlo, cierre la aplicación.

**P: ¿Cuántos archivos puedo procesar a la vez?**
R: Uno a la vez. Use el botón "Limpiar" para procesar otro.

**P: ¿Los datos están seguros?**
R: Sí, todo se procesa localmente. No se envía información a internet.

---

## 📋 Glosario

- **Carné**: Identificador único del estudiante
- **Boleta**: Número de comprobante de pago
- **Normalización**: Proceso de estandarizar datos
- **Bloque**: División de archivo grande en partes
- **Log**: Registro de actividades del sistema
- **Estatus**: Estado del estudiante (Activo/Inactivo/Graduado)

---

**Versión del documento**: 1.0  
**Fecha**: 2025-01-17  
**Autor**: AndresSantosSotec
