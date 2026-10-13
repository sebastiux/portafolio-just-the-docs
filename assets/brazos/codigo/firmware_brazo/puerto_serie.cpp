// puerto_serie.cpp — Ver puerto_serie.h
#include "puerto_serie.h"
#include "control.h"

namespace puerto_serie {

namespace {
char linea_[64];
size_t largo_ = 0;

int articulacionPorNombre(const char* t) {
  if (isdigit(static_cast<unsigned char>(t[0]))) return atoi(t);
  for (uint8_t i = 0; i < NUM_ARTICULACIONES; i++) {
    if (strcasecmp(t, LIMITES[i].nombre) == 0) return i;
  }
  return -1;
}

void responder(Resultado r) {
  Serial.println(control::textoResultado(r));
}

void ejecutar(char* l) {
  char* orden = strtok(l, " \t");
  if (!orden) return;
  const char c = toupper(static_cast<unsigned char>(orden[0]));

  if (c == 'J') {
    char* a = strtok(nullptr, " \t");
    char* g = strtok(nullptr, " \t");
    const int art = a ? articulacionPorNombre(a) : -1;
    if (!g || art < 0) {
      Serial.println(F("ERR uso: J <art> <grados>"));
      return;
    }
    responder(control::mover(static_cast<uint8_t>(art), atof(g), Fuente::SERIE));
  } else if (c == 'A') {
    float g[NUM_ARTICULACIONES];
    for (uint8_t i = 0; i < NUM_ARTICULACIONES; i++) {
      char* t = strtok(nullptr, " \t,");
      if (!t) { Serial.println(F("ERR uso: A <b> <h> <c> <p>")); return; }
      g[i] = atof(t);
    }
    Resultado r = Resultado::ACEPTADA;
    for (uint8_t i = 0; i < NUM_ARTICULACIONES && r == Resultado::ACEPTADA; i++) {
      r = control::mover(i, g[i], Fuente::SERIE);
    }
    responder(r);
  } else if (c == 'P') {
    char* t = strtok(nullptr, " \t");
    if (!t) { Serial.println(F("ERR uso: P A|C")); return; }
    responder(control::pinza(toupper(static_cast<unsigned char>(t[0])) == 'A', Fuente::SERIE));
  } else if (c == 'H') {
    responder(control::inicio(Fuente::SERIE));
  } else if (c == 'D') {
    control::diagnostico();
    Serial.println(F("OK"));
  } else if (c == 'E') {
    char json[460];
    control::estadoJson(json, sizeof(json));
    Serial.print(F("OK "));
    Serial.println(json);
  } else if (c == '?') {
    Serial.println(F("OK ordenes: J <art> <grados> | A <b> <h> <c> <p> | P A|C | H | D | E | ?"));
  } else {
    Serial.println(F("ERR orden desconocida, envia ? para ayuda"));
  }
}
}  // namespace

void iniciar() {
  Serial.begin(SERIE_BAUDIOS);
}

void atender() {
  while (Serial.available()) {
    const char ch = Serial.read();
    if (ch == '\r') continue;
    if (ch == '\n') {
      linea_[largo_] = '\0';
      ejecutar(linea_);
      largo_ = 0;
    } else if (largo_ < sizeof(linea_) - 1) {
      linea_[largo_++] = ch;
    }
  }
}

}  // namespace puerto_serie
