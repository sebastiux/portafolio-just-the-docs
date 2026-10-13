#!/usr/bin/env python3
"""F5 — Capturas de la app web del brazo, servida en la computadora.

La app vive dentro del firmware (`pagina_web.h`) y hasta aquí no la había
ejecutado nada: las pruebas de g++ no compilan ni esa cabecera ni el servidor
web. Este script saca el HTML del archivo, lo sirve con un remedo del
`/api/estado` del firmware y lo fotografía en pantalla de celular.

Sirve para dos cosas:
  - comprobar que la app corre, que pinta los deslizables con los límites que
    le llegan y que el aviso de modo manual aparece y desaparece;
  - tener una figura para la página mientras no llegue la captura del celular
    real. **La figura dice que el estado es simulado**: no se puede presentar
    como una foto del brazo funcionando.

Lo que NO prueba: nada del lado del ESP32-C3. Las rutas de aquí son un remedo
en Python, no `servidor_web.cpp`.

Necesita playwright (`pip install playwright`) y un Chromium. Si la versión de
playwright no coincide con la del navegador instalado, se le pasa la ruta del
ejecutable en la variable CHROMIUM, p. ej.
CHROMIUM=/opt/pw-browsers/chromium-1194/chrome-linux/chrome

    python3 tools/f5_captura_app.py [carpeta de salida]
"""
import http.server, json, os, re, socketserver, sys, threading

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGINA_H = os.path.join(RAIZ, "assets/brazos/codigo/firmware_brazo/pagina_web.h")

# Estado inventado, con los límites del brazo impreso de config.h.
ARTICULACIONES = [
    {"nombre": "base",   "angulo": 90.0,  "objetivo": 90.0,  "min": 0,  "max": 180},
    {"nombre": "hombro", "angulo": 112.0, "objetivo": 115.0, "min": 30, "max": 150},
    {"nombre": "codo",   "angulo": 64.0,  "objetivo": 64.0,  "min": 20, "max": 160},
    {"nombre": "pinza",  "angulo": 100.0, "objetivo": 100.0, "min": 30, "max": 100},
]


def html_del_firmware():
    txt = open(PAGINA_H, encoding="utf-8").read()
    m = re.search(r'R"HTML\((.*)\)HTML"', txt, re.S)
    if not m:
        sys.exit("no se encontró el bloque R\"HTML(...)HTML\" en pagina_web.h")
    return m.group(1)


def servidor(modo, pagina):
    class Rutas(http.server.BaseHTTPRequestHandler):
        def log_message(self, *_):      # sin ruido en la terminal
            pass

        def responder(self, codigo, tipo, cuerpo):
            datos = cuerpo.encode("utf-8")
            self.send_response(codigo)
            self.send_header("Content-Type", tipo)
            self.send_header("Content-Length", str(len(datos)))
            self.end_headers()
            self.wfile.write(datos)

        def do_GET(self):
            ruta = self.path.split("?")[0]
            if ruta == "/":
                return self.responder(200, "text/html; charset=utf-8", pagina)
            if ruta == "/api/estado":
                return self.responder(200, "application/json", json.dumps({
                    "brazo": "impreso", "modo": modo,
                    "clientes": 1 if modo == "app" else 0,
                    "diag": False, "articulaciones": ARTICULACIONES,
                    "pinza_abierta": 100, "pinza_cerrada": 30,
                }))
            if ruta == "/favicon.ico":
                # El firmware no sirve icono; se responde vacío para que el 404
                # no ensucie la lista de errores que revisa esta prueba.
                return self.responder(204, "image/x-icon", "")
            if ruta.startswith("/api/"):
                if modo == "manual":    # igual que control::codigoHttp
                    return self.responder(409, "application/json", '{"error":"modo manual"}')
                return self.do_GET_estado()
            self.responder(404, "text/plain", "no encontrado")

        def do_GET_estado(self):
            self.path = "/api/estado"
            return self.do_GET()

    s = socketserver.TCPServer(("127.0.0.1", 0), Rutas)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s


def main(salida):
    from playwright.sync_api import sync_playwright

    os.makedirs(salida, exist_ok=True)
    pagina = html_del_firmware()
    print(f"HTML sacado de pagina_web.h: {len(pagina)} caracteres")

    with sync_playwright() as pw:
        ruta = os.environ.get("CHROMIUM")
        navegador = pw.chromium.launch(executable_path=ruta) if ruta else pw.chromium.launch()
        for modo, nombre in (("app", "app-modo-app.png"), ("manual", "app-modo-manual.png")):
            s = servidor(modo, pagina)
            url = f"http://127.0.0.1:{s.server_address[1]}/"
            ctx = navegador.new_context(viewport={"width": 390, "height": 760},
                                        device_scale_factor=2)
            pg = ctx.new_page()
            errores = []
            pg.on("pageerror", lambda e: errores.append(str(e)))
            pg.on("console", lambda m: errores.append(m.text) if m.type == "error" else None)
            pg.goto(url)
            pg.wait_for_selector("#articulaciones .tarjeta")
            pg.wait_for_timeout(600)

            texto_modo = pg.inner_text("#modo")
            aviso = pg.is_visible("#aviso")
            inerte = "inerte" in (pg.get_attribute("#controles", "class") or "")
            destino = os.path.join(salida, nombre)
            pg.screenshot(path=destino, full_page=True)
            print(f"  {destino}")
            print(f"     modo que muestra: '{texto_modo}' | aviso visible: {aviso} | "
                  f"controles apagados: {inerte} | errores de JS: {errores or 'ninguno'}")
            ctx.close()
            s.shutdown()
        navegador.close()


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "assets/brazos/electronica/v3")
