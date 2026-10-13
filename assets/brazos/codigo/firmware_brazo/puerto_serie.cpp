// puerto_serie.cpp — Ver puerto_serie.h
#include "puerto_serie.h"
#include "control.h"
#include "diagnostico.h"

namespace puerto_serie {

namespace {
char linea_[64];
size_t largo_ = 0;

void ayuda() {
  Serial.println(F("OK ordenes: E (estado) | D (diagnostico) | ? (ayuda)"));
  Serial.println(F("OK el brazo se mueve con los potenciometros o con la app; el USB no manda"));
}

void ejecutar(char* l, uint8_t clientes) {
  char* orden = strtok(l, " \t");
  if (!orden) return;
  const char c = toupper(static_cast<unsigned char>(orden[0]));

  if (c == 'E') {
    char json[400];
    control::estadoJson(json, sizeof(json), clientes, diagnostico::alerta());
    Serial.print(F("OK "));
    Serial.println(json);
  } else if (c == 'D') {
    diagnostico::reporte(clientes);
  } else if (c == '?') {
    ayuda();
  } else if (c == 'J' || c == 'A' || c == 'P' || c == 'H') {
    // Protocolo viejo de brazo_gui.py: se conserva el mensaje para que quede
    // claro por qué dejó de funcionar.
    Serial.println(F("ERR control por USB deshabilitado"));
  } else {
    Serial.println(F("ERR orden desconocida, envia ? para ayuda"));
  }
}
}  // namespace

void iniciar() {
  Serial.begin(SERIE_BAUDIOS);
}

void atender(uint8_t clientes) {
  while (Serial.available()) {
    const char ch = Serial.read();
    if (ch == '\r') continue;
    if (ch == '\n') {
      linea_[largo_] = '\0';
      ejecutar(linea_, clientes);
      largo_ = 0;
    } else if (largo_ < sizeof(linea_) - 1) {
      linea_[largo_++] = ch;
    }
  }
}

}  // namespace puerto_serie
