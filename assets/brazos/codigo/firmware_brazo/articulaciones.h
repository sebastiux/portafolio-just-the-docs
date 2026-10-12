// articulaciones.h — Manejo de los 4 servos con el periférico LEDC del ESP32-C3.
//
// Cada articulación tiene un ángulo objetivo y un ángulo actual. En cada ciclo
// el ángulo actual avanza hacia el objetivo a una velocidad máxima, para que
// los servos no arranquen todos de golpe (eso provoca picos de corriente).
#pragma once
#include "config.h"

namespace articulaciones {

void iniciar();                                  // configura el PWM y va a la posición de inicio
void fijarObjetivo(uint8_t art, float grados);   // limita el valor al rango de la articulación
void irAInicio();                                // todas las articulaciones a su ángulo de inicio
void actualizar(float dt_s);                     // avanza hacia los objetivos; llamar cada ciclo

float angulo(uint8_t art);                       // ángulo que se está enviando al servo
float objetivo(uint8_t art);                     // ángulo al que se quiere llegar
float limitar(uint8_t art, float grados);        // recorta al rango [mínimo, máximo]

}  // namespace articulaciones
