// servidor_web.cpp — Ver servidor_web.h
#include "servidor_web.h"
#include <WiFi.h>
#include <WebServer.h>
#include "control.h"
#include "pagina_web.h"

namespace servidor_web {

namespace {
WebServer servidor(80);

void responderEstado() {
  char json[400];
  control::estadoJson(json, sizeof(json));
  servidor.send(200, "application/json", json);
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
  if (art < 0 || !control::mover(static_cast<uint8_t>(art), servidor.arg("grados").toFloat(), Fuente::WEB)) {
    servidor.send(400, "text/plain", "articulacion invalida");
    return;
  }
  responderEstado();
}

void pinza() {
  const String accion = servidor.arg("accion");
  if (accion != "abrir" && accion != "cerrar") {
    servidor.send(400, "text/plain", "accion debe ser abrir o cerrar");
    return;
  }
  control::pinza(accion == "abrir", Fuente::WEB);
  responderEstado();
}

void inicio() {
  control::inicio(Fuente::WEB);
  responderEstado();
}
}  // namespace

void iniciar() {
  WiFi.mode(WIFI_AP);
  WiFi.softAP(WIFI_SSID, WIFI_CLAVE);
  servidor.on("/", HTTP_GET, paginaPrincipal);
  servidor.on("/api/estado", HTTP_GET, responderEstado);
  servidor.on("/api/mover", HTTP_GET, mover);
  servidor.on("/api/pinza", HTTP_GET, pinza);
  servidor.on("/api/inicio", HTTP_GET, inicio);
  servidor.onNotFound([] { servidor.send(404, "text/plain", "no encontrado"); });
  servidor.begin();
}

void atender() {
  servidor.handleClient();
}

}  // namespace servidor_web
