// servidor_web.cpp — Ver servidor_web.h
#include "servidor_web.h"
#include <WiFi.h>
#include <WebServer.h>
#include "control.h"
#include "diagnostico.h"
#include "pagina_web.h"

namespace servidor_web {

namespace {
WebServer servidor(80);

void responderEstado() {
  char json[400];
  control::estadoJson(json, sizeof(json), clientes(), diagnostico::alerta());
  servidor.send(200, "application/json", json);
}

// Toda orden pasa por aquí: control::codigoHttp decide si fue 200, 409 o 400.
void responder(Resultado r) {
  if (r == Resultado::OK) {
    responderEstado();
    return;
  }
  servidor.send(control::codigoHttp(r), "application/json", control::cuerpoJson(r));
}

void paginaPrincipal() {
  servidor.send_P(200, "text/html; charset=utf-8", PAGINA_WEB);
}

void mover() {
  if (!servidor.hasArg("art") || !servidor.hasArg("grados")) {
    servidor.send(400, "application/json", "{\"error\":\"faltan art y grados\"}");
    return;
  }
  const long art = servidor.arg("art").toInt();
  responder(control::mover(art < 0 ? 255 : static_cast<uint8_t>(art),
                           servidor.arg("grados").toFloat()));
}

void pinza() {
  const String accion = servidor.arg("accion");
  if (accion != "abrir" && accion != "cerrar") {
    servidor.send(400, "application/json", "{\"error\":\"accion debe ser abrir o cerrar\"}");
    return;
  }
  responder(control::pinza(accion == "abrir"));
}

void inicio() {
  responder(control::inicio());
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

uint8_t clientes() {
  return WiFi.softAPgetStationNum();
}

}  // namespace servidor_web
