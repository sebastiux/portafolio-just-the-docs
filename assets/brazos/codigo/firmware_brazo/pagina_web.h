// pagina_web.h — App de control que sirve el ESP32-C3. Se guarda en flash (PROGMEM).
#pragma once
#include <Arduino.h>

const char PAGINA_WEB[] PROGMEM = R"HTML(<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Brazo robótico</title>
<style>
  :root { --rojo: #E00034; --gris: #4B5563; }
  * { box-sizing: border-box; }
  body { margin: 0; font-family: system-ui, sans-serif; background: #f5f6f8; color: #222; }
  header { background: var(--rojo); color: #fff; padding: 14px 16px; }
  header h1 { margin: 0; font-size: 1.2rem; }
  header p { margin: 4px 0 0; font-size: .85rem; opacity: .9; }
  main { max-width: 520px; margin: 0 auto; padding: 16px; }
  .tarjeta { background: #fff; border-radius: 12px; padding: 14px 16px; margin-bottom: 12px;
             box-shadow: 0 1px 3px rgba(0,0,0,.08); }
  .fila { display: flex; justify-content: space-between; align-items: baseline; }
  .fila b { font-size: 1rem; text-transform: capitalize; }
  .valor { font-variant-numeric: tabular-nums; color: var(--gris); }
  input[type=range] { width: 100%; accent-color: var(--rojo); height: 32px; }
  .botones { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; }
  button { font: inherit; padding: 12px 8px; border-radius: 10px; border: 1px solid #d1d5db;
           background: #fff; cursor: pointer; }
  button.primario { background: var(--rojo); color: #fff; border-color: var(--rojo); }
  .fuente { display: inline-block; padding: 2px 8px; border-radius: 999px; background: #fff;
            color: var(--rojo); font-weight: 600; font-size: .8rem; }
  .error { color: var(--rojo); font-size: .85rem; min-height: 1.2em; }
</style>
</head>
<body>
<header>
  <h1>Brazo <span id="brazo">…</span></h1>
  <p>Mando actual: <span class="fuente" id="fuente">…</span></p>
</header>
<main>
  <div id="articulaciones"></div>
  <div class="tarjeta">
    <div class="botones">
      <button class="primario" id="abrir">Abrir pinza</button>
      <button class="primario" id="cerrar">Cerrar pinza</button>
      <button id="inicio">Inicio</button>
    </div>
  </div>
  <p class="error" id="error"></p>
</main>
<script>
const NOMBRES_DESLIZABLES = 3;          // base, hombro y codo; la pinza va con botones
const contenedor = document.getElementById('articulaciones');
let arrastrando = -1, ultimoEnvio = 0, pendiente = null;

function crearDeslizables(arts) {
  contenedor.innerHTML = '';
  arts.slice(0, NOMBRES_DESLIZABLES).forEach((a, i) => {
    const t = document.createElement('div');
    t.className = 'tarjeta';
    t.innerHTML = `<div class="fila"><b>${a.nombre}</b><span class="valor" id="v${i}"></span></div>
      <input type="range" id="r${i}" min="${a.min}" max="${a.max}" step="1">`;
    contenedor.appendChild(t);
    const r = t.querySelector('input');
    r.addEventListener('pointerdown', () => arrastrando = i);
    r.addEventListener('pointerup', () => { arrastrando = -1; enviar(i, r.value, true); });
    r.addEventListener('input', () => { document.getElementById('v' + i).textContent = r.value + '°'; enviar(i, r.value); });
  });
}

// Limita los envíos a uno cada 80 ms mientras se arrastra.
function enviar(art, grados, forzar) {
  const ahora = Date.now();
  if (!forzar && ahora - ultimoEnvio < 80) {
    clearTimeout(pendiente);
    pendiente = setTimeout(() => enviar(art, grados, true), 80);
    return;
  }
  ultimoEnvio = ahora;
  pedir(`/api/mover?art=${art}&grados=${grados}`);
}

async function pedir(url) {
  try {
    const r = await fetch(url);
    if (!r.ok) throw new Error(await r.text());
    mostrar(await r.json());
    document.getElementById('error').textContent = '';
  } catch (e) {
    document.getElementById('error').textContent = 'Sin conexión con el brazo: ' + e.message;
  }
}

function mostrar(e) {
  document.getElementById('brazo').textContent = e.brazo;
  document.getElementById('fuente').textContent = e.fuente;
  if (!contenedor.children.length) crearDeslizables(e.articulaciones);
  e.articulaciones.slice(0, NOMBRES_DESLIZABLES).forEach((a, i) => {
    if (i === arrastrando) return;
    document.getElementById('r' + i).value = Math.round(a.objetivo);
    document.getElementById('v' + i).textContent = Math.round(a.angulo) + '°';
  });
}

document.getElementById('abrir').onclick  = () => pedir('/api/pinza?accion=abrir');
document.getElementById('cerrar').onclick = () => pedir('/api/pinza?accion=cerrar');
document.getElementById('inicio').onclick = () => pedir('/api/inicio');
pedir('/api/estado');
setInterval(() => { if (arrastrando < 0) pedir('/api/estado'); }, 500);
</script>
</body>
</html>)HTML";
