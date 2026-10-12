// articulaciones.cpp — Ver articulaciones.h
#include "articulaciones.h"

namespace articulaciones {

namespace {
float actual_[NUM_ARTICULACIONES];
float objetivo_[NUM_ARTICULACIONES];

// Convierte grados (0–180) a ciclo de trabajo del LEDC.
uint32_t gradosADuty(float grados) {
  const float pulso_us = SERVO_PULSO_MIN_US +
                         (SERVO_PULSO_MAX_US - SERVO_PULSO_MIN_US) * (grados / 180.0f);
  const float periodo_us = 1000000.0f / SERVO_FRECUENCIA_HZ;
  const uint32_t maximo = (1u << SERVO_RESOLUCION_BITS) - 1;
  return static_cast<uint32_t>(pulso_us / periodo_us * maximo + 0.5f);
}

void escribir(uint8_t art, float grados) {
  ledcWrite(PIN_SERVO[art], gradosADuty(grados));
}
}  // namespace

float limitar(uint8_t art, float grados) {
  const LimitesArticulacion& l = LIMITES[art];
  if (grados < l.minimo) return l.minimo;
  if (grados > l.maximo) return l.maximo;
  return grados;
}

void iniciar() {
  for (uint8_t i = 0; i < NUM_ARTICULACIONES; i++) {
    ledcAttach(PIN_SERVO[i], SERVO_FRECUENCIA_HZ, SERVO_RESOLUCION_BITS);
    actual_[i] = objetivo_[i] = LIMITES[i].inicio;
    escribir(i, actual_[i]);
  }
}

void fijarObjetivo(uint8_t art, float grados) {
  if (art >= NUM_ARTICULACIONES) return;
  objetivo_[art] = limitar(art, grados);
}

void irAInicio() {
  for (uint8_t i = 0; i < NUM_ARTICULACIONES; i++) objetivo_[i] = LIMITES[i].inicio;
}

void actualizar(float dt_s) {
  const float paso = VELOCIDAD_MAX_GRADOS_S * dt_s;
  for (uint8_t i = 0; i < NUM_ARTICULACIONES; i++) {
    const float error = objetivo_[i] - actual_[i];
    if (error == 0.0f) continue;
    if (error > paso)        actual_[i] += paso;
    else if (error < -paso)  actual_[i] -= paso;
    else                     actual_[i] = objetivo_[i];
    escribir(i, actual_[i]);
  }
}

float angulo(uint8_t art)   { return art < NUM_ARTICULACIONES ? actual_[art] : 0.0f; }
float objetivo(uint8_t art) { return art < NUM_ARTICULACIONES ? objetivo_[art] : 0.0f; }

}  // namespace articulaciones
