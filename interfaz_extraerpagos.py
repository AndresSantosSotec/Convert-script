#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interfaz gráfica para el procesador de pagos
Versión 3.2 - Con responsividad mejorada para múltiples tamaños de pantalla
Autor: AndresSantosSotec
Fecha: 2025-01-17
"""

import os
import sys
import threading
from pathlib import Path
from tkinter import filedialog, messagebox
import customtkinter as ctk
from extraer_pagos import ExcelPaymentProcessorV3, procesar_archivo_v3
import logging

# Configuración de CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class InterfazExtraerPagos(ctk.CTk):
    """Interfaz gráfica para procesar archivos de pagos con diseño responsivo"""
    
    def __init__(self):
        super().__init__()
        
        # Obtener dimensiones de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Detectar tipo de pantalla
        self.screen_type = self.detect_screen_type(screen_width, screen_height)
        
        # Calcular tamaño de ventana adaptativo según tipo de pantalla
        if self.screen_type == "mobile":
            # Pantallas móviles: usar casi toda la pantalla
            window_width = int(screen_width * 0.95)
            window_height = int(screen_height * 0.95)
        elif self.screen_type == "tablet":
            # Tablets: usar 85% de la pantalla
            window_width = int(screen_width * 0.85)
            window_height = int(screen_height * 0.85)
        else:
            # Desktop: usar 70% de la pantalla
            window_width = int(screen_width * 0.7)
            window_height = int(screen_height * 0.7)
        
        # Limitar tamaños mínimos y máximos
        window_width = max(500, min(window_width, 1600))
        window_height = max(400, min(window_height, 1200))
        
        # Calcular tamaños mínimos adaptativos
        min_width = max(450, int(screen_width * 0.35))
        min_height = max(350, int(screen_height * 0.35))
        
        # Configuración de ventana
        self.title("Procesador de Pagos - v3.2")
        self.geometry(f"{window_width}x{window_height}")
        self.minsize(min_width, min_height)
        
        # Variables
        self.archivo_entrada = None
        self.carpeta_salida = None
        self.procesando = False
        
        # Variables para responsividad
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Crear interfaz
        self.crear_interfaz()
        
        # Centrar ventana
        self.centrar_ventana()
        
        # Vincular evento de redimensionamiento para ajustes dinámicos
        self.bind("<Configure>", self.on_resize)
    
    def detect_screen_type(self, width, height):
        """Detecta el tipo de pantalla basándose en sus dimensiones"""
        # Pantallas móviles: < 768px de ancho
        if width < 768:
            return "mobile"
        # Tablets: entre 768px y 1024px
        elif width < 1024:
            return "tablet"
        # Desktop: >= 1024px
        else:
            return "desktop"
    
    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def get_responsive_font_size(self, base_size):
        """Calcula tamaño de fuente responsivo basado en el tipo de pantalla"""
        if self.screen_type == "mobile":
            return max(8, int(base_size * 0.75))
        elif self.screen_type == "tablet":
            return int(base_size * 0.85)
        elif self.screen_width < 1366:
            return int(base_size * 0.95)
        else:
            return base_size
    
    def get_responsive_button_size(self, base_width, base_height):
        """Calcula tamaño de botón responsivo basado en el tipo de pantalla"""
        if self.screen_type == "mobile":
            # En móviles, hacer botones más pequeños pero tactilmente adecuados
            return max(120, int(base_width * 0.7)), max(35, int(base_height * 0.8))
        elif self.screen_type == "tablet":
            return int(base_width * 0.85), int(base_height * 0.9)
        elif self.screen_width < 1366:
            return int(base_width * 0.95), int(base_height * 0.95)
        else:
            return base_width, base_height
    
    def get_responsive_padding(self, base_padding):
        """Calcula padding responsivo basado en el tipo de pantalla"""
        if self.screen_type == "mobile":
            return max(8, int(base_padding * 0.6))
        elif self.screen_type == "tablet":
            return max(10, int(base_padding * 0.75))
        elif self.screen_width < 1366:
            return int(base_padding * 0.85)
        else:
            return base_padding
    
    def on_resize(self, event):
        """Maneja el evento de redimensionamiento de ventana"""
        # Solo procesar eventos de la ventana principal
        if event.widget == self:
            # Actualizar el estado de responsividad si es necesario
            # En una implementación más avanzada, aquí podríamos
            # ajustar dinámicamente el layout cuando se redimensiona
            pass
    
    def crear_interfaz(self):
        """Crea todos los elementos de la interfaz"""
        
        # Calcular valores responsivos
        padding = self.get_responsive_padding(20)
        title_size = self.get_responsive_font_size(28)
        subtitle_size = self.get_responsive_font_size(14)
        
        # Frame principal con padding responsivo
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=padding, pady=padding)
        
        # Título con tamaño responsivo
        titulo = ctk.CTkLabel(
            main_frame,
            text="Procesador de Pagos",
            font=ctk.CTkFont(size=title_size, weight="bold")
        )
        titulo.pack(pady=(0, 10))
        
        # Subtítulo con tamaño responsivo
        subtitle_text = "Versión 3.2 - Diseño responsivo para todas las pantallas"
        if self.screen_type == "mobile":
            subtitle_text = "v3.2 - Adaptado para pantallas pequeñas"
        elif self.screen_type == "tablet":
            subtitle_text = "v3.2 - Optimizado para tablets"
        
        subtitulo = ctk.CTkLabel(
            main_frame,
            text=subtitle_text,
            font=ctk.CTkFont(size=subtitle_size),
            text_color="gray"
        )
        subtitulo.pack(pady=(0, self.get_responsive_padding(30)))
        
        # Frame para selección de archivo
        frame_archivo = ctk.CTkFrame(main_frame)
        frame_archivo.pack(fill="x", pady=10)
        
        label_size = self.get_responsive_font_size(16)
        label_archivo = ctk.CTkLabel(
            frame_archivo,
            text="1. Seleccionar archivo de entrada:",
            font=ctk.CTkFont(size=label_size, weight="bold")
        )
        label_archivo.pack(anchor="w", padx=15, pady=(15, 5))
        
        frame_archivo_btn = ctk.CTkFrame(frame_archivo, fg_color="transparent")
        frame_archivo_btn.pack(fill="x", padx=15, pady=(0, 15))
        
        btn_width, btn_height = self.get_responsive_button_size(200, 40)
        self.btn_seleccionar = ctk.CTkButton(
            frame_archivo_btn,
            text="📁 Seleccionar Archivo",
            command=self.seleccionar_archivo,
            width=btn_width,
            height=btn_height,
            font=ctk.CTkFont(size=self.get_responsive_font_size(14))
        )
        self.btn_seleccionar.pack(side="left", padx=(0, 10))
        
        self.label_archivo_seleccionado = ctk.CTkLabel(
            frame_archivo_btn,
            text="Ningún archivo seleccionado",
            font=ctk.CTkFont(size=self.get_responsive_font_size(12)),
            text_color="gray"
        )
        self.label_archivo_seleccionado.pack(side="left", fill="x", expand=True)
        
        # Frame para carpeta de salida
        frame_salida = ctk.CTkFrame(main_frame)
        frame_salida.pack(fill="x", pady=10)
        
        label_salida = ctk.CTkLabel(
            frame_salida,
            text="2. Seleccionar carpeta de salida:",
            font=ctk.CTkFont(size=label_size, weight="bold")
        )
        label_salida.pack(anchor="w", padx=15, pady=(15, 5))
        
        frame_salida_btn = ctk.CTkFrame(frame_salida, fg_color="transparent")
        frame_salida_btn.pack(fill="x", padx=15, pady=(0, 15))
        
        self.btn_carpeta = ctk.CTkButton(
            frame_salida_btn,
            text="📂 Seleccionar Carpeta",
            command=self.seleccionar_carpeta,
            width=btn_width,
            height=btn_height,
            font=ctk.CTkFont(size=self.get_responsive_font_size(14))
        )
        self.btn_carpeta.pack(side="left", padx=(0, 10))
        
        self.label_carpeta_seleccionada = ctk.CTkLabel(
            frame_salida_btn,
            text="Se usará la carpeta actual por defecto",
            font=ctk.CTkFont(size=self.get_responsive_font_size(12)),
            text_color="gray"
        )
        self.label_carpeta_seleccionada.pack(side="left", fill="x", expand=True)
        
        # Frame de progreso
        frame_progreso = ctk.CTkFrame(main_frame)
        frame_progreso.pack(fill="both", expand=True, pady=10)
        
        label_progreso = ctk.CTkLabel(
            frame_progreso,
            text="3. Procesamiento:",
            font=ctk.CTkFont(size=label_size, weight="bold")
        )
        label_progreso.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Barra de progreso
        self.progress_bar = ctk.CTkProgressBar(frame_progreso, mode="indeterminate")
        self.progress_bar.pack(fill="x", padx=15, pady=10)
        self.progress_bar.set(0)
        
        # Área de texto para logs - altura responsiva
        log_height = max(150, int(self.screen_height * 0.2))
        text_size = self.get_responsive_font_size(11)
        self.text_log = ctk.CTkTextbox(
            frame_progreso,
            height=log_height,
            font=ctk.CTkFont(family="Courier", size=text_size)
        )
        self.text_log.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.text_log.insert("1.0", "✓ Interfaz lista. Seleccione un archivo para comenzar.\n")
        self.text_log.configure(state="disabled")
        
        # Frame de botones de acción
        frame_botones = ctk.CTkFrame(main_frame, fg_color="transparent")
        frame_botones.pack(fill="x", pady=10)
        
        # Tamaños de botones de acción responsivos
        action_btn_width, action_btn_height = self.get_responsive_button_size(250, 50)
        clear_btn_width, clear_btn_height = self.get_responsive_button_size(150, 50)
        action_font_size = self.get_responsive_font_size(16)
        
        self.btn_procesar = ctk.CTkButton(
            frame_botones,
            text="▶ Procesar Archivo",
            command=self.procesar_archivo,
            width=action_btn_width,
            height=action_btn_height,
            font=ctk.CTkFont(size=action_font_size, weight="bold"),
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        self.btn_procesar.pack(side="left", padx=5)
        self.btn_procesar.configure(state="disabled")
        
        self.btn_abrir_carpeta = ctk.CTkButton(
            frame_botones,
            text="📁 Abrir Carpeta de Resultados",
            command=self.abrir_carpeta_resultados,
            width=action_btn_width,
            height=action_btn_height,
            font=ctk.CTkFont(size=action_font_size),
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        self.btn_abrir_carpeta.pack(side="left", padx=5)
        self.btn_abrir_carpeta.configure(state="disabled")
        
        self.btn_limpiar = ctk.CTkButton(
            frame_botones,
            text="🔄 Limpiar",
            command=self.limpiar,
            width=clear_btn_width,
            height=clear_btn_height,
            font=ctk.CTkFont(size=action_font_size),
            fg_color="#95a5a6",
            hover_color="#7f8c8d"
        )
        self.btn_limpiar.pack(side="right", padx=5)
    
    def agregar_log(self, mensaje):
        """Agrega un mensaje al área de logs"""
        self.text_log.configure(state="normal")
        self.text_log.insert("end", f"{mensaje}\n")
        self.text_log.see("end")
        self.text_log.configure(state="disabled")
        self.update()
    
    def seleccionar_archivo(self):
        """Abre diálogo para seleccionar archivo"""
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo de pagos",
            filetypes=[
                ("Archivos Excel", "*.xlsx"),
                ("Archivos CSV", "*.csv"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if archivo:
            self.archivo_entrada = archivo
            nombre_archivo = Path(archivo).name
            self.label_archivo_seleccionado.configure(
                text=f"✓ {nombre_archivo}",
                text_color="#2ecc71"
            )
            self.agregar_log(f"✓ Archivo seleccionado: {nombre_archivo}")
            self.btn_procesar.configure(state="normal")
    
    def seleccionar_carpeta(self):
        """Abre diálogo para seleccionar carpeta de salida"""
        carpeta = filedialog.askdirectory(
            title="Seleccionar carpeta de salida"
        )
        
        if carpeta:
            self.carpeta_salida = carpeta
            self.label_carpeta_seleccionada.configure(
                text=f"✓ {carpeta}",
                text_color="#2ecc71"
            )
            self.agregar_log(f"✓ Carpeta de salida: {carpeta}")
    
    def procesar_archivo(self):
        """Inicia el procesamiento del archivo en un hilo separado"""
        if not self.archivo_entrada:
            messagebox.showwarning(
                "Advertencia",
                "Por favor seleccione un archivo de entrada"
            )
            return
        
        if self.procesando:
            messagebox.showwarning(
                "Advertencia",
                "Ya hay un proceso en ejecución"
            )
            return
        
        # Deshabilitar botones
        self.btn_procesar.configure(state="disabled")
        self.btn_seleccionar.configure(state="disabled")
        self.btn_carpeta.configure(state="disabled")
        self.btn_limpiar.configure(state="disabled")
        self.procesando = True
        
        # Iniciar barra de progreso
        self.progress_bar.start()
        
        # Limpiar logs
        self.text_log.configure(state="normal")
        self.text_log.delete("1.0", "end")
        self.text_log.configure(state="disabled")
        
        self.agregar_log("="*60)
        self.agregar_log("🚀 INICIANDO PROCESAMIENTO...")
        self.agregar_log("="*60)
        
        # Ejecutar en hilo separado
        thread = threading.Thread(target=self._ejecutar_procesamiento, daemon=True)
        thread.start()
    
    def _ejecutar_procesamiento(self):
        """Ejecuta el procesamiento en un hilo separado"""
        try:
            # Determinar carpeta de salida
            if self.carpeta_salida:
                carpeta_salida = Path(self.carpeta_salida)
            else:
                carpeta_salida = Path(self.archivo_entrada).parent
            
            # Crear nombre de archivo de salida
            nombre_base = Path(self.archivo_entrada).stem
            archivo_salida = carpeta_salida / f"{nombre_base}_procesado.xlsx"
            
            self.agregar_log(f"📄 Archivo entrada: {self.archivo_entrada}")
            self.agregar_log(f"📂 Carpeta salida: {carpeta_salida}")
            self.agregar_log("")
            
            # Crear procesador con logging custom
            class GUILogHandler(logging.Handler):
                def __init__(self, gui_callback):
                    super().__init__()
                    self.gui_callback = gui_callback
                
                def emit(self, record):
                    msg = self.format(record)
                    # Filtrar algunos mensajes muy verbosos
                    if "debug" not in msg.lower() or "ERROR" in msg or "WARNING" in msg:
                        self.gui_callback(msg)
            
            # Configurar logging
            processor = ExcelPaymentProcessorV3(log_level=logging.INFO)
            gui_handler = GUILogHandler(self.agregar_log)
            gui_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
            processor.logger.addHandler(gui_handler)
            
            self.agregar_log("⏳ Procesando archivo...")
            
            # Procesar
            pagos = processor.procesar_excel_v3(self.archivo_entrada)
            
            if pagos:
                self.agregar_log("")
                self.agregar_log("💾 Generando archivos de salida...")
                archivos = processor.generar_excel_normalizado_en_bloques(
                    pagos, 
                    str(archivo_salida)
                )
                
                if archivos:
                    self.agregar_log("")
                    self.agregar_log("="*60)
                    self.agregar_log("✅ PROCESO COMPLETADO EXITOSAMENTE")
                    self.agregar_log("="*60)
                    self.agregar_log(f"📊 Total de pagos procesados: {len(pagos)}")
                    self.agregar_log(f"📦 Archivos generados: {len(archivos)}")
                    self.agregar_log("")
                    for archivo in archivos:
                        archivo_path = Path(archivo)
                        self.agregar_log(f"   ✓ {archivo_path.name}")
                    
                    # Habilitar botón para abrir carpeta
                    self.after(0, lambda: self.btn_abrir_carpeta.configure(state="normal"))
                    
                    # Mostrar mensaje de éxito
                    self.after(0, lambda: messagebox.showinfo(
                        "Éxito",
                        f"Procesamiento completado!\n\n"
                        f"Pagos procesados: {len(pagos)}\n"
                        f"Archivos generados: {len(archivos)}\n\n"
                        f"Ubicación: {carpeta_salida}"
                    ))
                else:
                    raise Exception("No se pudieron generar los archivos de salida")
            else:
                raise Exception("No se pudieron extraer pagos del archivo")
                
        except Exception as e:
            self.agregar_log("")
            self.agregar_log("="*60)
            self.agregar_log(f"❌ ERROR: {str(e)}")
            self.agregar_log("="*60)
            
            self.after(0, lambda: messagebox.showerror(
                "Error",
                f"Ocurrió un error durante el procesamiento:\n\n{str(e)}"
            ))
        
        finally:
            # Detener barra de progreso y rehabilitar botones
            self.after(0, self._finalizar_procesamiento)
    
    def _finalizar_procesamiento(self):
        """Finaliza el procesamiento y restaura la interfaz"""
        self.progress_bar.stop()
        self.progress_bar.set(0)
        self.procesando = False
        self.btn_procesar.configure(state="normal")
        self.btn_seleccionar.configure(state="normal")
        self.btn_carpeta.configure(state="normal")
        self.btn_limpiar.configure(state="normal")
    
    def abrir_carpeta_resultados(self):
        """Abre la carpeta de resultados en el explorador"""
        try:
            if self.carpeta_salida:
                carpeta = self.carpeta_salida
            elif self.archivo_entrada:
                carpeta = str(Path(self.archivo_entrada).parent)
            else:
                carpeta = os.getcwd()
            
            # Abrir carpeta según el sistema operativo
            if sys.platform == 'win32':
                os.startfile(carpeta)
            elif sys.platform == 'darwin':  # macOS
                os.system(f'open "{carpeta}"')
            else:  # Linux
                os.system(f'xdg-open "{carpeta}"')
                
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo abrir la carpeta:\n{str(e)}"
            )
    
    def limpiar(self):
        """Limpia la interfaz y reinicia el estado"""
        if self.procesando:
            messagebox.showwarning(
                "Advertencia",
                "No se puede limpiar mientras hay un proceso en ejecución"
            )
            return
        
        self.archivo_entrada = None
        self.carpeta_salida = None
        
        self.label_archivo_seleccionado.configure(
            text="Ningún archivo seleccionado",
            text_color="gray"
        )
        self.label_carpeta_seleccionada.configure(
            text="Se usará la carpeta actual por defecto",
            text_color="gray"
        )
        
        self.text_log.configure(state="normal")
        self.text_log.delete("1.0", "end")
        self.text_log.insert("1.0", "✓ Interfaz lista. Seleccione un archivo para comenzar.\n")
        self.text_log.configure(state="disabled")
        
        self.btn_procesar.configure(state="disabled")
        self.btn_abrir_carpeta.configure(state="disabled")
        
        self.progress_bar.set(0)


def main():
    """Función principal"""
    app = InterfazExtraerPagos()
    app.mainloop()


if __name__ == "__main__":
    main()
