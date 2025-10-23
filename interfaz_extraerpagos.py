#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interfaz gráfica para el procesador de pagos
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
    """Interfaz gráfica para procesar archivos de pagos"""
    
    def __init__(self):
        super().__init__()
        
        # Configuración de ventana
        self.title("Procesador de Pagos - v3.1")
        self.geometry("800x600")
        self.minsize(700, 500)
        
        # Variables
        self.archivo_entrada = None
        self.carpeta_salida = None
        self.procesando = False
        
        # Crear interfaz
        self.crear_interfaz()
        
        # Centrar ventana
        self.centrar_ventana()
    
    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def crear_interfaz(self):
        """Crea todos los elementos de la interfaz"""
        
        # Frame principal con padding
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        titulo = ctk.CTkLabel(
            main_frame,
            text="Procesador de Pagos",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        titulo.pack(pady=(0, 10))
        
        subtitulo = ctk.CTkLabel(
            main_frame,
            text="Versión 3.1 - Procesamiento de archivos Excel y CSV",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitulo.pack(pady=(0, 30))
        
        # Frame para selección de archivo
        frame_archivo = ctk.CTkFrame(main_frame)
        frame_archivo.pack(fill="x", pady=10)
        
        label_archivo = ctk.CTkLabel(
            frame_archivo,
            text="1. Seleccionar archivo de entrada:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        label_archivo.pack(anchor="w", padx=15, pady=(15, 5))
        
        frame_archivo_btn = ctk.CTkFrame(frame_archivo, fg_color="transparent")
        frame_archivo_btn.pack(fill="x", padx=15, pady=(0, 15))
        
        self.btn_seleccionar = ctk.CTkButton(
            frame_archivo_btn,
            text="📁 Seleccionar Archivo",
            command=self.seleccionar_archivo,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.btn_seleccionar.pack(side="left", padx=(0, 10))
        
        self.label_archivo_seleccionado = ctk.CTkLabel(
            frame_archivo_btn,
            text="Ningún archivo seleccionado",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.label_archivo_seleccionado.pack(side="left", fill="x", expand=True)
        
        # Frame para carpeta de salida
        frame_salida = ctk.CTkFrame(main_frame)
        frame_salida.pack(fill="x", pady=10)
        
        label_salida = ctk.CTkLabel(
            frame_salida,
            text="2. Seleccionar carpeta de salida:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        label_salida.pack(anchor="w", padx=15, pady=(15, 5))
        
        frame_salida_btn = ctk.CTkFrame(frame_salida, fg_color="transparent")
        frame_salida_btn.pack(fill="x", padx=15, pady=(0, 15))
        
        self.btn_carpeta = ctk.CTkButton(
            frame_salida_btn,
            text="📂 Seleccionar Carpeta",
            command=self.seleccionar_carpeta,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.btn_carpeta.pack(side="left", padx=(0, 10))
        
        self.label_carpeta_seleccionada = ctk.CTkLabel(
            frame_salida_btn,
            text="Se usará la carpeta actual por defecto",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.label_carpeta_seleccionada.pack(side="left", fill="x", expand=True)
        
        # Frame de progreso
        frame_progreso = ctk.CTkFrame(main_frame)
        frame_progreso.pack(fill="both", expand=True, pady=10)
        
        label_progreso = ctk.CTkLabel(
            frame_progreso,
            text="3. Procesamiento:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        label_progreso.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Barra de progreso
        self.progress_bar = ctk.CTkProgressBar(frame_progreso, mode="indeterminate")
        self.progress_bar.pack(fill="x", padx=15, pady=10)
        self.progress_bar.set(0)
        
        # Área de texto para logs
        self.text_log = ctk.CTkTextbox(
            frame_progreso,
            height=200,
            font=ctk.CTkFont(family="Courier", size=11)
        )
        self.text_log.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.text_log.insert("1.0", "✓ Interfaz lista. Seleccione un archivo para comenzar.\n")
        self.text_log.configure(state="disabled")
        
        # Frame de botones de acción
        frame_botones = ctk.CTkFrame(main_frame, fg_color="transparent")
        frame_botones.pack(fill="x", pady=10)
        
        self.btn_procesar = ctk.CTkButton(
            frame_botones,
            text="▶ Procesar Archivo",
            command=self.procesar_archivo,
            width=250,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        self.btn_procesar.pack(side="left", padx=5)
        self.btn_procesar.configure(state="disabled")
        
        self.btn_abrir_carpeta = ctk.CTkButton(
            frame_botones,
            text="📁 Abrir Carpeta de Resultados",
            command=self.abrir_carpeta_resultados,
            width=250,
            height=50,
            font=ctk.CTkFont(size=16),
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        self.btn_abrir_carpeta.pack(side="left", padx=5)
        self.btn_abrir_carpeta.configure(state="disabled")
        
        self.btn_limpiar = ctk.CTkButton(
            frame_botones,
            text="🔄 Limpiar",
            command=self.limpiar,
            width=150,
            height=50,
            font=ctk.CTkFont(size=16),
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
