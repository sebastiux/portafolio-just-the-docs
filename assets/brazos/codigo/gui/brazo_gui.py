#!/usr/bin/env python3
"""brazo_gui.py — Control de los brazos robóticos desde la computadora por USB.

Habla con firmware_brazo (ESP32-C3) usando el protocolo de texto de
puerto_serie.h:  J <art> <grados> | P A|C | H | E

Uso:
    pip install -r requirements.txt
    python brazo_gui.py                 # elegir el puerto en la ventana
    python brazo_gui.py --puerto COM5   # o indicarlo directamente

Integración Mecatrónica Otoño 2026
Juan Pablo Martha · Carlos Sebastián Ortega · Santiago Alejandro Velázquez
"""
import argparse
import json
import queue
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox

import serial
import serial.tools.list_ports

BAUDIOS = 115200
PERIODO_ESTADO_MS = 500      # cada cuánto se pide el estado al brazo
PERIODO_ENVIO_S = 0.08       # mínimo entre órdenes al arrastrar un deslizador
ARTICULACIONES_DESLIZABLES = 3   # base, hombro y codo; la pinza va con botones


class EnlaceSerie:
    """Puerto serie en un hilo aparte: la ventana nunca se congela esperando al brazo."""

    def __init__(self):
        self.puerto = None
        self.respuestas = queue.Queue()
        self._hilo = None
        self._activo = False
        self._candado = threading.Lock()

    def conectar(self, nombre):
        self.desconectar()
        self.puerto = serial.Serial(nombre, BAUDIOS, timeout=0.1)
        time.sleep(0.3)                  # el USB CDC del ESP32-C3 tarda un poco en estar listo
        self.puerto.reset_input_buffer()
        self._activo = True
        self._hilo = threading.Thread(target=self._leer, daemon=True)
        self._hilo.start()

    def desconectar(self):
        self._activo = False
        if self.puerto and self.puerto.is_open:
            self.puerto.close()
        self.puerto = None

    @property
    def conectado(self):
        return self.puerto is not None and self.puerto.is_open

    def enviar(self, orden):
        if not self.conectado:
            return
        with self._candado:
            self.puerto.write((orden + "\n").encode("ascii"))

    def _leer(self):
        while self._activo:
            try:
                linea = self.puerto.readline().decode("utf-8", errors="replace").strip()
            except (serial.SerialException, OSError, TypeError):
                self.respuestas.put(("desconectado", None))
                return
            if linea:
                self.respuestas.put(("linea", linea))


class Aplicacion(tk.Tk):
    def __init__(self, puerto_inicial=None):
        super().__init__()
        self.title("Brazo robótico · ESP32-C3")
        self.resizable(False, False)
        self.enlace = EnlaceSerie()
        self.deslizadores = []
        self.etiquetas = []
        self.arrastrando = None
        self.ultimo_envio = 0.0
        self._construir()
        self._listar_puertos(puerto_inicial)
        if puerto_inicial:
            self._conectar()
        self.after(50, self._procesar_respuestas)
        self.after(PERIODO_ESTADO_MS, self._pedir_estado)
        self.protocol("WM_DELETE_WINDOW", self._cerrar)

    # ----- ventana -------------------------------------------------------
    def _construir(self):
        marco = ttk.Frame(self, padding=12)
        marco.grid()

        conexion = ttk.LabelFrame(marco, text="Conexión", padding=8)
        conexion.grid(row=0, column=0, sticky="ew")
        self.puertos = ttk.Combobox(conexion, width=28, state="readonly")
        self.puertos.grid(row=0, column=0, padx=(0, 6))
        ttk.Button(conexion, text="↻", width=3, command=self._listar_puertos).grid(row=0, column=1)
        self.boton_conectar = ttk.Button(conexion, text="Conectar", command=self._conectar)
        self.boton_conectar.grid(row=0, column=2, padx=(6, 0))
        self.estado = ttk.Label(conexion, text="Sin conectar", foreground="#6B7280")
        self.estado.grid(row=1, column=0, columnspan=3, sticky="w", pady=(6, 0))

        self.marco_arts = ttk.LabelFrame(marco, text="Articulaciones", padding=8)
        self.marco_arts.grid(row=1, column=0, sticky="ew", pady=10)
        for i, nombre in enumerate(["Base", "Hombro", "Codo"]):
            ttk.Label(self.marco_arts, text=nombre, width=8).grid(row=i, column=0, sticky="w")
            d = ttk.Scale(self.marco_arts, from_=0, to=180, length=280,
                          command=lambda v, art=i: self._al_mover(art, v))
            d.set(90)
            d.grid(row=i, column=1, pady=4)
            d.bind("<ButtonPress-1>", lambda e, art=i: setattr(self, "arrastrando", art))
            d.bind("<ButtonRelease-1>", lambda e, art=i: self._al_soltar(art))
            etiqueta = ttk.Label(self.marco_arts, text="90°", width=5, anchor="e")
            etiqueta.grid(row=i, column=2)
            self.deslizadores.append(d)
            self.etiquetas.append(etiqueta)

        botones = ttk.Frame(marco)
        botones.grid(row=2, column=0, sticky="ew")
        for col, (texto, orden) in enumerate([("Abrir pinza", "P A"), ("Cerrar pinza", "P C"), ("Inicio", "H")]):
            ttk.Button(botones, text=texto, command=lambda o=orden: self.enlace.enviar(o)).grid(
                row=0, column=col, padx=3, sticky="ew")
            botones.columnconfigure(col, weight=1)

        self.fuente = ttk.Label(marco, text="Mando actual: —")
        self.fuente.grid(row=3, column=0, sticky="w", pady=(10, 0))

    def _listar_puertos(self, preferido=None):
        nombres = [p.device for p in serial.tools.list_ports.comports()]
        self.puertos["values"] = nombres
        if preferido:
            self.puertos.set(preferido)
        elif nombres:
            self.puertos.set(nombres[0])

    # ----- acciones ------------------------------------------------------
    def _conectar(self):
        if self.enlace.conectado:
            self.enlace.desconectar()
            self.boton_conectar.config(text="Conectar")
            self.estado.config(text="Sin conectar", foreground="#6B7280")
            return
        nombre = self.puertos.get()
        if not nombre:
            messagebox.showwarning("Puerto", "Conecta el brazo por USB y elige su puerto.")
            return
        try:
            self.enlace.conectar(nombre)
        except serial.SerialException as e:
            messagebox.showerror("Puerto", f"No se pudo abrir {nombre}:\n{e}")
            return
        self.boton_conectar.config(text="Desconectar")
        self.estado.config(text=f"Conectado a {nombre}", foreground="#047857")
        self.enlace.enviar("E")

    def _al_mover(self, art, valor):
        grados = round(float(valor))
        self.etiquetas[art].config(text=f"{grados}°")
        ahora = time.monotonic()
        if self.arrastrando == art and ahora - self.ultimo_envio >= PERIODO_ENVIO_S:
            self.ultimo_envio = ahora
            self.enlace.enviar(f"J {art} {grados}")

    def _al_soltar(self, art):
        self.arrastrando = None
        self.enlace.enviar(f"J {art} {round(self.deslizadores[art].get())}")

    def _pedir_estado(self):
        if self.enlace.conectado and self.arrastrando is None:
            self.enlace.enviar("E")
        self.after(PERIODO_ESTADO_MS, self._pedir_estado)

    def _procesar_respuestas(self):
        while not self.enlace.respuestas.empty():
            tipo, linea = self.enlace.respuestas.get()
            if tipo == "desconectado":
                self.enlace.desconectar()
                self.boton_conectar.config(text="Conectar")
                self.estado.config(text="Se perdió la conexión", foreground="#E00034")
            elif linea.startswith("OK {"):
                self._mostrar_estado(json.loads(linea[3:]))
            elif linea.startswith("ERR"):
                self.estado.config(text=linea, foreground="#E00034")
        self.after(50, self._procesar_respuestas)

    def _mostrar_estado(self, e):
        self.title(f"Brazo {e['brazo']} · ESP32-C3")
        self.fuente.config(text=f"Mando actual: {e['fuente']}")
        for i, a in enumerate(e["articulaciones"][:ARTICULACIONES_DESLIZABLES]):
            d = self.deslizadores[i]
            d.config(from_=a["min"], to=a["max"])
            if self.arrastrando != i:
                d.set(a["objetivo"])
                self.etiquetas[i].config(text=f"{round(a['angulo'])}°")

    def _cerrar(self):
        self.enlace.desconectar()
        self.destroy()


def main():
    parser = argparse.ArgumentParser(description="Control del brazo robótico por USB")
    parser.add_argument("--puerto", help="puerto serie, por ejemplo COM5 o /dev/ttyACM0")
    args = parser.parse_args()
    Aplicacion(args.puerto).mainloop()


if __name__ == "__main__":
    main()
