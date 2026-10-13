// firmware_brazo.ino — Control de los brazos robóticos con ESP32-C3 Super Mini.
//
// Integración Mecatrónica Otoño 2026
// Juan Pablo Martha · Carlos Sebastián Ortega · Santiago Alejandro Velázquez
//
// Tarjeta: brazo_control v3 (58 × 48 mm, una cara). Un solo firmware para los
// dos brazos (impreso en 3D y cortado con láser): se elige el brazo en config.h.
//   - Interruptor MODO (SW2) en Manual: potenciómetros RV1–RV3 e interruptor SW1
//   - Interruptor MODO (SW2) en App: app web en la red "Brazo-Impreso" o
//     "Brazo-Laser" (http://192.168.4.1) o brazo_gui.py por USB
//   - Botón BOOT del módulo: secuencia de diagnóstico
//
// Placa en Arduino IDE: "ESP32C3 Dev Module", con "USB CDC On Boot: Enabled".

#include "config.h"
#include "control.h"
#include "puerto_serie.h"
#include "servidor_web.h"

static uint32_t ultimo_ciclo_ms = 0;

static void led(uint8_t pin, bool encendido) {
  digitalWrite(pin, encendido ? LOW : HIGH);   // los dos LEDs son activos en bajo
}

// D2 (estado): fijo = Manual, parpadeo lento = App esperando o app web,
// parpadeo rápido = la última orden llegó por USB.
// D3 (DIAG): encendido durante el diagnóstico; parpadeo rápido si no se pudo
// crear la red Wi-Fi.
static void actualizarLeds() {
  const uint32_t t = millis();
  bool estado;
  if (!control::modoApp())                          estado = true;
  else if (control::fuenteActual() == Fuente::SERIE) estado = (t / 125) % 2;
  else                                              estado = (t / 500) % 2;
  led(PIN_LED_ESTADO, estado);

  bool diag = control::enDiagnostico();
  if (!diag && !servidor_web::activo()) diag = (t / 125) % 2;
  led(PIN_LED_DIAG, diag);
}

void setup() {
  pinMode(PIN_LED_ESTADO, OUTPUT);
  pinMode(PIN_LED_DIAG, OUTPUT);
  led(PIN_LED_ESTADO, false);
  led(PIN_LED_DIAG, false);
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
    actualizarLeds();
  }
}
