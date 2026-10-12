// entradas.h — Lectura de los 3 potenciómetros y del interruptor de la pinza.
#pragma once
#include "config.h"

namespace entradas {

void iniciar();
void leer();                         // llamar cada ciclo: filtra el ADC y quita rebotes

float anguloPot(uint8_t pot);        // posición del potenciómetro convertida a grados de la articulación
bool  interruptorActivo();           // true = pinza abierta
bool  interruptorCambio();           // true una sola vez después de cada cambio

}  // namespace entradas
