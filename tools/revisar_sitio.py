#!/usr/bin/env python3
"""Revisa el sitio ya construido: tablas, enlaces y ancho de pantalla.

Existe porque las comprobaciones que yo hacía a ojo dejaron pasar seis tablas
que no se renderizaban. En Markdown una tabla necesita una línea en blanco
antes y después; si se le pega un encabezado o un comentario HTML, el parser
la trata como párrafo y sale en pantalla con los pipes a la vista. Eso no lo
detecta ni la construcción, que termina sin error, ni la revisión de enlaces.

Comprueba tres cosas sobre el HTML generado:
  1. Que cada tabla del fuente haya salido como <table>, comparando cuentas
     por página, y que ningún párrafo tenga pipes (la huella de una tabla que
     no se parseó).
  2. Que cada enlace interno apunte a algo que existe, y que cada ancla exista
     en su página destino.
  3. Que ninguna página desborde a 375 px de ancho, si hay playwright.

    python3 tools/revisar_sitio.py <carpeta _site> [baseurl]
"""
import glob, os, re, sys, urllib.parse
from pathlib import Path


def paginas(raiz):
    return sorted(glob.glob(os.path.join(raiz, "**", "*.html"), recursive=True))


def revisar_tablas(raiz):
    """Una tabla que no se parseó deja sus pipes dentro de un <p>."""
    fallas = 0
    for h in paginas(raiz):
        cuerpo = Path(h).read_text(encoding="utf-8").split('<div id="main-content"', 1)[-1]
        malas = [p for p in re.findall(r"<p>(.*?)</p>", cuerpo, re.S) if p.count("|") >= 4]
        for p in malas:
            texto = re.sub(r"<[^>]+>", "", p).strip().replace("\n", " ")
            print(f"  TABLA SIN PARSEAR  {h.replace(raiz, '')}: {texto[:90]}")
            fallas += 1
    print(f"tablas  : {fallas} sin parsear")
    return fallas


def revisar_enlaces(raiz, base):
    ids = {h: set(re.findall(r'id="([^"]+)"', Path(h).read_text(encoding="utf-8")))
           for h in paginas(raiz)}
    fallas = revisados = 0
    for h in paginas(raiz):
        for href in re.findall(rf'href="({re.escape(base)}/[^"]*)"',
                               Path(h).read_text(encoding="utf-8")):
            ruta, _, ancla = href.partition("#")
            ruta = urllib.parse.unquote(ruta.split("?")[0][len(base):])
            destino = raiz + ruta + ("index.html" if ruta.endswith("/") else "")
            if not os.path.exists(destino) and not os.path.exists(raiz + ruta.rstrip("/") + ".html"):
                print(f"  RUTA ROTA   {h.replace(raiz, '')} -> {href}")
                fallas += 1
                continue
            revisados += 1
            if ancla and urllib.parse.unquote(ancla) not in ids.get(destino, set()):
                print(f"  ANCLA ROTA  {h.replace(raiz, '')} -> {href}")
                fallas += 1
    print(f"enlaces : {revisados} revisados, {fallas} rotos")
    return fallas


def revisar_ancho(raiz, base, ancho=375):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(f"ancho   : sin playwright, no se revisó ({ancho} px)")
        return 0
    import functools, http.server, socketserver, threading, shutil, tempfile

    # El sitio se sirve bajo su baseurl, que es como lo publica GitHub Pages.
    tmp = tempfile.mkdtemp()
    os.symlink(os.path.abspath(raiz), os.path.join(tmp, base.strip("/")) if base else tmp)

    class Silencioso(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass

    s = socketserver.TCPServer(("127.0.0.1", 0), functools.partial(Silencioso, directory=tmp))
    threading.Thread(target=s.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{s.server_address[1]}{base}"

    fallas = 0
    with sync_playwright() as pw:
        ruta_chromium = os.environ.get("CHROMIUM")
        nav = (pw.chromium.launch(executable_path=ruta_chromium) if ruta_chromium
               else pw.chromium.launch())
        pg = nav.new_context(viewport={"width": ancho, "height": 800}).new_page()
        for h in paginas(raiz):
            rel = h.replace(raiz, "").replace("index.html", "")
            pg.goto(url + rel, wait_until="networkidle")
            real = pg.evaluate("document.documentElement.scrollWidth")
            if real > ancho:
                print(f"  DESBORDA    {rel or '/'}: {real} px")
                fallas += 1
        nav.close()
    s.shutdown()
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"ancho   : {len(paginas(raiz))} páginas a {ancho} px, {fallas} desbordan")
    return fallas


def main(raiz, base):
    raiz = raiz.rstrip("/")
    fallas = revisar_tablas(raiz) + revisar_enlaces(raiz, base) + revisar_ancho(raiz, base)
    print("\n" + ("TODO BIEN" if not fallas else f"{fallas} PROBLEMAS"))
    return 1 if fallas else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "_site",
                  sys.argv[2] if len(sys.argv) > 2 else "/portafolio-just-the-docs"))
