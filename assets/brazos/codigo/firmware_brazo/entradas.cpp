// entradas.cpp — Ver entradas.h
#include "entradas.h"

namespace entradas {

namespace {

// Antirrebote común a los dos switches y al botón: la lectura solo pasa a
// `estable` si se mantiene ANTIRREBOTE_MS sin cambiar.
struct Antirrebote {
  bool estable = false;
  bool anterior = false;
  uint32_t ultimo_cambio_ms = 0;

  void iniciar(bool lectura) { estable = anterior = lectura; }

  void actualizar(bool lectura, uint32_t ahora) {
    if (lectura != anterior) {
      anterior = lectura;
      ultimo_cambio_ms = ahora;
    } else if (lectura != estable && ahora - ultimo_cambio_ms >= ANTIRREBOTE_MS) {
      estable = lectura;
    }
  }
};

// El botón DIAG es el BOOT del módulo: presionado al encender entra en modo de
// descarga, así que no se atiende hasta pasado este tiempo desde el arranque.
constexpr uint32_t DIAG_IGNORAR_AL_ARRANQUE_MS = 1000;

float mv_filtrado_[NUM_POTS];
Antirrebote sw_pinza_, sw_modo_, boton_diag_;
uint32_t arranque_ms_ = 0;
bool diag_pulsacion_ = false;

}  // namespace

void iniciar() {
  pinMode(PIN_SW_PINZA, INPUT_PULLUP);
  pinMode(PIN_SW_MODO, INPUT_PULLUP);
  pinMode(PIN_BOTON_DIAG, INPUT_PULLUP);
  for (uint8_t i = 0; i < NUM_POTS; i++) {
    mv_filtrado_[i] = analogReadMilliVolts(PIN_POT[i]);
  }
  sw_pinza_.iniciar(digitalRead(PIN_SW_PINZA) == LOW);
  sw_modo_.iniciar(digitalRead(PIN_SW_MODO) == LOW);
  boton_diag_.iniciar(digitalRead(PIN_BOTON_DIAG) == LOW);
  arranque_ms_ = millis();
  diag_pulsacion_ = false;
}

void leer() {
  // Filtro exponencial: quita el ruido del ADC sin agregar mucho retardo.
  for (uint8_t i = 0; i < NUM_POTS; i++) {
    const float mv = analogReadMilliVolts(PIN_POT[i]);
    mv_filtrado_[i] += POT_FILTRO_ALFA * (mv - mv_filtrado_[i]);
  }

  const uint32_t ahora = millis();
  sw_pinza_.actualizar(digitalRead(PIN_SW_PINZA) == LOW, ahora);
  sw_modo_.actualizar(digitalRead(PIN_SW_MODO) == LOW, ahora);

  // Flanco de bajada del botón, ya antirrebotado: una pulsación.
  const bool presionado_antes = boton_diag_.estable;
  boton_diag_.actualizar(digitalRead(PIN_BOTON_DIAG) == LOW, ahora);
  if (ahora - arranque_ms_ >= DIAG_IGNORAR_AL_ARRANQUE_MS &&
      boton_diag_.estable && !presionado_antes) {
    diag_pulsacion_ = true;
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

uint16_t milivoltsPot(uint8_t pot) {
  return pot < NUM_POTS ? static_cast<uint16_t>(mv_filtrado_[pot] + 0.5f) : 0;
}

bool modoApp()      { return sw_modo_.estable == MODO_APP_EN_BAJO; }
bool pinzaAbierta() { return sw_pinza_.estable == PINZA_ABIERTA_EN_BAJO; }

bool botonDiagPresionado() { return boton_diag_.estable; }

bool botonDiagPulsacion() {
  const bool p = diag_pulsacion_;
  diag_pulsacion_ = false;
  return p;
}

}  // namespace entradas
