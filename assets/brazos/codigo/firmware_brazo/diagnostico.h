// diagnostico.h — LEDs de estado y reporte de diagnóstico por USB.
//
// D2 ESTADO (verde) dice en qué modo está el brazo y si hay un celular
// conectado. D3 DIAG (rojo) avisa de un reinicio por brown-out: es lo que pasa
// cuando los cuatro servos arrancan a la vez y hunden los 5 V. El botón DIAG
// imprime el reporte por el puerto serie y apaga D3.
//
// El número de celulares conectados lo sabe el servidor web, así que entra como
// parámetro: así este módulo se puede probar con g++ sin levantar el Wi-Fi.
#pragma once
#include "config.h"

namespace diagnostico {

void iniciar();                     // guarda la causa del reinicio y enciende D3 si fue brown-out
void ciclo(uint8_t clientes);       // LEDs y botón DIAG; llamar cada ciclo de control
void reporte(uint8_t clientes);     // imprime el reporte por USB y apaga D3

bool alerta();                      // true mientras D3 sigue avisando del brown-out
const char* causaReinicio();        // texto corto de la causa del último reinicio

}  // namespace diagnostico
