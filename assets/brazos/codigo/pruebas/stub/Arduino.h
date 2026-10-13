// Arduino.h mínimo para compilar el firmware en la computadora (pruebas).
// Solo implementa lo que usan config, articulaciones, entradas, control,
// diagnostico y puerto_serie. El servidor web y el Wi-Fi no se compilan aquí:
// la lógica que las rutas necesitan vive en control::codigoHttp y
// control::cuerpoJson, y el número de celulares conectados entra como
// parámetro, así que se puede probar sin ellos.
#pragma once
#include <cctype>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <strings.h>
#include <string>

#define F(s) (s)
#define PROGMEM
enum { LOW = 0, HIGH = 1 };
enum { INPUT = 0, OUTPUT = 1, INPUT_PULLUP = 2 };

// Mismos nombres y valores que esp_system.h del núcleo esp32.
typedef enum {
  ESP_RST_UNKNOWN = 0,
  ESP_RST_POWERON,
  ESP_RST_EXT,
  ESP_RST_SW,
  ESP_RST_PANIC,
  ESP_RST_INT_WDT,
  ESP_RST_TASK_WDT,
  ESP_RST_WDT,
  ESP_RST_DEEPSLEEP,
  ESP_RST_BROWNOUT,
  ESP_RST_SDIO,
} esp_reset_reason_t;

namespace sim {
// Estado del "hardware" simulado; las pruebas lo leen y lo modifican.
extern uint32_t tiempo_ms;
extern int pin_digital[32];
extern uint32_t mv_adc[32];
extern uint32_t duty[32];
extern std::string entrada_serie;        // lo que "llega" por el USB
extern std::string salida_serie;         // lo que el firmware escribió
extern esp_reset_reason_t razon_reinicio;
}

inline uint32_t millis() { return sim::tiempo_ms; }
inline void pinMode(uint8_t, uint8_t) {}
inline int digitalRead(uint8_t p) { return sim::pin_digital[p]; }
inline void digitalWrite(uint8_t p, int v) { sim::pin_digital[p] = v; }
inline uint32_t analogReadMilliVolts(uint8_t p) { return sim::mv_adc[p]; }
inline bool ledcAttach(uint8_t, uint32_t, uint8_t) { return true; }
inline bool ledcWrite(uint8_t p, uint32_t d) { sim::duty[p] = d; return true; }
inline esp_reset_reason_t esp_reset_reason() { return sim::razon_reinicio; }

class SerieSimulada {
 public:
  void begin(unsigned long) {}
  int available() { return static_cast<int>(sim::entrada_serie.size()); }
  int read() {
    if (sim::entrada_serie.empty()) return -1;
    const char c = sim::entrada_serie.front();
    sim::entrada_serie.erase(0, 1);
    return c;
  }
  void print(const char* s) { sim::salida_serie += s; }
  void println(const char* s) { sim::salida_serie += s; sim::salida_serie += "\n"; }
};
extern SerieSimulada Serial;
