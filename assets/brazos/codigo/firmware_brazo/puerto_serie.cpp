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

void ayuda() {
  Serial.println(F("OK ordenes: J <art> <grados> | A <b> <h> <c> <p> | P A|C | H | E | ?"));
}

void ejecutar(char* l) {
  char* orden = strtok(l, " \t");
  if (!orden) return;
  const char c = toupper(static_cast<unsigned char>(orden[0]));

  if (c == 'J') {
    char* a = strtok(nullptr, " \t");
    char* g = strtok(nullptr, " \t");
    const int art = a ? articulacionPorNombre(a) : -1;
    if (!g || !control::mover(art < 0 ? 255 : art, atof(g), Fuente::SERIE)) {
      Serial.println(F("ERR uso: J <art> <grados>"));
      return;
    }
    Serial.println(F("OK"));
  } else if (c == 'A') {
    float g[NUM_ARTICULACIONES];
    for (uint8_t i = 0; i < NUM_ARTICULACIONES; i++) {
      char* t = strtok(nullptr, " \t,");
      if (!t) { Serial.println(F("ERR uso: A <b> <h> <c> <p>")); return; }
      g[i] = atof(t);
    }
    for (uint8_t i = 0; i < NUM_ARTICULACIONES; i++) control::mover(i, g[i], Fuente::SERIE);
    Serial.println(F("OK"));
  } else if (c == 'P') {
    char* t = strtok(nullptr, " \t");
    if (!t) { Serial.println(F("ERR uso: P A|C")); return; }
    control::pinza(toupper(static_cast<unsigned char>(t[0])) == 'A', Fuente::SERIE);
    Serial.println(F("OK"));
  } else if (c == 'H') {
    control::inicio(Fuente::SERIE);
    Serial.println(F("OK"));
  } else if (c == 'E') {
    char json[400];
    control::estadoJson(json, sizeof(json));
    Serial.print(F("OK "));
    Serial.println(json);
  } else if (c == '?') {
    ayuda();
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
