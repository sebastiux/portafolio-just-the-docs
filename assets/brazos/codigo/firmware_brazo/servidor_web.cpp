// servidor_web.cpp — Ver servidor_web.h
#include "servidor_web.h"
#include <WiFi.h>
#include <WebServer.h>
#include "control.h"
#include "pagina_web.h"

namespace servidor_web {

namespace {
WebServer servidor(80);
bool activo_ = false;

void responderEstado() {
  char json[460];
  control::estadoJson(json, sizeof(json));
  servidor.send(200, "application/json", json);
}

// 200 con el estado si la orden se aceptó; si no, el motivo en texto.
void responder(Resultado r) {
  if (r == Resultado::ACEPTADA) {
    responderEstado();
    return;
  }
  const int codigo = (r == Resultado::INVALIDA) ? 400 : 409;
  servidor.send(codigo, "text/plain; charset=utf-8", control::textoResultado(r) + 4);   // sin "ERR "
}

void paginaPrincipal() {
  servidor.send_P(200, "text/html; charset=utf-8", PAGINA_WEB);
}

void mover() {
  if (!servidor.hasArg("art") || !servidor.hasArg("grados")) {
    servidor.send(400, "text/plain", "faltan art y grados");
    return;
  }
  const long art = servidor.arg("art").toInt();
  if (art < 0 || art >= NUM_ARTICULACIONES) {
    responder(Resultado::INVALIDA);
    return;
  }
  responder(control::mover(static_cast<uint8_t>(art), servidor.arg("grados").toFloat(), Fuente::WEB));
}

void pinza() {
  const String accion = servidor.arg("accion");
  if (accion != "abrir" && accion != "cerrar") {
    servidor.send(400, "text/plain", "accion debe ser abrir o cerrar");
    return;
  }
  responder(control::pinza(accion == "abrir", Fuente::WEB));
}

void inicio() { responder(control::inicio(Fuente::WEB)); }

void diagnostico() {
  control::diagnostico();
  responderEstado();
}
}  // namespace

void iniciar() {
  WiFi.mode(WIFI_AP);
  activo_ = WiFi.softAP(WIFI_SSID, WIFI_CLAVE);
  servidor.on("/", HTTP_GET, paginaPrincipal);
  servidor.on("/api/estado", HTTP_GET, responderEstado);
  servidor.on("/api/mover", HTTP_GET, mover);
  servidor.on("/api/pinza", HTTP_GET, pinza);
  servidor.on("/api/inicio", HTTP_GET, inicio);
  servidor.on("/api/diagnostico", HTTP_GET, diagnostico);
  servidor.onNotFound([] { servidor.send(404, "text/plain", "no encontrado"); });
  servidor.begin();
}

void atender() {
  servidor.handleClient();
}

bool activo() { return activo_; }

}  // namespace servidor_web
