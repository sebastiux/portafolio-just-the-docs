// servidor_web.h — Punto de acceso Wi-Fi y app de control en http://192.168.4.1
//
// Rutas:
//   GET /                         página de la app (pagina_web.h)
//   GET /api/estado               estado en JSON
//   GET /api/mover?art=N&grados=G mover una articulación
//   GET /api/pinza?accion=abrir   abrir | cerrar la pinza
//   GET /api/inicio               posición de inicio
#pragma once
#include "config.h"

namespace servidor_web {

void iniciar();
void atender();   // llamar cada ciclo

}  // namespace servidor_web
