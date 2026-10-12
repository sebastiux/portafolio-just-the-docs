// Arduino.h mínimo para compilar el firmware en la computadora (pruebas y simulador).
// Solo implementa lo que usan control, entradas, articulaciones y puerto_serie.
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

namespace sim {
// Estado del "hardware" simulado; las pruebas lo leen y lo modifican.
extern uint32_t tiempo_ms;
extern int pin_digital[32];
extern uint32_t mv_adc[32];
extern uint32_t duty[32];
extern std::string entrada_serie;   // lo que "llega" por el USB
extern std::string salida_serie;    // lo que el firmware escribió
}

inline uint32_t millis() { return sim::tiempo_ms; }
inline void pinMode(uint8_t, uint8_t) {}
inline int digitalRead(uint8_t p) { return sim::pin_digital[p]; }
inline void digitalWrite(uint8_t p, int v) { sim::pin_digital[p] = v; }
inline uint32_t analogReadMilliVolts(uint8_t p) { return sim::mv_adc[p]; }
inline bool ledcAttach(uint8_t, uint32_t, uint8_t) { return true; }
inline bool ledcWrite(uint8_t p, uint32_t d) { sim::duty[p] = d; return true; }

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
