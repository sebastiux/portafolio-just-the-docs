// control.h — Modo de operación, órdenes y diagnóstico del brazo.
//
// El interruptor MODO (SW2) decide quién mueve el brazo:
//   Manual : potenciómetros RV1–RV3 y SW1 (pinza)
//   App    : app web (http://192.168.4.1) o brazo_gui.py por USB; manda la
//            última que dio una orden
// El botón BOOT del módulo (DIAG) corre una secuencia de diagnóstico en
// cualquier modo.
#pragma once
#include "config.h"

enum class Fuente : uint8_t { MANUAL, WEB, SERIE };
enum class Resultado : uint8_t { ACEPTADA, MODO_MANUAL, INVALIDA, EN_DIAGNOSTICO };

namespace control {

void iniciar();
void ciclo(float dt_s);                                       // lee entradas, aplica el modo y mueve servos

Resultado mover(uint8_t art, float grados, Fuente fuente);    // solo en modo App
Resultado pinza(bool abrir, Fuente fuente);
Resultado inicio(Fuente fuente);
void diagnostico();                                           // arranca la secuencia (también con BOOT)

bool modoApp();
bool enDiagnostico();
Fuente fuenteActual();
const char* nombreFuente(Fuente f);
const char* textoResultado(Resultado r);
size_t estadoJson(char* destino, size_t tam);                 // estado completo en JSON

}  // namespace control
