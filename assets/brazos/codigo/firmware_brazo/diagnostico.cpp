// diagnostico.cpp — Ver diagnostico.h
#include "diagnostico.h"
#include "articulaciones.h"
#include "control.h"
#include "entradas.h"

#if defined(ARDUINO_ARCH_ESP32)
#include <esp_system.h>
#endif

namespace diagnostico {

namespace {
esp_reset_reason_t causa_ = ESP_RST_UNKNOWN;
bool alerta_ = false;

void escribirLed(uint8_t pin, bool encendido) {
  digitalWrite(pin, encendido ? LOW : HIGH);   // ánodo a 3V3: activo en bajo
}

const char* textoCausa(esp_reset_reason_t c) {
  switch (c) {
    case ESP_RST_POWERON:   return "encendido normal";
    case ESP_RST_EXT:       return "reset externo";
    case ESP_RST_SW:        return "reinicio por software";
    case ESP_RST_PANIC:     return "excepcion del programa";
    case ESP_RST_INT_WDT:   return "watchdog de interrupciones";
    case ESP_RST_TASK_WDT:  return "watchdog de tareas";
    case ESP_RST_WDT:       return "otro watchdog";
    case ESP_RST_DEEPSLEEP: return "salida de sueno profundo";
    case ESP_RST_BROWNOUT:  return "BROWN-OUT: cayo la alimentacion";
    case ESP_RST_SDIO:      return "reset por SDIO";
    default:                return "desconocida";
  }
}
}  // namespace

void iniciar() {
  pinMode(PIN_LED_ESTADO, OUTPUT);
  pinMode(PIN_LED_DIAG, OUTPUT);
  causa_ = esp_reset_reason();
  alerta_ = (causa_ == ESP_RST_BROWNOUT);
  escribirLed(PIN_LED_ESTADO, false);
  escribirLed(PIN_LED_DIAG, alerta_);
}

void ciclo(uint8_t clientes) {
  const uint32_t t = millis();

  // D2: fijo en manual; en app parpadea lento sin celulares y rápido con uno.
  bool d2;
  if (control::modo() == Modo::MANUAL) {
    d2 = true;
  } else {
    const uint32_t medio = clientes > 0 ? LED_APP_CON_CLIENTES_MS : LED_APP_SIN_CLIENTES_MS;
    d2 = (t / medio) % 2 == 0;
  }
  escribirLed(PIN_LED_ESTADO, d2);

  // El botón DIAG imprime el reporte y apaga la alerta. No mueve servos.
  if (entradas::botonDiagPulsacion()) reporte(clientes);

  // D3: parpadea mientras el botón está presionado; si no, fijo solo si hay alerta.
  const bool presionado = entradas::botonDiagPresionado();
  escribirLed(PIN_LED_DIAG, presionado ? ((t / LED_DIAG_PARPADEO_MS) % 2 == 0) : alerta_);
}

void reporte(uint8_t clientes) {
  char linea[120];

  Serial.println(F("--- diagnostico ---"));

  snprintf(linea, sizeof(linea), "brazo          : %s", NOMBRE_BRAZO);
  Serial.println(linea);
  snprintf(linea, sizeof(linea), "ultimo reinicio: %s", textoCausa(causa_));
  Serial.println(linea);
  snprintf(linea, sizeof(linea), "encendido hace : %lu s",
           static_cast<unsigned long>(millis() / 1000));
  Serial.println(linea);
  snprintf(linea, sizeof(linea), "modo (SW2)     : %s", control::nombreModo(control::modo()));
  Serial.println(linea);
  snprintf(linea, sizeof(linea), "pinza (SW1)    : %s",
           entradas::pinzaAbierta() ? "abierta" : "cerrada");
  Serial.println(linea);
  snprintf(linea, sizeof(linea), "celulares      : %u", static_cast<unsigned>(clientes));
  Serial.println(linea);

  for (uint8_t i = 0; i < NUM_POTS; i++) {
    snprintf(linea, sizeof(linea), "pot %-7s    : %u mV",
             LIMITES[i].nombre, static_cast<unsigned>(entradas::milivoltsPot(i)));
    Serial.println(linea);
  }
  for (uint8_t i = 0; i < NUM_ARTICULACIONES; i++) {
    snprintf(linea, sizeof(linea), "servo %-7s  : %.1f grados (objetivo %.1f)",
             LIMITES[i].nombre, articulaciones::angulo(i), articulaciones::objetivo(i));
    Serial.println(linea);
  }

  alerta_ = false;
  escribirLed(PIN_LED_DIAG, false);
}

bool alerta() { return alerta_; }

const char* causaReinicio() { return textoCausa(causa_); }

}  // namespace diagnostico
