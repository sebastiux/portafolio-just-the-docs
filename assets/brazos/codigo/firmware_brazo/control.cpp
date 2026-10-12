// control.cpp — Ver control.h
#include "control.h"
#include "articulaciones.h"
#include "entradas.h"

namespace control {

namespace {
Fuente fuente_ = Fuente::MANUAL;
float referencia_pot_[NUM_POTS];   // posición de los pots cuando un mando remoto tomó el control

void tomarControlRemoto(Fuente f) {
  if (f == Fuente::MANUAL) return;
  if (fuente_ == Fuente::MANUAL) {
    for (uint8_t i = 0; i < NUM_POTS; i++) referencia_pot_[i] = entradas::anguloPot(i);
  }
  fuente_ = f;
}

bool potenciometroMovido() {
  for (uint8_t i = 0; i < NUM_POTS; i++) {
    if (fabsf(entradas::anguloPot(i) - referencia_pot_[i]) > UMBRAL_TOMA_MANUAL_GRADOS) return true;
  }
  return false;
}
}  // namespace

void iniciar() {
  entradas::iniciar();
  articulaciones::iniciar();
  for (uint8_t i = 0; i < NUM_POTS; i++) referencia_pot_[i] = entradas::anguloPot(i);
  articulaciones::fijarObjetivo(ART_PINZA, entradas::interruptorActivo() ? PINZA_ABIERTA : PINZA_CERRADA);
}

void ciclo(float dt_s) {
  entradas::leer();

  if (fuente_ != Fuente::MANUAL && potenciometroMovido()) fuente_ = Fuente::MANUAL;

  if (fuente_ == Fuente::MANUAL) {
    for (uint8_t i = 0; i < NUM_POTS; i++) articulaciones::fijarObjetivo(i, entradas::anguloPot(i));
  }

  // El interruptor manda sobre la pinza en cuanto cambia, sin importar la fuente.
  if (entradas::interruptorCambio()) {
    articulaciones::fijarObjetivo(ART_PINZA, entradas::interruptorActivo() ? PINZA_ABIERTA : PINZA_CERRADA);
  }

  articulaciones::actualizar(dt_s);
}

bool mover(uint8_t art, float grados, Fuente fuente) {
  if (art >= NUM_ARTICULACIONES) return false;
  tomarControlRemoto(fuente);
  articulaciones::fijarObjetivo(art, grados);
  return true;
}

void pinza(bool abrir, Fuente fuente) {
  tomarControlRemoto(fuente);
  articulaciones::fijarObjetivo(ART_PINZA, abrir ? PINZA_ABIERTA : PINZA_CERRADA);
}

void inicio(Fuente fuente) {
  tomarControlRemoto(fuente);
  articulaciones::irAInicio();
}

Fuente fuenteActual() { return fuente_; }

const char* nombreFuente(Fuente f) {
  switch (f) {
    case Fuente::WEB:   return "web";
    case Fuente::SERIE: return "serie";
    default:            return "manual";
  }
}

size_t estadoJson(char* destino, size_t tam) {
  size_t n = snprintf(destino, tam, "{\"brazo\":\"%s\",\"fuente\":\"%s\",\"articulaciones\":[",
                      NOMBRE_BRAZO, nombreFuente(fuente_));
  for (uint8_t i = 0; i < NUM_ARTICULACIONES && n < tam; i++) {
    n += snprintf(destino + n, tam - n,
                  "%s{\"nombre\":\"%s\",\"angulo\":%.1f,\"objetivo\":%.1f,\"min\":%u,\"max\":%u}",
                  i ? "," : "", LIMITES[i].nombre, articulaciones::angulo(i),
                  articulaciones::objetivo(i), LIMITES[i].minimo, LIMITES[i].maximo);
  }
  if (n < tam) {
    n += snprintf(destino + n, tam - n, "],\"pinza_abierta\":%u,\"pinza_cerrada\":%u,\"interruptor\":%s}",
                  PINZA_ABIERTA, PINZA_CERRADA, entradas::interruptorActivo() ? "true" : "false");
  }
  return n;
}

}  // namespace control
