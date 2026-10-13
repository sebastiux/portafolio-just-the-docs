// entradas.cpp — Ver entradas.h
#include "entradas.h"

namespace entradas {

namespace {
// Entrada digital con antirrebote: el cambio cuenta solo si se mantiene ANTIRREBOTE_MS.
struct Digital {
  uint8_t pin;
  bool estable;
  bool anterior;
  uint32_t desde_ms;
  bool cambio;

  void iniciar() {
    pinMode(pin, INPUT_PULLUP);
    estable = anterior = digitalRead(pin);
    desde_ms = millis();
    cambio = false;
  }
  void leer(uint32_t ahora) {
    const bool v = digitalRead(pin);
    if (v != anterior) {
      anterior = v;
      desde_ms = ahora;
    } else if (v != estable && ahora - desde_ms >= ANTIRREBOTE_MS) {
      estable = v;
      cambio = true;
    }
  }
};

float mv_filtrado_[NUM_POTS];
Digital sw_pinza_{PIN_SW_PINZA, true, true, 0, false};
Digital sw_modo_{PIN_SW_MODO, true, true, 0, false};
Digital boton_{PIN_BOTON_DIAG, true, true, 0, false};
}  // namespace

void iniciar() {
  sw_pinza_.iniciar();
  sw_modo_.iniciar();
  boton_.iniciar();
  for (uint8_t i = 0; i < NUM_POTS; i++) mv_filtrado_[i] = analogReadMilliVolts(PIN_POT[i]);
}

void leer() {
  // Filtro exponencial: quita el ruido del ADC sin agregar mucho retardo.
  for (uint8_t i = 0; i < NUM_POTS; i++) {
    const float mv = analogReadMilliVolts(PIN_POT[i]);
    mv_filtrado_[i] += POT_FILTRO_ALFA * (mv - mv_filtrado_[i]);
  }
  const uint32_t ahora = millis();
  sw_pinza_.leer(ahora);
  sw_modo_.leer(ahora);
  boton_.leer(ahora);
}

float anguloPot(uint8_t pot) {
  if (pot >= NUM_POTS) return 0.0f;
  float fraccion = mv_filtrado_[pot] / POT_MV_MAX;
  if (fraccion < 0.0f) fraccion = 0.0f;
  if (fraccion > 1.0f) fraccion = 1.0f;
  const LimitesArticulacion& l = LIMITES[pot];   // el pot i mueve la articulación i
  return l.minimo + fraccion * (l.maximo - l.minimo);
}

bool pinzaAbierta() { return sw_pinza_.estable == NIVEL_PINZA_ABIERTA; }
bool modoApp()      { return sw_modo_.estable == NIVEL_MODO_APP; }

bool pinzaCambio() {
  const bool c = sw_pinza_.cambio;
  sw_pinza_.cambio = false;
  return c;
}

bool botonDiagPresionado() {
  const bool c = boton_.cambio && boton_.estable == LOW;   // flanco de bajada: se presionó
  boton_.cambio = false;
  return c;
}

}  // namespace entradas
