// servidor_web.h — Punto de acceso Wi-Fi y app de control en http://192.168.4.1
//
// El punto de acceso no se apaga nunca, ni en modo manual: así el celular no
// pierde la conexión al mover el switch SW2.
//
// Rutas:
//   GET /                         página de la app (pagina_web.h)
//   GET /api/estado               estado en JSON
//   GET /api/mover?art=N&grados=G mover una articulación
//   GET /api/pinza?accion=abrir   abrir | cerrar la pinza
//   GET /api/inicio               posición de inicio
//
// Las tres últimas responden 409 {"error":"modo manual"} si SW2 está en manual.
#pragma once
#include "config.h"

namespace servidor_web {

void iniciar();
void atender();            // llamar cada ciclo
uint8_t clientes();        // celulares conectados al punto de acceso

}  // namespace servidor_web
