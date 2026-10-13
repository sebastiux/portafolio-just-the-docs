// puerto_serie.h — Consola de diagnóstico por el USB nativo del ESP32-C3.
//
// Solo lectura: el control por USB se retiró, el mando lo decide el switch SW2.
// Una orden por línea, terminada en '\n'.
//   E   estado en JSON
//   D   reporte de diagnóstico, igual que el botón DIAG
//   ?   ayuda
// Las órdenes de movimiento del protocolo viejo (J, A, P, H) responden ERR.
#pragma once
#include "config.h"

namespace puerto_serie {

void iniciar();
void atender(uint8_t clientes);   // leer y ejecutar las órdenes pendientes; llamar cada ciclo

}  // namespace puerto_serie
