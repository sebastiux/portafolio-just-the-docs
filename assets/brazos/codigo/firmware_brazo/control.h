// control.h — Aplica las órdenes al brazo según el modo que marca el switch SW2.
//
// Dos modos, y los elige el hardware, no el programa:
//   MANUAL : mandan los potenciómetros (base, hombro, codo) y SW1 (pinza).
//            Las órdenes de la app se rechazan con Resultado::MODO_MANUAL,
//            que el servidor traduce a HTTP 409.
//   APP    : manda solo la app servida en http://192.168.4.1. Los
//            potenciómetros y SW1 se ignoran.
//
// No hay arbitraje automático: el modo es exactamente lo que dice SW2 en cada
// ciclo. Al pasar de APP a MANUAL los objetivos vuelven a la posición de los
// pots y el límite de VELOCIDAD_MAX_GRADOS_S evita el salto brusco; al pasar de
// MANUAL a APP los objetivos se quedan donde están.
#pragma once
#include "config.h"

enum class Modo : uint8_t { MANUAL, APP };

enum class Resultado : uint8_t {
  OK,
  MODO_MANUAL,            // la app pidió algo con SW2 en manual → HTTP 409
  ARTICULACION_INVALIDA,  // → HTTP 400
};

namespace control {

void iniciar();
void ciclo(float dt_s);                     // lee entradas, aplica el modo y mueve servos

Resultado mover(uint8_t art, float grados); // órdenes de la app
Resultado pinza(bool abrir);
Resultado inicio();

Modo modo();
const char* nombreModo(Modo m);

// Traducción de Resultado a respuesta HTTP. Vive aquí, y no en las rutas del
// servidor, para poder probarla con g++ sin levantar el Wi-Fi.
uint16_t codigoHttp(Resultado r);
const char* cuerpoJson(Resultado r);

// Estado completo en JSON. `clientes` y `diag` los aportan quien los conoce:
// el servidor web cuenta los celulares conectados y el módulo de diagnóstico
// sabe si hubo un reinicio por brown-out.
size_t estadoJson(char* destino, size_t tam, uint8_t clientes, bool diag);

}  // namespace control
