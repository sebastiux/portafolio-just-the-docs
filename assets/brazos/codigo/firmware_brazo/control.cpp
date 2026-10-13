// control.cpp — Ver control.h
#include "control.h"
#include "articulaciones.h"
#include "entradas.h"

namespace control {

namespace {
Fuente fuente_ = Fuente::MANUAL;
bool modo_app_ = false;

// Diagnóstico: por cada articulación, mínimo → máximo → inicio.
constexpr uint8_t PASOS_DIAG = NUM_ARTICULACIONES * 3;
bool diag_ = false;
uint8_t paso_diag_ = 0;
uint32_t inicio_paso_ms_ = 0;

void aplicarPasoDiag() {
  const uint8_t art = paso_diag_ / 3;
  const LimitesArticulacion& l = LIMITES[art];
  const uint8_t destino[3] = {l.minimo, l.maximo, l.inicio};
  articulaciones::fijarObjetivo(art, destino[paso_diag_ % 3]);
  inicio_paso_ms_ = millis();
}

void avanzarDiag() {
  if (millis() - inicio_paso_ms_ < DIAG_PASO_MS) return;
  if (++paso_diag_ >= PASOS_DIAG) {
    diag_ = false;
    return;
  }
  aplicarPasoDiag();
}

Resultado aceptar(Fuente fuente) {
  if (diag_) return Resultado::EN_DIAGNOSTICO;
  if (!modo_app_) return Resultado::MODO_MANUAL;
  fuente_ = fuente;
  return Resultado::ACEPTADA;
}
}  // namespace

void iniciar() {
  entradas::iniciar();
  articulaciones::iniciar();
  modo_app_ = entradas::modoApp();
  fuente_ = modo_app_ ? Fuente::WEB : Fuente::MANUAL;
  articulaciones::fijarObjetivo(ART_PINZA, entradas::pinzaAbierta() ? PINZA_ABIERTA : PINZA_CERRADA);
}

void ciclo(float dt_s) {
  entradas::leer();

  if (entradas::botonDiagPresionado() && !diag_) diagnostico();

  // Cambio de modo con SW2. Al pasar a App el brazo se queda donde está;
  // al regresar a Manual sigue otra vez a los potenciómetros.
  const bool app = entradas::modoApp();
  if (app != modo_app_) {
    modo_app_ = app;
    fuente_ = app ? Fuente::WEB : Fuente::MANUAL;
    if (!app) articulaciones::fijarObjetivo(ART_PINZA, entradas::pinzaAbierta() ? PINZA_ABIERTA : PINZA_CERRADA);
  }

  const bool cambio_pinza = entradas::pinzaCambio();
  if (diag_) {
    avanzarDiag();
  } else if (!modo_app_) {
    for (uint8_t i = 0; i < NUM_POTS; i++) articulaciones::fijarObjetivo(i, entradas::anguloPot(i));
    if (cambio_pinza) {
      articulaciones::fijarObjetivo(ART_PINZA, entradas::pinzaAbierta() ? PINZA_ABIERTA : PINZA_CERRADA);
    }
  }

  articulaciones::actualizar(dt_s);
}

Resultado mover(uint8_t art, float grados, Fuente fuente) {
  if (art >= NUM_ARTICULACIONES) return Resultado::INVALIDA;
  const Resultado r = aceptar(fuente);
  if (r == Resultado::ACEPTADA) articulaciones::fijarObjetivo(art, grados);
  return r;
}

Resultado pinza(bool abrir, Fuente fuente) {
  const Resultado r = aceptar(fuente);
  if (r == Resultado::ACEPTADA) articulaciones::fijarObjetivo(ART_PINZA, abrir ? PINZA_ABIERTA : PINZA_CERRADA);
  return r;
}

Resultado inicio(Fuente fuente) {
  const Resultado r = aceptar(fuente);
  if (r == Resultado::ACEPTADA) articulaciones::irAInicio();
  return r;
}

void diagnostico() {
  diag_ = true;
  paso_diag_ = 0;
  aplicarPasoDiag();
}

bool modoApp() { return modo_app_; }
bool enDiagnostico() { return diag_; }
Fuente fuenteActual() { return fuente_; }

const char* nombreFuente(Fuente f) {
  switch (f) {
    case Fuente::WEB:   return "web";
    case Fuente::SERIE: return "serie";
    default:            return "manual";
  }
}

const char* textoResultado(Resultado r) {
  switch (r) {
    case Resultado::ACEPTADA:       return "OK";
    case Resultado::MODO_MANUAL:    return "ERR modo manual: pasa el interruptor MODO a App";
    case Resultado::EN_DIAGNOSTICO: return "ERR diagnostico en curso";
    default:                        return "ERR articulacion invalida";
  }
}

size_t estadoJson(char* destino, size_t tam) {
  size_t n = snprintf(destino, tam,
                      "{\"brazo\":\"%s\",\"modo\":\"%s\",\"fuente\":\"%s\",\"diagnostico\":%s,\"articulaciones\":[",
                      NOMBRE_BRAZO, modo_app_ ? "app" : "manual", nombreFuente(fuente_), diag_ ? "true" : "false");
  for (uint8_t i = 0; i < NUM_ARTICULACIONES && n < tam; i++) {
    n += snprintf(destino + n, tam - n,
                  "%s{\"nombre\":\"%s\",\"angulo\":%.1f,\"objetivo\":%.1f,\"min\":%u,\"max\":%u}",
                  i ? "," : "", LIMITES[i].nombre, articulaciones::angulo(i),
                  articulaciones::objetivo(i), LIMITES[i].minimo, LIMITES[i].maximo);
  }
  if (n < tam) {
    n += snprintf(destino + n, tam - n, "],\"pinza_abierta\":%u,\"pinza_cerrada\":%u,\"sw_pinza\":%s}",
                  PINZA_ABIERTA, PINZA_CERRADA, entradas::pinzaAbierta() ? "true" : "false");
  }
  return n;
}

}  // namespace control
