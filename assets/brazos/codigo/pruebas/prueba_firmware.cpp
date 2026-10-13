// prueba_firmware.cpp — Pruebas automáticas de la lógica del firmware en la computadora.
//
// Compila los mismos archivos del firmware contra un Arduino.h simulado y
// comprueba: límites de las articulaciones, velocidad máxima, conversión a
// PWM, interruptor MODO (Manual / App), interruptor de la pinza, protocolo
// serie y secuencia de diagnóstico. No sustituye la prueba con el brazo real;
// detecta errores de lógica antes de cargar el programa.
//
// Uso:  make   (o ver el Makefile)
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

static const int NIVEL_MODO_MANUAL = (NIVEL_MODO_APP == LOW) ? HIGH : LOW;
static const int NIVEL_PINZA_CERRADA = (NIVEL_PINZA_ABIERTA == LOW) ? HIGH : LOW;

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

static bool empieza(const std::string& s, const char* p) { return s.rfind(p, 0) == 0; }

static uint32_t dutyEsperado(float grados) {
  const float us = SERVO_PULSO_MIN_US + (SERVO_PULSO_MAX_US - SERVO_PULSO_MIN_US) * grados / 180.0f;
  return static_cast<uint32_t>(us / 20000.0f * ((1u << SERVO_RESOLUCION_BITS) - 1) + 0.5f);
}

int main() {
  std::cout << "Firmware del brazo " << NOMBRE_BRAZO << "\n";

  // Arranque: MODO en Manual, pinza cerrada, BOOT suelto, pots a la mitad.
  sim::pin_digital[PIN_SW_MODO] = NIVEL_MODO_MANUAL;
  sim::pin_digital[PIN_SW_PINZA] = NIVEL_PINZA_CERRADA;
  sim::pin_digital[PIN_BOTON_DIAG] = HIGH;
  potsEnMv(POT_MV_MAX / 2, POT_MV_MAX / 2, POT_MV_MAX / 2);
  puerto_serie::iniciar();
  control::iniciar();

  std::cout << "1. Arranque\n";
  COMPROBAR(!control::modoApp(), "arranca en modo Manual con SW2 en Manual");
  COMPROBAR(articulaciones::angulo(0) == LIMITES[0].inicio, "base en su ángulo de inicio");
  COMPROBAR(articulaciones::objetivo(ART_PINZA) == PINZA_CERRADA, "SW1 en cerrar: pinza cerrada");
  COMPROBAR(sim::duty[PIN_SERVO[0]] == dutyEsperado(LIMITES[0].inicio), "PWM de la base (IO5) corresponde a su ángulo");

  std::cout << "2. Conversión a PWM\n";
  COMPROBAR(dutyEsperado(0) == 410, "0° = 500 us = duty 410 de 16383");
  COMPROBAR(dutyEsperado(180) == 1966, "180° = 2400 us = duty 1966 de 16383");

  std::cout << "3. Modo Manual con potenciómetros\n";
  potsEnMv(0, POT_MV_MAX, POT_MV_MAX / 2);
  correr(3000);
  COMPROBAR(fabsf(articulaciones::angulo(0) - LIMITES[0].minimo) < 1.0f, "RV1 al mínimo lleva la base a su límite inferior");
  COMPROBAR(fabsf(articulaciones::angulo(1) - LIMITES[1].maximo) < 1.0f, "RV2 al máximo lleva el hombro a su límite superior");
  COMPROBAR(empieza(ordenSerie("J 0 45"), "ERR modo manual"), "en Manual, una orden por USB se rechaza");
  COMPROBAR(articulaciones::objetivo(0) < 1.0f, "y la base no se mueve");

  std::cout << "4. Velocidad máxima\n";
  potsEnMv(POT_MV_MAX, POT_MV_MAX, POT_MV_MAX / 2);
  correr(PERIODO_CONTROL_MS * 5);
  const float antes = articulaciones::angulo(0);
  correr(100);
  COMPROBAR(articulaciones::angulo(0) - antes <= VELOCIDAD_MAX_GRADOS_S * 0.1f + 0.01f, "la base no avanza más de 12° en 100 ms");
  correr(3000);

  std::cout << "5. Interruptor de la pinza (Manual)\n";
  sim::pin_digital[PIN_SW_PINZA] = NIVEL_PINZA_ABIERTA;   // pulso de 20 ms: más corto que el antirrebote
  correr(20);
  sim::pin_digital[PIN_SW_PINZA] = NIVEL_PINZA_CERRADA;
  correr(100);
  COMPROBAR(articulaciones::objetivo(ART_PINZA) == PINZA_CERRADA, "un rebote de 20 ms no mueve la pinza");
  sim::pin_digital[PIN_SW_PINZA] = NIVEL_PINZA_ABIERTA;
  correr(100);
  COMPROBAR(articulaciones::objetivo(ART_PINZA) == PINZA_ABIERTA, "SW1 en abrir abre la pinza");

  std::cout << "6. Modo App por USB\n";
  sim::pin_digital[PIN_SW_MODO] = NIVEL_MODO_APP;
  correr(100);
  COMPROBAR(control::modoApp(), "SW2 en App cambia al modo App");
  const float base_antes = articulaciones::objetivo(0);
  potsEnMv(POT_MV_MAX / 3, POT_MV_MAX, POT_MV_MAX / 2);
  correr(500);
  COMPROBAR(articulaciones::objetivo(0) == base_antes, "en App, los potenciómetros no mueven el brazo");
  COMPROBAR(ordenSerie("J 0 45") == "OK\n", "J 0 45 responde OK");
  COMPROBAR(control::fuenteActual() == Fuente::SERIE, "la orden queda registrada como USB");
  correr(2000);
  COMPROBAR(fabsf(articulaciones::angulo(0) - 45) < 0.5f, "la base llega a 45°");
  ordenSerie("J hombro 999");
  COMPROBAR(articulaciones::objetivo(1) == LIMITES[1].maximo, "un ángulo fuera de rango se recorta al límite");
  COMPROBAR(empieza(ordenSerie("J 7 90"), "ERR"), "articulación inexistente responde ERR");
  COMPROBAR(empieza(ordenSerie("X"), "ERR"), "orden desconocida responde ERR");
  COMPROBAR(ordenSerie("A 10 60 70 50") == "OK\n", "A mueve las cuatro articulaciones");
  COMPROBAR(articulaciones::objetivo(2) == 70, "A fija el codo en 70°");
  ordenSerie("P C");
  COMPROBAR(articulaciones::objetivo(ART_PINZA) == PINZA_CERRADA, "P C cierra la pinza");
  ordenSerie("H");
  COMPROBAR(articulaciones::objetivo(0) == LIMITES[0].inicio, "H regresa al inicio");
  const std::string e = ordenSerie("E");
  COMPROBAR(empieza(e, "OK {\"brazo\":") && e.find("\"modo\":\"app\"") != std::string::npos, "E devuelve el estado en JSON con el modo");

  std::cout << "7. Modo App por la app web\n";
  COMPROBAR(control::mover(2, 100, Fuente::WEB) == Resultado::ACEPTADA, "una orden de la app se acepta en App");
  COMPROBAR(control::fuenteActual() == Fuente::WEB, "y queda registrada como web");

  std::cout << "8. Regreso a Manual\n";
  sim::pin_digital[PIN_SW_MODO] = NIVEL_MODO_MANUAL;
  correr(3000);
  COMPROBAR(!control::modoApp(), "SW2 en Manual regresa al modo Manual");
  COMPROBAR(fabsf(articulaciones::objetivo(0) - entradas::anguloPot(0)) < 0.5f, "la base vuelve a seguir a RV1");
  COMPROBAR(articulaciones::objetivo(ART_PINZA) == PINZA_ABIERTA, "la pinza vuelve a la posición de SW1");
  COMPROBAR(control::mover(0, 90, Fuente::WEB) == Resultado::MODO_MANUAL, "la app se rechaza en Manual");

  std::cout << "9. Diagnóstico con el botón BOOT\n";
  sim::pin_digital[PIN_BOTON_DIAG] = LOW;
  correr(60);
  sim::pin_digital[PIN_BOTON_DIAG] = HIGH;
  COMPROBAR(control::enDiagnostico(), "presionar BOOT arranca el diagnóstico");
  COMPROBAR(articulaciones::objetivo(0) == LIMITES[0].minimo, "primer paso: base a su mínimo");
  correr(DIAG_PASO_MS);
  COMPROBAR(articulaciones::objetivo(0) == LIMITES[0].maximo, "segundo paso: base a su máximo");
  COMPROBAR(empieza(ordenSerie("H"), "ERR diagnostico"), "durante el diagnóstico se rechazan órdenes");
  correr(DIAG_PASO_MS * (NUM_ARTICULACIONES * 3));
  COMPROBAR(!control::enDiagnostico(), "el diagnóstico termina solo (12 pasos)");

  std::cout << "\n" << (total - fallas) << " de " << total << " comprobaciones correctas\n";
  return fallas ? 1 : 0;
}
