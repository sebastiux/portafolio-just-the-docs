// prueba_firmware.cpp — Pruebas automáticas de la lógica del firmware en la computadora.
//
// Compila los mismos archivos del firmware contra un Arduino.h simulado y
// comprueba: límites de las articulaciones, velocidad máxima, conversión a
// PWM, arbitraje entre fuentes de mando, interruptor de la pinza y protocolo
// serie. No sustituye la prueba con el brazo real; detecta errores de lógica
// antes de cargar el programa.
//
// Uso:  make   (o ver el Makefile)
#include <cassert>
#include <iostream>
#include "Arduino.h"
#include "../firmware_brazo/config.h"
#include "../firmware_brazo/articulaciones.h"
#include "../firmware_brazo/control.h"
#include "../firmware_brazo/entradas.h"
#include "../firmware_brazo/puerto_serie.h"

static int fallas = 0, total = 0;
#define COMPROBAR(cond, msg)                                              \
  do {                                                                    \
    total++;                                                              \
    if (!(cond)) { fallas++; std::cout << "  FALLA: " << msg << "\n"; }   \
    else         { std::cout << "  ok   : " << msg << "\n"; }             \
  } while (0)

// Avanza el tiempo simulado ejecutando ciclos de control de 20 ms.
static void correr(uint32_t ms) {
  for (uint32_t t = 0; t < ms; t += PERIODO_CONTROL_MS) {
    sim::tiempo_ms += PERIODO_CONTROL_MS;
    puerto_serie::atender();
    control::ciclo(PERIODO_CONTROL_MS / 1000.0f);
  }
}

static void potsEnMv(uint32_t b, uint32_t h, uint32_t c) {
  sim::mv_adc[PIN_POT[0]] = b; sim::mv_adc[PIN_POT[1]] = h; sim::mv_adc[PIN_POT[2]] = c;
}

static std::string ordenSerie(const std::string& o) {
  sim::salida_serie.clear();
  sim::entrada_serie += o + "\n";
  correr(PERIODO_CONTROL_MS);
  return sim::salida_serie;
}

static uint32_t dutyEsperado(float grados) {
  const float us = SERVO_PULSO_MIN_US + (SERVO_PULSO_MAX_US - SERVO_PULSO_MIN_US) * grados / 180.0f;
  return static_cast<uint32_t>(us / 20000.0f * ((1u << SERVO_RESOLUCION_BITS) - 1) + 0.5f);
}

int main() {
  std::cout << "Firmware del brazo " << NOMBRE_BRAZO << "\n";

  // Arranque: pots a la mitad del recorrido, interruptor abierto (pull-up = HIGH).
  sim::pin_digital[PIN_INTERRUPTOR] = HIGH;
  potsEnMv(POT_MV_MAX / 2, POT_MV_MAX / 2, POT_MV_MAX / 2);
  puerto_serie::iniciar();
  control::iniciar();

  std::cout << "1. Arranque\n";
  COMPROBAR(control::fuenteActual() == Fuente::MANUAL, "arranca en modo manual");
  COMPROBAR(articulaciones::angulo(0) == LIMITES[0].inicio, "base en su ángulo de inicio");
  COMPROBAR(articulaciones::objetivo(ART_PINZA) == PINZA_CERRADA, "interruptor suelto: pinza cerrada");
  COMPROBAR(sim::duty[PIN_SERVO[0]] == dutyEsperado(LIMITES[0].inicio), "PWM de la base corresponde a su ángulo");

  std::cout << "2. Conversión a PWM\n";
  COMPROBAR(dutyEsperado(0) == 410, "0° = 500 us = duty 410 de 16383");
  COMPROBAR(dutyEsperado(180) == 1966, "180° = 2400 us = duty 1966 de 16383");

  std::cout << "3. Modo manual con potenciómetros\n";
  potsEnMv(0, POT_MV_MAX, POT_MV_MAX / 2);
  correr(3000);
  COMPROBAR(fabsf(articulaciones::angulo(0) - LIMITES[0].minimo) < 1.0f, "pot de la base al mínimo lleva la base a su límite inferior");
  COMPROBAR(fabsf(articulaciones::angulo(1) - LIMITES[1].maximo) < 1.0f, "pot del hombro al máximo lleva el hombro a su límite superior");

  std::cout << "4. Velocidad máxima\n";
  potsEnMv(POT_MV_MAX, POT_MV_MAX, POT_MV_MAX / 2);
  correr(PERIODO_CONTROL_MS * 5);   // dejar asentar el filtro un poco
  const float antes = articulaciones::angulo(0);
  correr(100);
  const float avance = articulaciones::angulo(0) - antes;
  COMPROBAR(avance <= VELOCIDAD_MAX_GRADOS_S * 0.1f + 0.01f, "la base no avanza más de 12° en 100 ms");
  correr(3000);

  std::cout << "5. Mando por USB\n";
  std::string r = ordenSerie("J 0 45");
  COMPROBAR(r == "OK\n", "J 0 45 responde OK");
  COMPROBAR(control::fuenteActual() == Fuente::SERIE, "una orden por USB toma el control");
  correr(2000);
  COMPROBAR(fabsf(articulaciones::angulo(0) - 45) < 0.5f, "la base llega a 45° aunque el pot diga otra cosa");
  r = ordenSerie("J hombro 999");
  correr(2000);
  COMPROBAR(articulaciones::objetivo(1) == LIMITES[1].maximo, "un ángulo fuera de rango se recorta al límite");
  COMPROBAR(ordenSerie("J 7 90").rfind("ERR", 0) == 0, "articulación inexistente responde ERR");
  COMPROBAR(ordenSerie("X").rfind("ERR", 0) == 0, "orden desconocida responde ERR");
  COMPROBAR(ordenSerie("A 10 60 70 50") == "OK\n", "A mueve las cuatro articulaciones");
  COMPROBAR(articulaciones::objetivo(2) == 70, "A fija el codo en 70°");
  ordenSerie("P A");
  COMPROBAR(articulaciones::objetivo(ART_PINZA) == PINZA_ABIERTA, "P A abre la pinza");
  ordenSerie("H");
  COMPROBAR(articulaciones::objetivo(0) == LIMITES[0].inicio, "H regresa al inicio");
  r = ordenSerie("E");
  COMPROBAR(r.rfind("OK {\"brazo\":", 0) == 0 && r.find("\"fuente\":\"serie\"") != std::string::npos, "E devuelve el estado en JSON");

  std::cout << "6. Regreso al modo manual\n";
  potsEnMv(POT_MV_MAX, POT_MV_MAX, POT_MV_MAX / 2 + 20);   // ruido pequeño en un pot
  correr(500);
  COMPROBAR(control::fuenteActual() == Fuente::SERIE, "el ruido del pot no quita el control al USB");
  potsEnMv(POT_MV_MAX / 3, POT_MV_MAX, POT_MV_MAX / 2);    // giro claro de la base
  correr(500);
  COMPROBAR(control::fuenteActual() == Fuente::MANUAL, "girar un pot devuelve el control al modo manual");

  std::cout << "7. Mando web\n";
  control::mover(2, 100, Fuente::WEB);
  COMPROBAR(control::fuenteActual() == Fuente::WEB, "una orden de la app toma el control");

  std::cout << "8. Interruptor de la pinza\n";
  control::pinza(false, Fuente::WEB);          // parte de pinza cerrada
  sim::pin_digital[PIN_INTERRUPTOR] = LOW;     // pulso de 20 ms: más corto que el antirrebote
  correr(20);
  sim::pin_digital[PIN_INTERRUPTOR] = HIGH;
  correr(100);
  COMPROBAR(articulaciones::objetivo(ART_PINZA) == PINZA_CERRADA, "un rebote de 20 ms no mueve la pinza");
  sim::pin_digital[PIN_INTERRUPTOR] = LOW;     // se cierra a GND y se queda
  correr(100);
  COMPROBAR(articulaciones::objetivo(ART_PINZA) == PINZA_ABIERTA, "interruptor activado abre la pinza");
  sim::pin_digital[PIN_INTERRUPTOR] = HIGH;
  correr(100);
  COMPROBAR(articulaciones::objetivo(ART_PINZA) == PINZA_CERRADA, "interruptor suelto cierra la pinza");

  std::cout << "\n" << (total - fallas) << " de " << total << " comprobaciones correctas\n";
  return fallas ? 1 : 0;
}
