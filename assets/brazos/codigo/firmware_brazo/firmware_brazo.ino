// firmware_brazo.ino — Control de los brazos robóticos con ESP32-C3 Super Mini.
//
// Integración Mecatrónica Otoño 2026
// Juan Pablo Martha · Carlos Sebastián Ortega · Santiago Alejandro Velázquez
//
// Un solo firmware para los dos brazos (impreso en 3D y cortado con láser):
// se elige el brazo en config.h. El mando lo decide el switch SW2 de la tarjeta:
//   - MANUAL: 3 potenciómetros (base, hombro, codo) y SW1 (pinza)
//   - APP:    red "Brazo-Impreso" o "Brazo-Laser", página en http://192.168.4.1
// El USB queda solo para diagnóstico (órdenes E, D y ?).
//
// Placa en Arduino IDE: "ESP32C3 Dev Module", con "USB CDC On Boot: Enabled".

#include "config.h"
#include "control.h"
#include "diagnostico.h"
#include "puerto_serie.h"
#include "servidor_web.h"

static uint32_t ultimo_ciclo_ms = 0;

void setup() {
  puerto_serie::iniciar();
  diagnostico::iniciar();
  control::iniciar();
  servidor_web::iniciar();
  ultimo_ciclo_ms = millis();
}

void loop() {
  // El número de celulares conectados lo sabe el servidor; control y
  // diagnóstico lo reciben para el JSON de estado, el reporte y el LED D2.
  const uint8_t clientes = servidor_web::clientes();

  puerto_serie::atender(clientes);
  servidor_web::atender();

  const uint32_t ahora = millis();
  if (ahora - ultimo_ciclo_ms >= PERIODO_CONTROL_MS) {
    const float dt = (ahora - ultimo_ciclo_ms) / 1000.0f;
    ultimo_ciclo_ms = ahora;
    control::ciclo(dt);
    diagnostico::ciclo(clientes);
  }
}
