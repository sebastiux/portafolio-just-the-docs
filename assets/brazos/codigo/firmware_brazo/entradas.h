// entradas.h — Lectura de los 3 potenciómetros, los 2 switches y el botón DIAG.
//
// SW1 abre y cierra la pinza. SW2 elige el modo: manual o app. Los dos son
// switches deslizables, así que basta con su estado antirrebotado; quien manda
// (control.cpp) lo aplica en cada ciclo y no necesita detectar el cambio.
//
// El botón DIAG es el BOOT del propio módulo y solo se atiende después del
// arranque, porque presionado al encender mete al ESP32-C3 en modo de descarga.
#pragma once
#include "config.h"

namespace entradas {

void iniciar();
void leer();                         // llamar cada ciclo: filtra el ADC y quita rebotes

float    anguloPot(uint8_t pot);     // posición del potenciómetro en grados de la articulación
uint16_t milivoltsPot(uint8_t pot);  // lectura filtrada en mV, para el diagnóstico

bool modoApp();                      // SW2: true = app, false = manual
bool pinzaAbierta();                 // SW1

bool botonDiagPresionado();          // estado antirrebotado del botón DIAG
bool botonDiagPulsacion();           // true una sola vez por pulsación

}  // namespace entradas
