// puerto_serie.h — Protocolo de texto por el USB para brazo_gui.py.
//
// Una orden por línea, terminada en '\n'. Respuestas "OK ..." o "ERR ...".
// Las órdenes de movimiento solo se aceptan con el interruptor MODO en App.
//   J <art> <grados>      mover una articulación (art = 0..3 o base/hombro/codo/pinza)
//   A <b> <h> <c> <p>     mover las cuatro articulaciones
//   P A | P C             abrir | cerrar la pinza
//   H                     posición de inicio
//   D                     secuencia de diagnóstico (igual que el botón BOOT)
//   E                     estado en JSON
//   ?                     ayuda
#pragma once
#include "config.h"

namespace puerto_serie {

void iniciar();
void atender();   // leer y ejecutar las órdenes pendientes; llamar cada ciclo

}  // namespace puerto_serie
