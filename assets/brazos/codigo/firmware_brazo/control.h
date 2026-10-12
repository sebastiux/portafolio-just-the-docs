// control.h — Decide qué fuente mueve el brazo y aplica sus órdenes.
//
// Tres fuentes de mando:
//   MANUAL : potenciómetros e interruptor de la tarjeta (modo por defecto)
//   WEB    : app servida por el ESP32-C3 en http://192.168.4.1
//   SERIE  : brazo_gui.py en la computadora, por el USB
//
// Regla: manda la última fuente que dio una orden. Una orden de la app o del
// puerto serie toma el control; girar cualquier potenciómetro más de
// UMBRAL_TOMA_MANUAL_GRADOS lo devuelve al modo manual.
#pragma once
#include "config.h"

enum class Fuente : uint8_t { MANUAL, WEB, SERIE };

namespace control {

void iniciar();
void ciclo(float dt_s);                                   // lee entradas, arbitra y mueve servos

bool mover(uint8_t art, float grados, Fuente fuente);     // false si la articulación no existe
void pinza(bool abrir, Fuente fuente);
void inicio(Fuente fuente);

Fuente fuenteActual();
const char* nombreFuente(Fuente f);
size_t estadoJson(char* destino, size_t tam);             // estado completo en JSON

}  // namespace control
