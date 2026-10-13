// prueba_firmware.cpp — Pruebas automáticas de la lógica del firmware en la computadora.
//
// Compila los mismos archivos del firmware contra un Arduino.h simulado y
// comprueba: mapa de pines contra el esquemático, conversión a PWM, límites de
// las articulaciones, velocidad máxima, los dos modos que decide el switch SW2,
// el antirrebote, los LEDs de estado y la consola de diagnóstico por USB.
//
// No sustituye la prueba con el brazo real; detecta errores de lógica antes de
// cargar el programa.
//
// Uso:  make   (o ver el Makefile)
#include <cassert>
#include <iostream>
#include "Arduino.h"
#include "../firmware_brazo/config.h"
#include "../firmware_brazo/articulaciones.h"
#include "../firmware_brazo/control.h"
#include "../firmware_brazo/diagnostico.h"
#include "../firmware_brazo/entradas.h"
#include "../firmware_brazo/puerto_serie.h"

static int fallas = 0, total = 0;
#define COMPROBAR(cond, msg)                                              \
  do {                                                                    \
    total++;                                                              \
    if (!(cond)) { fallas++; std::cout << "  FALLA: " << msg << "\n"; }   \
    else         { std::cout << "  ok   : " << msg << "\n"; }             \
  } while (0)

static uint8_t clientes_ = 0;    // celulares conectados al punto de acceso

// Avanza el tiempo simulado ejecutando ciclos de control de 20 ms.
static void correr(uint32_t ms) {
  for (uint32_t t = 0; t < ms; t += PERIODO_CONTROL_MS) {
    sim::tiempo_ms += PERIODO_CONTROL_MS;
    puerto_serie::atender(clientes_);
    control::ciclo(PERIODO_CONTROL_MS / 1000.0f);
    diagnostico::ciclo(clientes_);
  }
}

static void potsEnMv(uint32_t b, uint32_t h, uint32_t c) {
  sim::mv_adc[PIN_POT[0]] = b; sim::mv_adc[PIN_POT[1]] = h; sim::mv_adc[PIN_POT[2]] = c;
}

// Posición de los switches, traducida a nivel eléctrico por las dos constantes
// de polaridad de config.h.
static void ponerModo(bool app) {
  sim::pin_digital[PIN_SW_MODO] = (app == MODO_APP_EN_BAJO) ? LOW : HIGH;
}
static void ponerSwPinza(bool abierta) {
  sim::pin_digital[PIN_SW_PINZA] = (abierta == PINZA_ABIERTA_EN_BAJO) ? LOW : HIGH;
}
static void ponerBotonDiag(bool presionado) {
  sim::pin_digital[PIN_BOTON_DIAG] = presionado ? LOW : HIGH;
}

static std::string ordenSerie(const std::string& o) {
  sim::salida_serie.clear();
  sim::entrada_serie += o + "\n";
  correr(PERIODO_CONTROL_MS);
  return sim::salida_serie;
}

static bool contiene(const std::string& donde, const std::string& que) {
  return donde.find(que) != std::string::npos;
}

static uint32_t dutyEsperado(float grados) {
  const float us = SERVO_PULSO_MIN_US + (SERVO_PULSO_MAX_US - SERVO_PULSO_MIN_US) * grados / 180.0f;
  return static_cast<uint32_t>(us / 20000.0f * ((1u << SERVO_RESOLUCION_BITS) - 1) + 0.5f);
}

static bool ledEncendido(uint8_t pin) { return sim::pin_digital[pin] == LOW; }

int main() {
  std::cout << "Firmware del brazo " << NOMBRE_BRAZO << "\n";

  std::cout << "1. Mapa de pines (contra el esquematico de la tarjeta v3)\n";
  COMPROBAR(PIN_SERVO[0] == 5 && PIN_SERVO[1] == 6 && PIN_SERVO[2] == 7 && PIN_SERVO[3] == 10,
            "servos en GPIO 5, 6, 7 y 10 (J3 a J6)");
  COMPROBAR(PIN_POT[0] == 1 && PIN_POT[1] == 0 && PIN_POT[2] == 3,
            "pots RV1, RV2 y RV3 en GPIO 1, 0 y 3");
  COMPROBAR(PIN_SW_PINZA == 21 && PIN_SW_MODO == 20, "SW1 en GPIO21 y SW2 en GPIO20");
  COMPROBAR(PIN_LED_ESTADO == 4 && PIN_LED_DIAG == 2, "D2 en GPIO4 y D3 en GPIO2");
  COMPROBAR(PIN_BOTON_DIAG == 9, "boton DIAG en GPIO9, el BOOT del modulo");

  std::cout << "2. Conversion a PWM\n";
  COMPROBAR(dutyEsperado(0) == 410, "0 grados = 500 us = duty 410 de 16383");
  COMPROBAR(dutyEsperado(180) == 1966, "180 grados = 2400 us = duty 1966 de 16383");

  // Arranque en manual, pots a la mitad del recorrido y pinza cerrada.
  sim::razon_reinicio = ESP_RST_POWERON;
  ponerModo(false);
  ponerSwPinza(false);
  ponerBotonDiag(false);
  potsEnMv(POT_MV_MAX / 2, POT_MV_MAX / 2, POT_MV_MAX / 2);
  puerto_serie::iniciar();
  diagnostico::iniciar();
  control::iniciar();

  std::cout << "3. Arranque\n";
  COMPROBAR(control::modo() == Modo::MANUAL, "con SW2 en manual arranca en modo manual");
  COMPROBAR(articulaciones::angulo(0) == LIMITES[0].inicio, "la base parte de su angulo de inicio");
  COMPROBAR(articulaciones::objetivo(ART_PINZA) == PINZA_CERRADA, "SW1 en cerrado: pinza cerrada");
  COMPROBAR(sim::duty[PIN_SERVO[0]] == dutyEsperado(LIMITES[0].inicio),
            "el PWM de la base corresponde a su angulo");
  COMPROBAR(!diagnostico::alerta(), "sin brown-out el LED D3 no avisa");

  std::cout << "4. Modo manual: mandan los potenciometros\n";
  potsEnMv(0, POT_MV_MAX, POT_MV_MAX / 2);
  correr(3000);
  COMPROBAR(fabsf(articulaciones::angulo(0) - LIMITES[0].minimo) < 1.0f,
            "pot de la base al minimo lleva la base a su limite inferior");
  COMPROBAR(fabsf(articulaciones::angulo(1) - LIMITES[1].maximo) < 1.0f,
            "pot del hombro al maximo lleva el hombro a su limite superior");
  COMPROBAR(control::mover(0, 123) == Resultado::MODO_MANUAL,
            "una orden de la app en modo manual se rechaza");
  COMPROBAR(control::codigoHttp(Resultado::MODO_MANUAL) == 409, "ese rechazo es un HTTP 409");
  COMPROBAR(contiene(control::cuerpoJson(Resultado::MODO_MANUAL), "modo manual"),
            "el 409 lleva {\"error\":\"modo manual\"}");
  COMPROBAR(control::pinza(true) == Resultado::MODO_MANUAL && control::inicio() == Resultado::MODO_MANUAL,
            "pinza e inicio tambien se rechazan en manual");
  correr(500);
  COMPROBAR(fabsf(articulaciones::objetivo(0) - LIMITES[0].minimo) < 1.0f,
            "la orden rechazada no movio el objetivo de la base");

  std::cout << "5. Velocidad maxima\n";
  potsEnMv(POT_MV_MAX, POT_MV_MAX, POT_MV_MAX / 2);
  correr(PERIODO_CONTROL_MS * 5);   // dejar asentar el filtro un poco
  const float antes_vel = articulaciones::angulo(0);
  correr(100);
  COMPROBAR(articulaciones::angulo(0) - antes_vel <= VELOCIDAD_MAX_GRADOS_S * 0.1f + 0.01f,
            "la base no avanza mas de 12 grados en 100 ms");
  correr(3000);

  std::cout << "6. Antirrebote de SW1\n";
  ponerSwPinza(true);
  correr(20);                       // pulso mas corto que los 30 ms del antirrebote
  ponerSwPinza(false);
  correr(100);
  COMPROBAR(articulaciones::objetivo(ART_PINZA) == PINZA_CERRADA,
            "un rebote de 20 ms no mueve la pinza");
  ponerSwPinza(true);
  correr(100);
  COMPROBAR(articulaciones::objetivo(ART_PINZA) == PINZA_ABIERTA, "SW1 en abierto abre la pinza");
  ponerSwPinza(false);
  correr(100);
  COMPROBAR(articulaciones::objetivo(ART_PINZA) == PINZA_CERRADA, "SW1 en cerrado cierra la pinza");

  std::cout << "7. Modo app: manda la app y se ignoran pots y SW1\n";
  ponerModo(true);
  correr(100);                      // antirrebote de SW2
  COMPROBAR(control::modo() == Modo::APP, "mover SW2 pasa a modo app");
  COMPROBAR(control::mover(2, LIMITES[2].minimo) == Resultado::OK, "la app mueve el codo");
  COMPROBAR(control::codigoHttp(Resultado::OK) == 200, "una orden aceptada es un HTTP 200");
  correr(3000);
  COMPROBAR(fabsf(articulaciones::angulo(2) - LIMITES[2].minimo) < 1.0f,
            "el codo llega a donde pidio la app");
  potsEnMv(0, 0, 0);                // los tres pots al minimo
  correr(1000);
  COMPROBAR(fabsf(articulaciones::objetivo(2) - LIMITES[2].minimo) < 1.0f &&
            fabsf(articulaciones::angulo(0) - LIMITES[0].maximo) < 1.0f,
            "en modo app los potenciometros no mueven nada");
  COMPROBAR(control::mover(NUM_ARTICULACIONES, 90) == Resultado::ARTICULACION_INVALIDA &&
            control::codigoHttp(Resultado::ARTICULACION_INVALIDA) == 400,
            "una articulacion inexistente es un HTTP 400");
  COMPROBAR(control::pinza(false) == Resultado::OK, "la app cierra la pinza");
  correr(500);
  ponerSwPinza(true);               // SW1 pide abrir, pero manda la app
  correr(200);
  COMPROBAR(articulaciones::objetivo(ART_PINZA) == PINZA_CERRADA,
            "en modo app SW1 no abre la pinza");
  COMPROBAR(control::inicio() == Resultado::OK, "la app manda a la posicion de inicio");
  correr(3000);
  COMPROBAR(articulaciones::objetivo(1) == LIMITES[1].inicio, "el hombro queda en su inicio");

  std::cout << "8. Regreso de app a manual\n";
  potsEnMv(POT_MV_MAX, POT_MV_MAX, POT_MV_MAX);   // los pots piden el maximo de cada eje
  correr(1000);                                   // el filtro se asienta sin mover nada
  ponerModo(false);
  correr(100);                                    // antirrebote de SW2
  COMPROBAR(control::modo() == Modo::MANUAL, "mover SW2 regresa a modo manual");
  const float antes_regreso = articulaciones::angulo(1);
  correr(100);
  const float avance_regreso = articulaciones::angulo(1) - antes_regreso;
  COMPROBAR(avance_regreso > 0.0f && avance_regreso <= VELOCIDAD_MAX_GRADOS_S * 0.1f + 0.01f,
            "al regresar, el hombro va hacia el pot sin pasar de 120 grados/s");
  correr(3000);
  COMPROBAR(fabsf(articulaciones::angulo(1) - LIMITES[1].maximo) < 1.0f,
            "el hombro termina donde dice su potenciometro");

  std::cout << "9. LED D2 de estado\n";
  COMPROBAR(ledEncendido(PIN_LED_ESTADO), "en manual D2 queda encendido fijo");
  ponerModo(true);
  correr(100);
  sim::tiempo_ms = 20000;           // multiplo de los dos medios periodos
  clientes_ = 0;
  diagnostico::ciclo(clientes_);
  const bool d2_lento_a = ledEncendido(PIN_LED_ESTADO);
  sim::tiempo_ms = 20125;
  diagnostico::ciclo(clientes_);
  const bool d2_lento_b = ledEncendido(PIN_LED_ESTADO);
  clientes_ = 1;
  diagnostico::ciclo(clientes_);
  const bool d2_rapido_b = ledEncendido(PIN_LED_ESTADO);
  sim::tiempo_ms = 20500;
  clientes_ = 0;
  diagnostico::ciclo(clientes_);
  const bool d2_lento_c = ledEncendido(PIN_LED_ESTADO);
  COMPROBAR(d2_lento_a && d2_lento_b && !d2_lento_c,
            "en app sin celulares D2 parpadea a 1 Hz (medio periodo de 500 ms)");
  COMPROBAR(d2_lento_b && !d2_rapido_b,
            "con un celular conectado D2 parpadea a 4 Hz (medio periodo de 125 ms)");

  std::cout << "10. LED D3 y boton de diagnostico\n";
  sim::razon_reinicio = ESP_RST_BROWNOUT;
  diagnostico::iniciar();           // simula el arranque despues de una caida de 5 V
  COMPROBAR(diagnostico::alerta() && ledEncendido(PIN_LED_DIAG),
            "tras un brown-out D3 queda encendido");
  COMPROBAR(contiene(diagnostico::causaReinicio(), "BROWN-OUT"),
            "el firmware reconoce la causa del reinicio");
  sim::salida_serie.clear();
  ponerBotonDiag(true);
  correr(100);
  const std::string reporte = sim::salida_serie;
  COMPROBAR(contiene(reporte, "--- diagnostico ---") && contiene(reporte, "ultimo reinicio") &&
            contiene(reporte, "pot ") && contiene(reporte, "servo "),
            "el boton DIAG imprime el reporte por USB");
  COMPROBAR(!diagnostico::alerta(), "el boton DIAG apaga el aviso de brown-out");
  ponerBotonDiag(false);
  correr(100);
  COMPROBAR(!ledEncendido(PIN_LED_DIAG), "al soltar el boton D3 queda apagado");

  std::cout << "11. Consola por USB: solo diagnostico\n";
  COMPROBAR(ordenSerie("J 0 45") == "ERR control por USB deshabilitado\n",
            "J responde ERR: el control por USB se retiro");
  COMPROBAR(ordenSerie("A 10 60 70 50") == "ERR control por USB deshabilitado\n", "A responde ERR");
  COMPROBAR(ordenSerie("P A") == "ERR control por USB deshabilitado\n", "P responde ERR");
  COMPROBAR(ordenSerie("H") == "ERR control por USB deshabilitado\n", "H responde ERR");
  COMPROBAR(ordenSerie("X").rfind("ERR", 0) == 0, "una orden desconocida responde ERR");
  COMPROBAR(ordenSerie("?").rfind("OK ordenes:", 0) == 0, "? lista las ordenes que quedan");
  const std::string estado = ordenSerie("E");
  COMPROBAR(estado.rfind("OK {\"brazo\":", 0) == 0 && contiene(estado, "\"modo\":\"app\"") &&
            contiene(estado, "\"clientes\":") && contiene(estado, "\"diag\":false"),
            "E devuelve el estado en JSON con modo, clientes y diag");
  COMPROBAR(contiene(ordenSerie("D"), "--- diagnostico ---"), "D imprime el mismo reporte");

  std::cout << "\n" << (total - fallas) << " de " << total << " comprobaciones correctas\n";
  return fallas ? 1 : 0;
}
