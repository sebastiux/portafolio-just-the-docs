// entradas.h — Potenciómetros, interruptores SW1 y SW2, y botón BOOT (DIAG).
#pragma once
#include "config.h"

namespace entradas {

void iniciar();
void leer();                         // llamar cada ciclo: filtra el ADC y quita rebotes

float anguloPot(uint8_t pot);        // posición del potenciómetro convertida a grados de su articulación
bool  pinzaAbierta();                // SW1 en la posición de abrir
bool  pinzaCambio();                 // true una sola vez después de cada cambio de SW1
bool  modoApp();                     // SW2 en la posición App
bool  botonDiagPresionado();         // true una sola vez por cada pulsación de BOOT

}  // namespace entradas
