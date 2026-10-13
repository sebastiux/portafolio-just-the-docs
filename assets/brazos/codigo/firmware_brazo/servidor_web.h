// servidor_web.h — Punto de acceso Wi-Fi y app de control en http://192.168.4.1
//
// Rutas (las de movimiento responden 409 si el interruptor MODO está en Manual):
//   GET /                         página de la app (pagina_web.h)
//   GET /api/estado               estado en JSON
//   GET /api/mover?art=N&grados=G mover una articulación
//   GET /api/pinza?accion=abrir   abrir | cerrar la pinza
//   GET /api/inicio               posición de inicio
//   GET /api/diagnostico          secuencia de diagnóstico
#pragma once
#include "config.h"

namespace servidor_web {

void iniciar();
void atender();   // llamar cada ciclo
bool activo();    // false si no se pudo crear la red Wi-Fi

}  // namespace servidor_web
