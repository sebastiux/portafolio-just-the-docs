// Visor STL para Just the Docs (three.js).
// Uso:
//   <div class="stl-viewer" data-stl="ruta/pieza.stl" data-color="#E00034"></div>
//   <div class="stl-viewer" data-assembly="ruta/ensamble.json" data-base="ruta/carpeta/"></div>
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { STLLoader } from 'three/addons/loaders/STLLoader.js';

const loader = new STLLoader();
const cache = new Map();

function loadGeometry(url) {
  if (!cache.has(url)) cache.set(url, loader.loadAsync(url));
  return cache.get(url);
}

function makeMaterial(color) {
  return new THREE.MeshStandardMaterial({ color, roughness: 0.55, metalness: 0.05 });
}

// Centra la pieza en X/Y y la apoya en Z = 0 (misma convención que la cama de impresión).
function centerOnBed(geometry) {
  geometry.computeBoundingBox();
  const bb = geometry.boundingBox;
  geometry.translate(-(bb.min.x + bb.max.x) / 2, -(bb.min.y + bb.max.y) / 2, -bb.min.z);
  geometry.computeVertexNormals();
  return geometry;
}

function createScene(container) {
  const scene = new THREE.Scene();
  scene.background = new THREE.Color('#f5f6f8');

  const camera = new THREE.PerspectiveCamera(40, 1, 0.1, 5000);
  camera.up.set(0, 0, 1);

  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  container.appendChild(renderer.domElement);

  scene.add(new THREE.HemisphereLight(0xffffff, 0x8a8f99, 1.6));
  const key = new THREE.DirectionalLight(0xffffff, 1.6);
  key.position.set(1, -1.5, 2);
  scene.add(key);
  const fill = new THREE.DirectionalLight(0xffffff, 0.6);
  fill.position.set(-1.5, 1, 0.5);
  scene.add(fill);

  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;

  const resize = () => {
    const w = container.clientWidth;
    const h = container.clientHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  };
  new ResizeObserver(resize).observe(container);
  resize();

  const loop = () => {
    controls.update();
    renderer.render(scene, camera);
    requestAnimationFrame(loop);
  };
  loop();

  return { scene, camera, controls };
}

function frame(ctx, object, grid = true) {
  const box = new THREE.Box3().setFromObject(object);
  const size = box.getSize(new THREE.Vector3());
  const center = box.getCenter(new THREE.Vector3());
  const radius = size.length() / 2 || 1;

  if (grid) {
    const extent = Math.ceil(Math.max(size.x, size.y) * 1.6 / 10) * 10 || 50;
    const g = new THREE.GridHelper(extent, extent / 5, 0xb8bec8, 0xdde1e6);
    g.rotation.x = Math.PI / 2;
    g.position.set(center.x, center.y, box.min.z - 0.01);
    g.name = 'grid';
    ctx.scene.getObjectByName('grid')?.removeFromParent();
    ctx.scene.add(g);
  }

  const dist = radius / Math.sin((ctx.camera.fov * Math.PI) / 360) * 1.05;
  ctx.camera.position.copy(center).add(new THREE.Vector3(0.9, -1.3, 0.8).normalize().multiplyScalar(dist));
  ctx.camera.near = dist / 100;
  ctx.camera.far = dist * 20;
  ctx.camera.updateProjectionMatrix();
  ctx.controls.target.copy(center);
  ctx.controls.update();
  ctx.home = { pos: ctx.camera.position.clone(), target: center.clone() };
}

function addToolbar(container, ctx, extra = []) {
  const bar = document.createElement('div');
  bar.className = 'stl-viewer__bar';
  const reset = document.createElement('button');
  reset.type = 'button';
  reset.textContent = 'Reiniciar vista';
  reset.addEventListener('click', () => {
    ctx.camera.position.copy(ctx.home.pos);
    ctx.controls.target.copy(ctx.home.target);
  });
  bar.append(...extra, reset);
  container.appendChild(bar);
}

function status(container, text) {
  let el = container.querySelector('.stl-viewer__status');
  if (!el) {
    el = document.createElement('div');
    el.className = 'stl-viewer__status';
    container.appendChild(el);
  }
  el.textContent = text;
  el.hidden = !text;
}

async function initSingle(container) {
  status(container, 'Cargando pieza…');
  const ctx = createScene(container);
  const geometry = centerOnBed(await loadGeometry(container.dataset.stl));
  const mesh = new THREE.Mesh(geometry, makeMaterial(container.dataset.color || '#E00034'));
  ctx.scene.add(mesh);
  frame(ctx, mesh);
  addToolbar(container, ctx);
  status(container, '');
}

async function initAssembly(container) {
  status(container, 'Cargando ensamble…');
  const ctx = createScene(container);
  const spec = await (await fetch(container.dataset.assembly)).json();
  const base = container.dataset.base || '';

  const group = new THREE.Group();
  const parts = await Promise.all(spec.parts.map(async (p) => {
    const geometry = centerOnBed((await loadGeometry(base + p.file)).clone());
    const mesh = new THREE.Mesh(geometry, makeMaterial(p.color));
    const [rx = 0, ry = 0, rz = 0] = p.rotation || [];
    mesh.rotation.set(THREE.MathUtils.degToRad(rx), THREE.MathUtils.degToRad(ry), THREE.MathUtils.degToRad(rz));
    const pos = new THREE.Vector3(...(p.position || [0, 0, 0]));
    const dir = new THREE.Vector3(...(p.explode || [0, 0, 0]));
    mesh.position.copy(pos);
    group.add(mesh);
    return { mesh, pos, dir, name: p.name };
  }));
  ctx.scene.add(group);

  const setExplode = (t) => parts.forEach(({ mesh, pos, dir }) => mesh.position.copy(pos).addScaledVector(dir, t));

  const label = document.createElement('label');
  label.className = 'stl-viewer__slider';
  label.textContent = 'Separar piezas ';
  const slider = document.createElement('input');
  slider.type = 'range';
  slider.min = '0';
  slider.max = '1';
  slider.step = '0.01';
  slider.value = '0';
  slider.addEventListener('input', () => setExplode(Number(slider.value)));
  label.appendChild(slider);

  // Encuadra con una separación parcial para que al separar las piezas sigan en pantalla.
  setExplode(0.8);
  frame(ctx, group);
  setExplode(0);

  const legend = document.createElement('ul');
  legend.className = 'stl-viewer__legend';
  spec.parts.forEach((p) => {
    const li = document.createElement('li');
    li.innerHTML = `<span style="background:${p.color}"></span>${p.name}`;
    legend.appendChild(li);
  });
  container.appendChild(legend);
  addToolbar(container, ctx, [label]);
  status(container, '');
}

document.querySelectorAll('.stl-viewer').forEach((el) => {
  const init = el.dataset.assembly ? initAssembly : initSingle;
  // Carga diferida: solo se crea el contexto WebGL cuando el visor entra en pantalla.
  const io = new IntersectionObserver((entries) => {
    if (!entries.some((e) => e.isIntersecting)) return;
    io.disconnect();
    init(el).catch((err) => {
      console.error(err);
      status(el, 'No se pudo cargar el modelo 3D.');
    });
  }, { rootMargin: '200px' });
  io.observe(el);
});
