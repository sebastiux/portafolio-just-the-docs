// control.cpp — Ver control.h
#include "control.h"
#include "articulaciones.h"
#include "entradas.h"

namespace control {

namespace {
Modo modo_ = Modo::MANUAL;

// En MANUAL los cuatro objetivos se copian de las entradas en cada ciclo. Eso
// hace que el regreso de APP a MANUAL no necesite ningún caso especial.
void objetivosDesdeEntradas() {
  for (uint8_t i = 0; i < NUM_POTS; i++) {
    articulaciones::fijarObjetivo(i, entradas::anguloPot(i));
  }
  articulaciones::fijarObjetivo(ART_PINZA, entradas::pinzaAbierta() ? PINZA_ABIERTA : PINZA_CERRADA);
}
}  // namespace

void iniciar() {
  entradas::iniciar();
  articulaciones::iniciar();
  modo_ = entradas::modoApp() ? Modo::APP : Modo::MANUAL;
  if (modo_ == Modo::MANUAL) objetivosDesdeEntradas();
}

void ciclo(float dt_s) {
  entradas::leer();
  modo_ = entradas::modoApp() ? Modo::APP : Modo::MANUAL;
  if (modo_ == Modo::MANUAL) objetivosDesdeEntradas();
  articulaciones::actualizar(dt_s);
}

Resultado mover(uint8_t art, float grados) {
  if (modo_ == Modo::MANUAL) return Resultado::MODO_MANUAL;
  if (art >= NUM_ARTICULACIONES) return Resultado::ARTICULACION_INVALIDA;
  articulaciones::fijarObjetivo(art, grados);
  return Resultado::OK;
}

Resultado pinza(bool abrir) {
  if (modo_ == Modo::MANUAL) return Resultado::MODO_MANUAL;
  articulaciones::fijarObjetivo(ART_PINZA, abrir ? PINZA_ABIERTA : PINZA_CERRADA);
  return Resultado::OK;
}

Resultado inicio() {
  if (modo_ == Modo::MANUAL) return Resultado::MODO_MANUAL;
  articulaciones::irAInicio();
  return Resultado::OK;
}

Modo modo() { return modo_; }

const char* nombreModo(Modo m) { return m == Modo::APP ? "app" : "manual"; }

uint16_t codigoHttp(Resultado r) {
  switch (r) {
    case Resultado::OK:          return 200;
    case Resultado::MODO_MANUAL: return 409;   // conflicto: el hardware tiene el mando
    default:                     return 400;
  }
}

const char* cuerpoJson(Resultado r) {
  switch (r) {
    case Resultado::MODO_MANUAL: return "{\"error\":\"modo manual\"}";
    default:                     return "{\"error\":\"articulacion invalida\"}";
  }
}

size_t estadoJson(char* destino, size_t tam, uint8_t clientes, bool diag) {
  size_t n = snprintf(destino, tam,
                      "{\"brazo\":\"%s\",\"modo\":\"%s\",\"clientes\":%u,\"diag\":%s,\"articulaciones\":[",
                      NOMBRE_BRAZO, nombreModo(modo_), clientes, diag ? "true" : "false");
  for (uint8_t i = 0; i < NUM_ARTICULACIONES && n < tam; i++) {
    n += snprintf(destino + n, tam - n,
                  "%s{\"nombre\":\"%s\",\"angulo\":%.1f,\"objetivo\":%.1f,\"min\":%u,\"max\":%u}",
                  i ? "," : "", LIMITES[i].nombre, articulaciones::angulo(i),
                  articulaciones::objetivo(i), LIMITES[i].minimo, LIMITES[i].maximo);
  }
  if (n < tam) {
    n += snprintf(destino + n, tam - n, "],\"pinza_abierta\":%u,\"pinza_cerrada\":%u}",
                  PINZA_ABIERTA, PINZA_CERRADA);
  }
  return n;
}

}  // namespace control
