import os
import re
import logging
import sys
import calendar
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Set
from pathlib import Path
from collections import defaultdict

import pandas as pd


class ExcelPaymentProcessorV3:
    """
    Procesador MEJORADO de pagos desde Excel.
    Versión 3.1 - Con normalización de carnés SIN GUIONES y mejoras críticas
    Autor: AndresSantosSotec
    Fecha: 2025-01-17
    
    Cambios v3.1:
    - Manejo de doble encabezado (años + meses)
    - Extracción de múltiples pagos en una celda (/)
    - Parseo mejorado de fechas con meses en español
    - Columnas especiales (Pago de casos, Certificación, etc.)
    - Estado del estudiante (activo/inactivo)
    - ✅ Normalización de carnés AMS → ASM SIN GUIONES
    - ✅ División de bloques preservando integridad de estudiantes
    - ✅ Soporte para montos negativos
    """
    
    TAMAÑO_BLOQUE = 4000
    
    # Índices de columnas fijas (ajustar según tu Excel real)
    COL_NOTAS = 0
    COL_CARNE = 1
    COL_NOMBRE = 2
    COL_PLAN = 3
    COL_ASESOR = 4
    COL_EMPRESA = 5
    COL_TELEFONO = 6
    COL_ESTATUS = 7
    COL_MAIL = 8
    COL_NOMENCLATURA = 9
    COL_MES_INICIO = 10
    COL_VALOR_TOTAL = 11
    
    # Columnas especiales antes de los meses
    COL_PAGO_CASOS_START = 12
    COL_CERTIFICACION_START = 15
    COL_TITULOS_START = 18
    COL_CAPSTONE_START = 21
    COL_GRADUACION_START = 24
    COL_INFO_PAGO_START = 27
    
    # A partir de aquí empiezan los meses (columna AC = 28 en base 0)
    COL_MESES_START = 28
    
    def __init__(self, log_level=logging.INFO, tamaño_bloque=4000):
        self.TAMAÑO_BLOQUE = tamaño_bloque
        
        # Mapeo de meses en español a números
        self.mes_a_numero = {
            'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
            'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
            'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12,
            'ene': 1, 'feb': 2, 'mar': 3, 'abr': 4,
            'may': 5, 'jun': 6, 'jul': 7, 'ago': 8, 'agos': 8,
            'sep': 9, 'sept': 9, 'oct': 10, 'nov': 11, 'dic': 12,
            'january': 1, 'february': 2, 'march': 3, 'april': 4,
            'may': 5, 'june': 6, 'july': 7, 'august': 8, 'september': 9,
            'october': 10, 'november': 11, 'december': 12,
            'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4,
            'jun': 6, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
        }
        
        self.meses_orden = [
            'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
            'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
        ]
        
        # ALIASES DE PROGRAMAS
        self.program_aliases = {
            'MMKD': 'MMK',
            'MMK': 'MMK',
            'MRRHH': 'MHTM',
            'MHHRR': 'MHHRR',
            'MGP': 'MPM',
            'MFM': 'MFIN',
        }
        
        # PROGRAMAS VÁLIDOS
        self.programas_validos = {
            'BBA': 'BBA',
            'BBACM': 'BBACM',
            'BBABF': 'BBABF',
            'MBA': 'MBA',
            'MFIN': 'MFIN',
            'MPM': 'MPM',
            'MMK': 'MMK',
            'MHTM': 'MHTM',
            'MLDO': 'MLDO',
            'MKD': 'MKD',
            'MKT': 'MKT',
            'TEMP': 'TEMP',
            'MHHRR': 'MHHRR',
            'MDGP': 'MDGP',
            'MDM': 'MDM',
            'DBA': 'DBA',
            'MGP': 'MPM',
            'MFM': 'MFIN',
        }
        
        # MAPEO COMPLETO
        self.mapeo_planes_completo = {
            'bba': 'BBA',
            'bba 24 on line': 'BBA',
            'bba 24 online': 'BBA',
            'bba online': 'BBA',
            'bba on line': 'BBA',
            'bachelor in business administration': 'BBA',
            'bachelor of business administration': 'BBA',
            
            'bba cm': 'BBACM',
            'bbacm': 'BBACM',
            'commercial management': 'BBACM',
            
            'bba bf': 'BBABF',
            'bbabf': 'BBABF',
            'banking and fintech': 'BBABF',
            
            'mba': 'MBA',
            'mba 24 on line': 'MBA',
            'mba 24 online': 'MBA',
            'master of business administration': 'MBA',
            'master in business administration': 'MBA',
            
            'mfin': 'MFIN',
            'mfm': 'MFIN',
            'mfm 18 on line': 'MFIN',
            'mfm 9 on line': 'MFIN',
            'master of financial management': 'MFIN',
            'master in financial management': 'MFIN',
            
            'mpm': 'MPM',
            'mgp': 'MPM',
            'mgdp': 'MPM',
            'mgp 18 on line': 'MPM',
            'mgp 21 on line': 'MPM',
            'master of project management': 'MPM',
            'master in project management': 'MPM',
            
            'mmkd': 'MMK',
            'mmk': 'MMK',
            'master of marketing': 'MMK',
            'master in marketing': 'MMK',
            
            'mhtm': 'MHTM',
            'mrrhh': 'MHTM',
            'master in human talent management': 'MHTM',
            
            'mhhrr': 'MHHRR',
            'recursos humanos': 'MHHRR',
            
            'mdgp': 'MDGP',
            'direccion y gestion de proyectos': 'MDGP',
            
            'mdm': 'MDM',
            'direccion de marketing': 'MDM',
            
            'dba': 'DBA',
            'doctor in business administration': 'DBA',
            
            'mldo': 'MLDO',
            'master in logistics': 'MLDO',
            
            'mkd': 'MKD',
            'mkt': 'MKT',
            'temp': 'TEMP',
        }
        
        # Patrones de bancos
        self.patrones_bancos = [
            (r'(?:^|\s)bi(?:\s|$|\/)', 'BI'),
            (r'industrial', 'Industrial'),
            (r'promerica', 'Promerica'),
            (r'bac', 'BAC'),
            (r'bantrab', 'Bantrab'),
            (r'banrural', 'Banrural'),
            (r'g\s*&\s*t', 'G&T Continental'),
            (r'neolink|neo\s*link', 'NeoLink'),
            (r'credomatic', 'Credomatic'),
            (r'visa(?!\s*net)', 'Visa'),
            (r'visa\s*net', 'Visa'),
            (r'mastercard|master\s*card', 'Mastercard'),
        ]
        
        self.setup_logging(log_level)
        self.logger = logging.getLogger(__name__)
        
        self.estadisticas = {
            'estudiantes_procesados': 0,
            'pagos_extraidos': 0,
            'pagos_especiales': 0,
            'pagos_mensuales': 0,
            'pagos_multiples_detectados': 0,
            'pagos_multiples_desbalanceados': 0,
            'montos_negativos': 0,
            'errores': 0,
            'estudiantes_sin_pagos': 0,
            'fechas_parseadas': 0,
            'fechas_fallidas': 0,
            'fechas_no_disponibles': 0,
            'fechas_corregidas': 0,
            'fechas_cambio_año': 0,
            'montos_invalidos': 0,
            'boletas_invalidas': 0,
            'carnets_normalizados': 0,
            'carnets_compactados': 0,  # ✅ NUEVO: carnés sin AMS pero con guiones eliminados
            'bancos_detectados': defaultdict(int),
            'planes_detectados': defaultdict(int),
            'planes_no_mapeados': defaultdict(int),
            'inicio_procesamiento': None,
            'carnets_procesados': set(),
            'carnets_duplicados': defaultdict(int),
            'filas_problematicas': [],
            'bloques_generados': 0,
            'estudiantes_activos': 0,
            'estudiantes_inactivos': 0,
        }

    # ========== LOGGING ==========
    def setup_logging(self, level):
        """Configura logging."""
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = log_dir / f'procesamiento_pagos_v3.1_{timestamp}.log'
        
        log_format = '%(asctime)s | %(levelname)-8s | %(funcName)-30s | %(message)s'
        
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        
        logging.basicConfig(
            level=level,
            format=log_format,
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler(log_file, encoding='utf-8')
            ],
            force=True
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"📁 Log guardado en: {log_file}")

    def log_estado(self, msg: str, nivel: str = "info", **kwargs):
        """Log con contexto adicional."""
        contexto = " | ".join([f"{k}={v}" for k, v in kwargs.items()])
        m = f"{msg}"
        if contexto:
            m += f" | {contexto}"
        
        log_func = getattr(self.logger, nivel.lower(), self.logger.info)
        log_func(m)

    # ========== UTILIDADES ==========
    def _is_empty(self, v: Any) -> bool:
        """Validación EXHAUSTIVA de valores vacíos."""
        if v is None:
            return True
        
        if isinstance(v, float) and pd.isna(v):
            return True
        
        if isinstance(v, str):
            s = v.strip().lower()
            empty_values = {
                '', 'nan', 'n/a', 'na', 'null', 'none', 
                'undefined', 'nil', '-', '--', '---',
                'sin dato', 'sin datos', 'no aplica',
                'no disponible', 'nd', 's/d', 's/n',
                'vacio', 'vacío', 'empty', '0'
            }
            return s in empty_values
        
        return False

    def limpiar_texto(self, v: Any) -> Optional[str]:
        """Limpieza robusta de texto."""
        if self._is_empty(v):
            return None
        
        try:
            texto = str(v).strip()
            texto = re.sub(r'\s+', ' ', texto)
            texto = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', texto)
            texto = texto.strip()
            return texto if texto else None
        except Exception as e:
            self.log_estado(f"Error limpiando texto: {e}", "debug", valor=str(v)[:50])
            return None

    def normalizar_carnet(self, carnet: str) -> str:
        """
        ✅ VERSIÓN FINAL: Normaliza carnés con formato COMPACTO (sin guiones).
        
        Reglas:
        1. AMS → ASM
        2. Eliminar todos los separadores (-, espacio, _)
        3. Convertir a MAYÚSCULAS
        
        Resultado: Formato compacto sin guiones
        
        Ejemplos:
        - "AMS-2020126" → "ASM2020126"
        - "AMS 2020126" → "ASM2020126"
        - "AMS2020126" → "ASM2020126"
        - "ams-2020126" → "ASM2020126"
        - "MBA-2021001" → "MBA2021001"
        - "BBA 2022123" → "BBA2022123"
        """
        if not carnet:
            return carnet
        
        # Convertir a mayúsculas
        carnet_upper = carnet.upper()
        carnet_original = carnet_upper
        
        # ✅ PASO 1: Eliminar TODOS los separadores (guiones, espacios, guiones bajos)
        carnet_limpio = carnet_upper.replace('-', '').replace(' ', '').replace('_', '')
        
        # ✅ PASO 2: Detectar si comienza con AMS
        if carnet_limpio.startswith('AMS'):
            # Extraer la parte después de AMS
            resto = carnet_limpio[3:]  # Todo después de "AMS"
            
            # Reconstruir como ASM + resto (SIN GUIÓN)
            carnet_normalizado = f"ASM{resto}"
            
            # Registrar la normalización
            if carnet_normalizado != carnet_original:
                self.estadisticas['carnets_normalizados'] += 1
                self.log_estado(
                    f"🔄 Carné normalizado (AMS→ASM)",
                    "debug",
                    original=carnet_original,
                    normalizado=carnet_normalizado
                )
            
            return carnet_normalizado
        
        # ✅ PASO 3: Si NO comienza con AMS, solo eliminar separadores
        # Esto también normaliza carnés como "MBA-2021001" → "MBA2021001"
        if carnet_limpio != carnet_original:
            self.estadisticas['carnets_compactados'] += 1
            self.log_estado(
                f"🔧 Carné compactado (guiones eliminados)",
                "debug",
                original=carnet_original,
                normalizado=carnet_limpio
            )
        
        return carnet_limpio

    def limpiar_monto(self, v: Any) -> Optional[float]:
        """
        ✅ MEJORADO: Limpieza ROBUSTA de montos con soporte para negativos.
        """
        if self._is_empty(v):
            return None
        
        try:
            s = str(v).strip()
            
            # Detectar si es negativo (para reembolsos/devoluciones)
            es_negativo = False
            if s.startswith('-') or (s.startswith('(') and s.endswith(')')):
                es_negativo = True
                if s.startswith('(') and s.endswith(')'):
                    s = s[1:-1]
            
            # Limpiar símbolos monetarios
            s = s.replace('Q', '').replace('$', '').replace('€', '').replace('₡', '').strip()
            s = s.replace(',', '').replace(' ', '')
            s = re.sub(r'[^\d\.\-]', '', s)
            
            if not s or s == '-' or s == '.':
                return None
            
            # Convertir a float SIN abs() para preservar signo
            val = float(s)
            
            # Aplicar el signo negativo si fue detectado
            if es_negativo and val > 0:
                val = -val
            
            # Validar rango (permitiendo negativos)
            if not (-100000.0 <= val <= 100000.0):
                if val != 0:
                    self.log_estado(f"Monto fuera de rango", "debug", monto=val)
                self.estadisticas['montos_invalidos'] += 1
                return None
            
            # Estadística para montos negativos
            if val < 0:
                self.estadisticas['montos_negativos'] += 1
                self.log_estado(
                    f"💸 Monto negativo (reembolso/devolución)",
                    "info",
                    monto=val
                )
            
            return val
            
        except (ValueError, TypeError):
            self.estadisticas['montos_invalidos'] += 1
            return None
        except Exception as e:
            self.log_estado(f"Error procesando monto: {e}", "debug", valor=str(v)[:50])
            self.estadisticas['montos_invalidos'] += 1
            return None

    def to_str_preserve_number(self, v: Any) -> Optional[str]:
        """Preserva números largos como texto."""
        if self._is_empty(v):
            return None
        
        try:
            if isinstance(v, bool):
                return None
            if isinstance(v, int):
                return str(v)
            if isinstance(v, float):
                if pd.isna(v) or not pd.api.types.is_finite(v):
                    return None
                if v == int(v):
                    return str(int(v))
                s = f"{v:.15f}".rstrip('0').rstrip('.')
                return s if s else "0"
            
            s = str(v).strip()
            if len(s) > 50:
                self.log_estado(f"Boleta muy larga (truncada)", "debug", valor=s[:30])
                return s[:50]
            return s if s else None
        except Exception as e:
            self.log_estado(f"Error convirtiendo número: {e}", "debug", valor=str(v)[:30])
            return None

    # ========== PARSEO DE FECHAS MEJORADO ==========
    def parse_fecha_mejorada(
        self, 
        v: Any, 
        año_contexto: Optional[int] = None, 
        mes_nombre: Optional[str] = None,
        año_columna: Optional[int] = None
    ) -> Optional[str]:
        """
        ✅ MEJORADO: Parser de fechas con mejor manejo de cambio de año.
        """
        if self._is_empty(v):
            self.estadisticas['fechas_no_disponibles'] += 1
            return None
        
        texto_original = str(v).strip()
        
        # 1. Timestamp de Excel
        if isinstance(v, (int, float)) and not pd.isna(v):
            try:
                if 25000 <= v <= 65000:
                    fecha = pd.to_datetime('1899-12-30') + pd.Timedelta(days=v)
                    self.estadisticas['fechas_parseadas'] += 1
                    return fecha.strftime('%Y-%m-%d')
            except Exception:
                pass
        
        # 2. Formato dd/mm/yyyy
        match = re.match(r'^(\d{1,2})/(\d{1,2})/(\d{4})$', texto_original)
        if match:
            try:
                dia = int(match.group(1))
                mes = int(match.group(2))
                año = int(match.group(3))
                
                if 1 <= mes <= 12 and 1 <= dia <= 31 and 2000 <= año <= 2030:
                    fecha = datetime(año, mes, dia)
                    self.estadisticas['fechas_parseadas'] += 1
                    return fecha.strftime('%Y-%m-%d')
            except (ValueError, OverflowError):
                pass
        
        # 3. Formato d-mmm (4-ago, 7-sep) - MEJORADO
        match = re.match(r'^(\d{1,2})-([a-zA-Zá-ú]+)$', texto_original.lower())
        if match:
            try:
                dia = int(match.group(1))
                mes_str = match.group(2).lower()
                
                mes_num = self.mes_a_numero.get(mes_str)
                
                if mes_num:
                    # ✅ USAR año_columna si está disponible
                    año_usar = año_columna if año_columna else (año_contexto or 2020)
                    
                    # ✅ DETECCIÓN DE CAMBIO DE AÑO mejorada
                    if mes_nombre and año_columna:
                        mes_columna_num = self._extraer_mes_de_nombre_columna(mes_nombre)
                        
                        if mes_columna_num and mes_columna_num >= 7 and mes_num <= 6:
                            año_usar = año_columna + 1
                            self.estadisticas['fechas_cambio_año'] += 1
                            self.log_estado(
                                f"📅 Cambio de año detectado",
                                "debug",
                                mes_columna=mes_columna_num,
                                mes_pago=mes_num,
                                año_original=año_columna,
                                año_ajustado=año_usar
                            )
                    
                    try:
                        fecha = datetime(año_usar, mes_num, dia)
                        self.estadisticas['fechas_parseadas'] += 1
                        return fecha.strftime('%Y-%m-%d')
                    except ValueError:
                        ultimo_dia = calendar.monthrange(año_usar, mes_num)[1]
                        dia_ajustado = min(dia, ultimo_dia)
                        fecha = datetime(año_usar, mes_num, dia_ajustado)
                        self.estadisticas['fechas_parseadas'] += 1
                        self.estadisticas['fechas_corregidas'] += 1
                        self.log_estado(
                            f"⚠️ Día ajustado",
                            "warning",
                            original=f"{dia}-{mes_str}",
                            ajustado=dia_ajustado
                        )
                        return fecha.strftime('%Y-%m-%d')
            except Exception as e:
                self.log_estado(f"Error parseando formato d-mmm: {e}", "debug", texto=texto_original)
        
        # 4. Último recurso: pandas
        try:
            fecha = pd.to_datetime(texto_original, dayfirst=True, errors='coerce')
            if not pd.isna(fecha) and 2000 <= fecha.year <= 2030:
                self.estadisticas['fechas_parseadas'] += 1
                return fecha.strftime('%Y-%m-%d')
        except Exception:
            pass
        
        self.estadisticas['fechas_fallidas'] += 1
        self.log_estado(f"⚠️ Fecha no parseada", "debug", fecha=texto_original)
        return None

    def _extraer_mes_de_nombre_columna(self, nombre_columna: str) -> Optional[int]:
        """Extrae el número de mes desde el nombre de la columna."""
        if not nombre_columna:
            return None
        
        nombre_limpio = re.sub(r'\.\d+$', '', nombre_columna).strip().lower()
        return self.mes_a_numero.get(nombre_limpio)

    # ========== NORMALIZACIÓN DE PLAN DE ESTUDIOS ==========
    def obtener_programa(self, plan_raw: Any) -> str:
        """Obtiene el código de programa normalizado."""
        if self._is_empty(plan_raw):
            self.estadisticas['planes_no_mapeados']['VACIO'] += 1
            return "TEMP"
        
        codigo_base = str(plan_raw).strip().upper()
        codigo_normalizado = re.sub(r'[^A-Z]', '', codigo_base)
        
        if codigo_normalizado in self.program_aliases:
            codigo_final = self.program_aliases[codigo_normalizado]
            self.estadisticas['planes_detectados'][codigo_final] += 1
            return codigo_final
        
        if codigo_normalizado in self.programas_validos:
            codigo_final = self.programas_validos[codigo_normalizado]
            self.estadisticas['planes_detectados'][codigo_final] += 1
            return codigo_final
        
        for programa_code in self.programas_validos.keys():
            if programa_code.startswith(codigo_normalizado) and len(codigo_normalizado) >= 2:
                codigo_final = self.programas_validos[programa_code]
                self.estadisticas['planes_detectados'][codigo_final] += 1
                return codigo_final
        
        plan_limpio = str(plan_raw).strip().lower()
        plan_limpio = re.sub(r'[^\w\s]', '', plan_limpio)
        plan_limpio = re.sub(r'\s+', ' ', plan_limpio).strip()
        
        if plan_limpio in self.mapeo_planes_completo:
            codigo_final = self.mapeo_planes_completo[plan_limpio]
            self.estadisticas['planes_detectados'][codigo_final] += 1
            return codigo_final
        
        for key, value in self.mapeo_planes_completo.items():
            if key in plan_limpio or plan_limpio in key:
                codigo_final = value
                self.estadisticas['planes_detectados'][codigo_final] += 1
                return codigo_final
        
        self.estadisticas['planes_no_mapeados'][str(plan_raw)] += 1
        self.log_estado(f"⚠️ Plan NO mapeado", "warning", plan=str(plan_raw))
        return "TEMP"

    def detectar_banco(self, texto: Optional[str]) -> str:
        """Detector de banco."""
        if not texto or self._is_empty(texto):
            return "No especificado"
        
        try:
            t = str(texto).strip().lower()
            
            if t in ['n/a', 'na', '0', '-', 'null', 'none']:
                return "No especificado"
            
            for patron, nombre_banco in self.patrones_bancos:
                if re.search(patron, t, re.IGNORECASE):
                    self.estadisticas['bancos_detectados'][nombre_banco] += 1
                    return nombre_banco
            
            return "No especificado"
        except Exception as e:
            self.log_estado(f"Error detectando banco: {e}", "debug", texto=str(texto)[:50])
            return "No especificado"

    def _validar_balance_pagos_multiples(
        self,
        boletas: List[str],
        montos: List[str],
        fechas: List[str],
        bancos: List[str],
        carnet: str,
        concepto: str
    ) -> bool:
        """
        ✅ Valida que los arrays de pagos múltiples estén balanceados.
        """
        longitudes = {
            'boletas': len(boletas),
            'montos': len(montos),
            'fechas': len(fechas),
            'bancos': len(bancos)
        }
        
        longitudes_validas = {k: v for k, v in longitudes.items() if v > 0}
        
        if not longitudes_validas:
            return True
        
        valores_unicos = set(longitudes_validas.values())
        
        if len(valores_unicos) > 1:
            if longitudes.get('boletas', 0) != longitudes.get('montos', 0):
                self.estadisticas['pagos_multiples_desbalanceados'] += 1
                self.log_estado(
                    f"⚠️ DESBALANCE CRÍTICO en pagos múltiples",
                    "warning",
                    carnet=carnet,
                    concepto=concepto,
                    longitudes=longitudes
                )
                return False
            
            self.log_estado(
                f"ℹ️ Desbalance menor en pagos múltiples (fechas/bancos)",
                "debug",
                longitudes=longitudes
            )
        
        return True

    def _auto_reconciliar_pagos_multiples(
        self,
        boletas: List[str],
        montos: List[Any],
        fechas: List[Any],
        bancos: List[Any],
        carnet: str,
        concepto: str
    ) -> Tuple[List[str], List[Any], List[Any], List[Any]]:
        """
        ✅ Reconciliación automática cuando las listas de pagos múltiples están desbalanceadas.
        Permite generar registros consistentes distribuyendo los datos lógicamente.
        """
        len_max = max(len(boletas), len(montos), len(fechas), len(bancos))

        if len_max == 0:
            return boletas, montos, fechas, bancos

        # Extender o repetir montos
        if len(montos) == 0:
            montos = [None] * len_max
        elif len(montos) == 1:
            montos = montos * len_max
        elif len(montos) < len_max:
            montos = (montos * ((len_max // len(montos)) + 1))[:len_max]

        # Extender o repetir fechas
        if len(fechas) == 0:
            fechas = [None] * len_max
        elif len(fechas) == 1:
            fechas = fechas * len_max
        elif len(fechas) < len_max:
            fechas = (fechas * ((len_max // len(fechas)) + 1))[:len_max]

        # Extender o ciclar bancos
        if len(bancos) == 0:
            bancos = ["No especificado"] * len_max
        elif len(bancos) < len_max:
            bancos = (bancos * ((len_max // len(bancos)) + 1))[:len_max]

        # Alinear boletas (si hay menos)
        if len(boletas) < len_max:
            boletas = (boletas * ((len_max // len(boletas)) + 1))[:len_max]

        self.log_estado(
            f"🤝 Pagos reconciliados automáticamente",
            "info",
            carnet=carnet,
            concepto=concepto,
            boletas=len(boletas),
            montos=len(montos),
            fechas=len(fechas),
            bancos=len(bancos)
        )

        return boletas, montos, fechas, bancos

    def extraer_valores_multiples(self, celda: Any) -> List[str]:
        """
        ✅ MEJORADO: Extrae múltiples valores con mejor validación.
        """
        if self._is_empty(celda):
            return []
        
        texto = str(celda).strip()
        
        if '/' in texto:
            if texto.startswith('http://') or texto.startswith('https://'):
                return [texto]
            
            num_separadores = texto.count('/')
            
            if num_separadores <= 2 and re.search(r'\d{1,2}/\d{1,2}', texto):
                return [texto]
            
            partes = [p.strip() for p in texto.split('/')]
            partes = [p for p in partes if p and p.lower() not in ['n/a', 'na', 'vale', '']]
            
            if len(partes) > 1:
                self.estadisticas['pagos_multiples_detectados'] += 1
                self.log_estado(
                    f"🔄 Múltiples valores detectados",
                    "debug",
                    original=texto,
                    cantidad=len(partes)
                )
            
            return partes
        
        return [texto] if texto else []

    # ========== PROCESAMIENTO PRINCIPAL ==========
    def procesar_excel_v3(self, archivo_entrada: str) -> List[Dict[str, Any]]:
        """
        Procesa el archivo Excel con estructura de doble encabezado.
        """
        self.estadisticas['inicio_procesamiento'] = datetime.now()
        self.log_estado(f"🚀 Iniciando procesamiento V3.1", archivo=archivo_entrada)

        try:
            archivo_path = Path(archivo_entrada)
            if not archivo_path.exists():
                raise FileNotFoundError(f"Archivo no encontrado: {archivo_entrada}")
            
            self.log_estado("📖 Leyendo archivo Excel con doble encabezado...")
            
            df = pd.read_excel(archivo_entrada, engine='openpyxl', dtype=object, header=None)
            
            if df.empty:
                raise ValueError("El archivo Excel está vacío")
            
            años_row = df.iloc[0]
            headers_row = df.iloc[1]
            
            self.log_estado(
                f"📋 Archivo cargado",
                filas_totales=len(df),
                columnas=len(df.columns)
            )
            
            columnas_info = self._construir_mapa_columnas(años_row, headers_row)
            
            pagos: List[Dict[str, Any]] = []
            i = 2
            n = len(df)
            
            while i < n:
                try:
                    if i + 3 >= n:
                        self.log_estado(f"⚠️ Bloque incompleto al final", "warning", fila=i+1)
                        break
                    
                    row_datos_principales = df.iloc[i]
                    row_cantidades = df.iloc[i + 1]
                    row_fechas = df.iloc[i + 2]
                    row_bancos = df.iloc[i + 3]
                    
                    carnet_val = row_datos_principales.iloc[self.COL_CARNE]
                    
                    if self._is_empty(carnet_val):
                        i += 4
                        continue
                    
                    carnet = self.limpiar_texto(carnet_val)
                    if not carnet:
                        i += 4
                        continue
                    
                    # ✅ NORMALIZAR CARNÉ (aplicar reglas: quitar espacios, AMS→ASM, eliminar guiones)
                    carnet = self.normalizar_carnet(carnet)
                    
                    if not self._es_carnet_valido(carnet):
                        self.log_estado(f"⚠️ Carné inválido", "debug", carnet=carnet, fila=i+1)
                        i += 4
                        continue
                    
                    if carnet in self.estadisticas['carnets_procesados']:
                        self.estadisticas['carnets_duplicados'][carnet] += 1
                        self.log_estado(
                            f"ℹ️ Carné duplicado (puede ser múltiples programas)",
                            "info",
                            carnet=carnet,
                            ocurrencias=self.estadisticas['carnets_duplicados'][carnet] + 1
                        )
                    
                    self.estadisticas['carnets_procesados'].add(carnet)
                    
                    nombre = self.limpiar_texto(row_datos_principales.iloc[self.COL_NOMBRE]) or "Sin nombre"
                    plan_raw = row_datos_principales.iloc[self.COL_PLAN]
                    plan_estudios = self.obtener_programa(plan_raw)
                    
                    asesor = self.limpiar_texto(row_datos_principales.iloc[self.COL_ASESOR])
                    empresa = self.limpiar_texto(row_datos_principales.iloc[self.COL_EMPRESA])
                    telefono = self.limpiar_texto(row_datos_principales.iloc[self.COL_TELEFONO])
                    
                    estatus_raw = row_datos_principales.iloc[self.COL_ESTATUS] if self.COL_ESTATUS < len(row_datos_principales) else None
                    estatus = self.limpiar_texto(estatus_raw)
                    
                    if not estatus or estatus.lower() in ['', 'na', 'n/a']:
                        estatus = "Activo"
                        self.estadisticas['estudiantes_activos'] += 1
                    else:
                        if 'inactiv' in estatus.lower() or 'baja' in estatus.lower():
                            estatus = "Inactivo"
                            self.estadisticas['estudiantes_inactivos'] += 1
                        else:
                            estatus = "Activo"
                            self.estadisticas['estudiantes_activos'] += 1
                    
                    mail = self.limpiar_texto(row_datos_principales.iloc[self.COL_MAIL])
                    mes_inicio = self.limpiar_texto(row_datos_principales.iloc[self.COL_MES_INICIO])
                    valor_total = self.limpiar_monto(row_datos_principales.iloc[self.COL_VALOR_TOTAL])
                    
                    self.log_estado(
                        f"👤 Procesando",
                        carnet=carnet,
                        nombre=nombre[:30],
                        plan=plan_estudios,
                        estatus=estatus
                    )
                    
                    pagos_estudiante: List[Dict[str, Any]] = []
                    
                    pagos_estudiante.extend(
                        self._procesar_columnas_especiales(
                            row_datos_principales,
                            row_cantidades,
                            row_fechas,
                            row_bancos,
                            carnet,
                            nombre,
                            plan_estudios,
                            estatus
                        )
                    )
                    
                    pagos_estudiante.extend(
                        self._procesar_columnas_meses(
                            row_datos_principales,
                            row_cantidades,
                            row_fechas,
                            row_bancos,
                            columnas_info,
                            carnet,
                            nombre,
                            plan_estudios,
                            estatus,
                            mes_inicio
                        )
                    )
                    
                    pagos.extend(pagos_estudiante)
                    self.estadisticas['estudiantes_procesados'] += 1
                    
                    if not pagos_estudiante:
                        self.estadisticas['estudiantes_sin_pagos'] += 1
                        self.log_estado(f"⚠️ Sin pagos válidos", "warning", carnet=carnet)
                    else:
                        self.log_estado(
                            f"✅ Procesado exitosamente",
                            carnet=carnet,
                            pagos=len(pagos_estudiante)
                        )
                    
                    i += 4

                except Exception as e:
                    self.log_estado(f"❌ Error en bloque", "error", fila=i+1, error=str(e)[:200])
                    self.estadisticas['errores'] += 1
                    self.estadisticas['filas_problematicas'].append(i+1)
                    i += 4
                    continue

            self.generar_reporte_final(pagos)
            return pagos

        except FileNotFoundError as e:
            self.log_estado(f"❌ {e}", "error")
            return []
        except Exception as e:
            self.log_estado(f"❌ Error fatal: {e}", "error")
            import traceback
            traceback.print_exc()
            return []

    def _construir_mapa_columnas(self, años_row, headers_row) -> List[Dict]:
        """Construye un mapa de columnas con información de año y mes."""
        columnas_info = []
        año_actual = None
        
        for idx in range(len(headers_row)):
            año_celda = años_row.iloc[idx] if idx < len(años_row) else None
            header_celda = headers_row.iloc[idx] if idx < len(headers_row) else None
            
            if not self._is_empty(año_celda):
                try:
                    año_actual = int(float(str(año_celda).strip()))
                except (ValueError, TypeError):
                    pass
            
            columnas_info.append({
                'indice': idx,
                'año': año_actual,
                'nombre': self.limpiar_texto(header_celda),
                'mes_numero': self._extraer_mes_de_nombre_columna(str(header_celda)) if header_celda else None
            })
        
        self.log_estado(
            f"🗂️ Mapa de columnas construido",
            columnas_con_año=sum(1 for c in columnas_info if c['año']),
            columnas_meses=sum(1 for c in columnas_info if c['mes_numero'])
        )
        
        return columnas_info

    def _procesar_columnas_especiales(
        self,
        row_datos,
        row_cantidades,
        row_fechas,
        row_bancos,
        carnet,
        nombre,
        plan_estudios,
        estatus
    ) -> List[Dict[str, Any]]:
        """Procesa las columnas especiales antes de los meses."""
        pagos = []
        
        columnas_especiales = [
            {'nombre': 'Pago de casos', 'inicio': self.COL_PAGO_CASOS_START},
            {'nombre': 'Certificación Internacional', 'inicio': self.COL_CERTIFICACION_START},
            {'nombre': 'Títulos', 'inicio': self.COL_TITULOS_START},
            {'nombre': 'Capstone Project', 'inicio': self.COL_CAPSTONE_START},
            {'nombre': 'Graduación', 'inicio': self.COL_GRADUACION_START},
        ]
        
        for col_especial in columnas_especiales:
            try:
                idx_inicio = col_especial['inicio']
                
                boleta_raw = row_datos.iloc[idx_inicio] if idx_inicio < len(row_datos) else None
                boletas = self.extraer_valores_multiples(boleta_raw)
                
                monto_raw = row_cantidades.iloc[idx_inicio] if idx_inicio < len(row_cantidades) else None
                montos = self.extraer_valores_multiples(monto_raw)
                
                fecha_raw = row_fechas.iloc[idx_inicio] if idx_inicio < len(row_fechas) else None
                fechas = self.extraer_valores_multiples(fecha_raw)
                
                banco_raw = row_bancos.iloc[idx_inicio] if idx_inicio < len(row_bancos) else None
                bancos = self.extraer_valores_multiples(banco_raw)
                
                if not self._validar_balance_pagos_multiples(
                    boletas, montos, fechas, bancos, carnet, col_especial['nombre']
                ):
                    self.log_estado(
                        "⚠️ Intentando reconciliar pagos múltiples desbalanceados",
                        "warning",
                        carnet=carnet,
                        concepto=col_especial['nombre']
                    )
                    boletas, montos, fechas, bancos = self._auto_reconciliar_pagos_multiples(
                        boletas, montos, fechas, bancos, carnet, col_especial['nombre']
                    )
                
                max_items = max(len(boletas), len(montos), len(fechas), len(bancos))
                
                for i in range(max_items):
                    boleta = boletas[i] if i < len(boletas) else None
                    monto = self.limpiar_monto(montos[i]) if i < len(montos) else None
                    fecha = self.parse_fecha_mejorada(
                        fechas[i] if i < len(fechas) else None,
                        año_contexto=2020
                    )
                    banco = self.detectar_banco(bancos[i]) if i < len(bancos) else "No especificado"
                    
                    if boleta and monto:
                        pago = {
                            'carnet': carnet,
                            'nombre_estudiante': nombre,
                            'plan_estudios': plan_estudios,
                            'estatus': estatus,
                            'numero_boleta': boleta,
                            'monto': monto,
                            'fecha_pago': fecha,
                            'banco': banco,
                            'concepto': col_especial['nombre'],
                            'mes_pago': None,
                            'tipo_pago': 'Especial',
                        }
                        
                        pagos.append(pago)
                        self.estadisticas['pagos_extraidos'] += 1
                        self.estadisticas['pagos_especiales'] += 1
                
            except Exception as e:
                self.log_estado(
                    f"Error procesando columna especial",
                    "debug",
                    columna=col_especial['nombre'],
                    error=str(e)[:100]
                )
        
        return pagos

    def _procesar_columnas_meses(
        self,
        row_datos,
        row_cantidades,
        row_fechas,
        row_bancos,
        columnas_info,
        carnet,
        nombre,
        plan_estudios,
        estatus,
        mes_inicio
    ) -> List[Dict[str, Any]]:
        """Procesa las columnas de meses."""
        pagos = []
        
        columnas_meses = [c for c in columnas_info if c['indice'] >= self.COL_MESES_START and c['mes_numero']]
        
        for col_info in columnas_meses:
            try:
                idx = col_info['indice']
                año_col = col_info['año']
                mes_nombre = col_info['nombre']
                mes_numero = col_info['mes_numero']
                
                boleta_raw = row_datos.iloc[idx] if idx < len(row_datos) else None
                boletas = self.extraer_valores_multiples(boleta_raw)
                
                monto_raw = row_cantidades.iloc[idx] if idx < len(row_cantidades) else None
                montos = self.extraer_valores_multiples(monto_raw)
                
                fecha_raw = row_fechas.iloc[idx] if idx < len(row_fechas) else None
                fechas = self.extraer_valores_multiples(fecha_raw)
                
                banco_raw = row_bancos.iloc[idx] if idx < len(row_bancos) else None
                bancos = self.extraer_valores_multiples(banco_raw)
                
                if not self._validar_balance_pagos_multiples(
                    boletas, montos, fechas, bancos, carnet, f"Mes {mes_nombre}"
                ):
                    self.log_estado(
                        "⚠️ Intentando reconciliar pagos múltiples desbalanceados",
                        "warning",
                        carnet=carnet,
                        concepto=f"Mes {mes_nombre}"
                    )
                    boletas, montos, fechas, bancos = self._auto_reconciliar_pagos_multiples(
                        boletas, montos, fechas, bancos, carnet, f"Mes {mes_nombre}"
                    )
                
                max_items = max(len(boletas), len(montos), len(fechas), len(bancos))
                
                for i in range(max_items):
                    boleta = boletas[i] if i < len(boletas) else None
                    monto = self.limpiar_monto(montos[i]) if i < len(montos) else None
                    fecha_str = fechas[i] if i < len(fechas) else None
                    banco = self.detectar_banco(bancos[i]) if i < len(bancos) else "No especificado"
                    
                    fecha = self.parse_fecha_mejorada(
                        fecha_str,
                        año_contexto=año_col,
                        mes_nombre=mes_nombre,
                        año_columna=año_col
                    )
                    
                    if boleta and monto:
                        pago = {
                            'carnet': carnet,
                            'nombre_estudiante': nombre,
                            'plan_estudios': plan_estudios,
                            'estatus': estatus,
                            'numero_boleta': boleta,
                            'monto': monto,
                            'fecha_pago': fecha,
                            'banco': banco,
                            'concepto': 'Cuota mensual',
                            'mes_pago': mes_nombre,
                            'tipo_pago': 'Mensual',
                            'año': año_col,
                        }
                        
                        pagos.append(pago)
                        self.estadisticas['pagos_extraidos'] += 1
                        self.estadisticas['pagos_mensuales'] += 1
                
            except Exception as e:
                self.log_estado(
                    f"Error procesando mes",
                    "debug",
                    columna=idx,
                    mes=col_info.get('nombre'),
                    error=str(e)[:100]
                )
        
        return pagos

    def _es_carnet_valido(self, carnet: str) -> bool:
        """Valida formato de carné."""
        if not carnet or len(carnet) < 5 or len(carnet) > 20:
            return False
        if not re.search(r'\d', carnet):
            return False
        if carnet.isdigit():
            return False
        if not carnet[0].isalpha():
            return False
        return True

    # ========== GENERACIÓN DE ARCHIVOS ==========
    def generar_excel_normalizado_en_bloques(self, pagos: List[Dict[str, Any]], archivo_salida: str) -> List[str]:
        """
        ✅ MEJORADO: Genera archivos preservando integridad de estudiantes.
        """
        if not pagos:
            self.log_estado("⚠️ No hay pagos para exportar", "warning")
            return []

        try:
            df = pd.DataFrame(pagos)
            df['numero_boleta'] = df['numero_boleta'].astype(str)
            df['monto'] = pd.to_numeric(df['monto'], errors='coerce')
            df = df.sort_values(['carnet', 'fecha_pago'], na_position='last')

            columnas_export = [
                'carnet',
                'nombre_estudiante',
                'plan_estudios',
                'estatus',
                'numero_boleta',
                'monto',
                'fecha_pago',
                'banco',
                'concepto',
                'tipo_pago',
                'mes_pago',
                'año'
            ]
            
            columnas_export = [c for c in columnas_export if c in df.columns]
            df_export = df[columnas_export]
            total_registros = len(df_export)
            
            archivos_generados = []
            archivo_path = Path(archivo_salida)
            nombre_base = archivo_path.stem
            extension = archivo_path.suffix
            directorio = archivo_path.parent
            
            # ✅ DIVISIÓN INTELIGENTE POR ESTUDIANTE
            carnets_unicos = df_export['carnet'].unique()
            total_carnets = len(carnets_unicos)
            
            self.log_estado(
                f"📦 Preparando división en bloques",
                total_registros=total_registros,
                total_carnets=total_carnets,
                tamaño_bloque=self.TAMAÑO_BLOQUE
            )
            
            bloques = []
            bloque_actual = []
            registros_actual = 0
            
            for carnet in carnets_unicos:
                registros_estudiante = df_export[df_export['carnet'] == carnet]
                num_registros = len(registros_estudiante)
                
                if registros_actual + num_registros > self.TAMAÑO_BLOQUE and bloque_actual:
                    bloques.append(bloque_actual)
                    bloque_actual = [carnet]
                    registros_actual = num_registros
                else:
                    bloque_actual.append(carnet)
                    registros_actual += num_registros
            
            if bloque_actual:
                bloques.append(bloque_actual)
            
            num_bloques = len(bloques)
            
            self.log_estado(
                f"✅ División optimizada",
                bloques=num_bloques,
                promedio_estudiantes_por_bloque=total_carnets // num_bloques if num_bloques > 0 else 0
            )
            
            for i, carnets_bloque in enumerate(bloques):
                df_bloque = df_export[df_export['carnet'].isin(carnets_bloque)]
                
                if num_bloques > 1:
                    nombre_archivo = f"{nombre_base}_parte_{i+1}_de_{num_bloques}{extension}"
                else:
                    nombre_archivo = f"{nombre_base}{extension}"
                
                ruta_archivo = directorio / nombre_archivo
                
                if ruta_archivo.exists():
                    ruta_archivo.unlink()
                
                with pd.ExcelWriter(ruta_archivo, engine='openpyxl') as writer:
                    df_bloque.to_excel(writer, index=False, sheet_name='Pagos')
                    
                    worksheet = writer.sheets['Pagos']
                    for idx, col in enumerate(df_bloque.columns, 1):
                        max_length = max(
                            df_bloque[col].astype(str).str.len().max(),
                            len(col)
                        )
                        col_letter = chr(64 + idx) if idx <= 26 else 'A' + chr(64 + idx - 26)
                        worksheet.column_dimensions[col_letter].width = min(max_length + 2, 50)
                
                archivos_generados.append(str(ruta_archivo))
                self.estadisticas['bloques_generados'] += 1
                
                self.log_estado(
                    f"✅ Bloque {i+1}/{num_bloques} guardado",
                    archivo=nombre_archivo,
                    registros=len(df_bloque),
                    estudiantes=len(carnets_bloque)
                )
            
            return archivos_generados
            
        except Exception as e:
            self.log_estado(f"❌ Error guardando archivos: {e}", "error")
            import traceback
            traceback.print_exc()
            return []

    # ========== REPORTES ==========
    def generar_reporte_final(self, pagos: List[Dict[str, Any]]):
        """✅ MEJORADO: Reporte con nuevas métricas."""
        if self.estadisticas['inicio_procesamiento']:
            tiempo_total = datetime.now() - self.estadisticas['inicio_procesamiento']
            tiempo_str = str(tiempo_total).split('.')[0]
        else:
            tiempo_str = "N/A"
        
        total_intentos = self.estadisticas['fechas_parseadas'] + self.estadisticas['fechas_fallidas']
        tasa_exito_fechas = (
            (self.estadisticas['fechas_parseadas'] / total_intentos * 100)
            if total_intentos > 0 else 0
        )
        
        top_bancos = sorted(
            self.estadisticas['bancos_detectados'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        top_planes = sorted(
            self.estadisticas['planes_detectados'].items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        rep = f"""
{'='*90}
📊 REPORTE FINAL DE PROCESAMIENTO v3.1
{'='*90}
⏰ Tiempo total: {tiempo_str}
📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
👤 Usuario: AndresSantosSotec

👥 ESTUDIANTES:
   • Procesados: {self.estadisticas['estudiantes_procesados']}
   • Activos: {self.estadisticas['estudiantes_activos']}
   • Inactivos: {self.estadisticas['estudiantes_inactivos']}
   • Sin pagos: {self.estadisticas['estudiantes_sin_pagos']}
   • Carnés únicos: {len(self.estadisticas['carnets_procesados'])}
   • Carnés duplicados: {len([k for k, v in self.estadisticas['carnets_duplicados'].items() if v > 0])}
   • 🔄 Carnés normalizados (AMS→ASM): {self.estadisticas['carnets_normalizados']}
   • 🔧 Carnés compactados (guiones removidos): {self.estadisticas['carnets_compactados']}

💰 PAGOS:
   • Total extraídos: {self.estadisticas['pagos_extraidos']}
   • Pagos mensuales: {self.estadisticas['pagos_mensuales']}
   • Pagos especiales: {self.estadisticas['pagos_especiales']}
   • Pagos múltiples detectados: {self.estadisticas['pagos_multiples_detectados']}
   • ⚠️ Pagos múltiples desbalanceados: {self.estadisticas['pagos_multiples_desbalanceados']}
   • 💸 Montos negativos (reembolsos): {self.estadisticas['montos_negativos']}

📅 FECHAS:
   • Parseadas: {self.estadisticas['fechas_parseadas']}
   • Fallidas: {self.estadisticas['fechas_fallidas']}
   • Tasa de éxito: {tasa_exito_fechas:.1f}%
   • Cambios de año detectados: {self.estadisticas['fechas_cambio_año']}
   • Fechas corregidas: {self.estadisticas['fechas_corregidas']}

📚 PLANES DE ESTUDIO:
"""
        for plan, count in top_planes:
            rep += f"   • {plan}: {count}\n"
        
        rep += f"\n🏦 BANCOS (Top 5):\n"
        for banco, count in top_bancos:
            rep += f"   • {banco}: {count}\n"
        
        rep += f"""
❌ ERRORES: {self.estadisticas['errores']}
📦 BLOQUES GENERADOS: {self.estadisticas['bloques_generados']}
{'='*90}
"""
        print(rep)
        self.log_estado("✅ Procesamiento completado")


# ========== FUNCIÓN PRINCIPAL ==========
def procesar_archivo_v3(entrada: str, salida: str):
    """Función principal."""
    print("🚀 PROCESADOR DE PAGOS V3.1")
    print("="*90)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"👤 Usuario: AndresSantosSotec")
    print("="*90)
    
    processor = ExcelPaymentProcessorV3(log_level=logging.INFO)
    
    pagos = processor.procesar_excel_v3(entrada)
    
    if pagos:
        archivos = processor.generar_excel_normalizado_en_bloques(pagos, salida)
        if archivos:
            print("\n✅ PROCESO COMPLETADO")
            print(f"📊 Total de pagos: {len(pagos)}")
            print(f"📦 Archivos generados: {len(archivos)}")
            for archivo in archivos:
                print(f"   • {archivo}")
    else:
        print("\n❌ NO SE PUDIERON EXTRAER PAGOS")


def main():
    """Función principal del script."""
    archivo_entrada = "pagos_originales.xlsx"
    archivo_salida = "pagos_normalizados_v3.1.xlsx"
    
    if not Path(archivo_entrada).exists():
        print(f"❌ ERROR: Archivo no encontrado '{archivo_entrada}'")
        return
    
    procesar_archivo_v3(archivo_entrada, archivo_salida)


if __name__ == "__main__":
    main()