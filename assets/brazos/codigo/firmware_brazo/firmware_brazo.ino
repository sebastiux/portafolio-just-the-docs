// firmware_brazo.ino — Control de los brazos robóticos con ESP32-C3 Super Mini.
//
// Integración Mecatrónica Otoño 2026
// Juan Pablo Martha · Carlos Sebastián Ortega · Santiago Alejandro Velázquez
//
// Un solo firmware para los dos brazos (impreso en 3D y cortado con láser):
// se elige el brazo en config.h. Tres modos de mando, con cambio automático:
//   - manual: 3 potenciómetros (base, hombro, codo) e interruptor (pinza)
//   - app web: red "Brazo-Impreso" o "Brazo-Laser", página en http://192.168.4.1
//   - USB: brazo_gui.py desde la computadora
//
// Placa en Arduino IDE: "ESP32C3 Dev Module", con "USB CDC On Boot: Enabled".

#include "config.h"
#include "control.h"
#include "puerto_serie.h"
#include "servidor_web.h"

static uint32_t ultimo_ciclo_ms = 0;

// LED de la placa según la fuente: fijo = manual, lento = web, rápido = USB.
static void actualizarLed() {
  const uint32_t t = millis();
  bool encendido;
  switch (control::fuenteActual()) {
    case Fuente::WEB:   encendido = (t / 500) % 2; break;
    case Fuente::SERIE: encendido = (t / 125) % 2; break;
    default:            encendido = true;          break;
  }
  digitalWrite(PIN_LED, encendido ? LOW : HIGH);   // activo en bajo
}

void setup() {
  pinMode(PIN_LED, OUTPUT);
  puerto_serie::iniciar();
  control::iniciar();
  servidor_web::iniciar();
  ultimo_ciclo_ms = millis();
}

void loop() {
  puerto_serie::atender();
  servidor_web::atender();

  const uint32_t ahora = millis();
  if (ahora - ultimo_ciclo_ms >= PERIODO_CONTROL_MS) {
    const float dt = (ahora - ultimo_ciclo_ms) / 1000.0f;
    ultimo_ciclo_ms = ahora;
    control::ciclo(dt);
    actualizarLed();
  }
}
