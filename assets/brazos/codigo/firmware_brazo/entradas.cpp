// entradas.cpp — Ver entradas.h
#include "entradas.h"

namespace entradas {

namespace {
float mv_filtrado_[NUM_POTS];
bool estado_estable_ = false;
bool lectura_anterior_ = false;
uint32_t ultimo_cambio_ms_ = 0;
bool hubo_cambio_ = false;

bool leerInterruptor() {
  return digitalRead(PIN_INTERRUPTOR) == LOW;   // cerrado a GND = activo
}
}  // namespace

void iniciar() {
  pinMode(PIN_INTERRUPTOR, INPUT_PULLUP);
  for (uint8_t i = 0; i < NUM_POTS; i++) {
    mv_filtrado_[i] = analogReadMilliVolts(PIN_POT[i]);
  }
  estado_estable_ = lectura_anterior_ = leerInterruptor();
}

void leer() {
  // Filtro exponencial: quita el ruido del ADC sin agregar mucho retardo.
  for (uint8_t i = 0; i < NUM_POTS; i++) {
    const float mv = analogReadMilliVolts(PIN_POT[i]);
    mv_filtrado_[i] += POT_FILTRO_ALFA * (mv - mv_filtrado_[i]);
  }

  // Antirrebote: el cambio cuenta solo si la lectura se mantiene ANTIRREBOTE_MS.
  const bool lectura = leerInterruptor();
  const uint32_t ahora = millis();
  if (lectura != lectura_anterior_) {
    lectura_anterior_ = lectura;
    ultimo_cambio_ms_ = ahora;
  } else if (lectura != estado_estable_ && ahora - ultimo_cambio_ms_ >= ANTIRREBOTE_MS) {
    estado_estable_ = lectura;
    hubo_cambio_ = true;
  }
}

float anguloPot(uint8_t pot) {
  if (pot >= NUM_POTS) return 0.0f;
  float fraccion = mv_filtrado_[pot] / POT_MV_MAX;
  if (fraccion < 0.0f) fraccion = 0.0f;
  if (fraccion > 1.0f) fraccion = 1.0f;
  const LimitesArticulacion& l = LIMITES[pot];   // el pot i mueve la articulación i
  return l.minimo + fraccion * (l.maximo - l.minimo);
}

bool interruptorActivo() { return estado_estable_; }

bool interruptorCambio() {
  const bool c = hubo_cambio_;
  hubo_cambio_ = false;
  return c;
}

}  // namespace entradas
