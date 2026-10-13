// config.h — Configuración del brazo: pines, límites y parámetros de cada versión.
//
// El mismo firmware y la misma tarjeta controlan los dos brazos. Solo cambia
// esta sección: elegir el brazo con BRAZO antes de compilar.
#pragma once
#include <Arduino.h>

// ---------------------------------------------------------------------------
// 1) Brazo que se compila
// ---------------------------------------------------------------------------
#define BRAZO_IMPRESO 1
#define BRAZO_LASER   2

#ifndef BRAZO
#define BRAZO BRAZO_IMPRESO   // cambiar a BRAZO_LASER para el MeArm de MDF
#endif

// ---------------------------------------------------------------------------
// 2) Pines de la tarjeta brazo_control v3 (ESP32-C3 Super Mini en zócalo).
//    Iguales en los dos brazos. Ver brazo_control_pcb/LEEME.md.
// ---------------------------------------------------------------------------
constexpr uint8_t NUM_ARTICULACIONES = 4;          // base, hombro, codo, pinza
constexpr uint8_t PIN_SERVO[NUM_ARTICULACIONES] = {5, 6, 7, 10};   // J3, J4, J5, J6

constexpr uint8_t NUM_POTS = 3;                    // base, hombro, codo
constexpr uint8_t PIN_POT[NUM_POTS] = {1, 0, 3};   // RV1 IO1 (ADC1_CH1), RV2 IO0 (ADC1_CH0), RV3 IO3 (ADC1_CH3)

constexpr uint8_t PIN_SW_PINZA = 21;               // SW1: común a IO21, otro extremo a GND
constexpr uint8_t PIN_SW_MODO  = 20;               // SW2: común a IO20, otro extremo a GND
constexpr uint8_t PIN_BOTON_DIAG = 9;              // botón BOOT del módulo; se lee después del arranque

constexpr uint8_t PIN_LED_ESTADO = 4;              // D2 verde, activo en bajo
constexpr uint8_t PIN_LED_DIAG   = 2;              // D3 rojo, activo en bajo (pull-up R6 de arranque)

// Posición de SW2 que activa el modo App (app web y USB). Si en tu tarjeta
// queda al revés, cambia LOW por HIGH.
constexpr int NIVEL_MODO_APP = LOW;
// Posición de SW1 que abre la pinza.
constexpr int NIVEL_PINZA_ABIERTA = LOW;

// ---------------------------------------------------------------------------
// 3) Servos SG90
// ---------------------------------------------------------------------------
constexpr uint32_t SERVO_FRECUENCIA_HZ = 50;
constexpr uint8_t  SERVO_RESOLUCION_BITS = 14;     // máximo del LEDC del ESP32-C3
constexpr uint16_t SERVO_PULSO_MIN_US = 500;       // 0°
constexpr uint16_t SERVO_PULSO_MAX_US = 2400;      // 180°
constexpr float    VELOCIDAD_MAX_GRADOS_S = 120.0f; // limita picos de corriente

// ---------------------------------------------------------------------------
// 4) Límites por brazo (grados de servo). Valores iniciales de diseño:
//    se ajustan en la calibración con el brazo armado (ver la documentación).
// ---------------------------------------------------------------------------
struct LimitesArticulacion {
  const char* nombre;
  uint8_t minimo;
  uint8_t maximo;
  uint8_t inicio;
};

#if BRAZO == BRAZO_IMPRESO
constexpr const char* NOMBRE_BRAZO = "impreso";
constexpr const char* WIFI_SSID    = "Brazo-Impreso";
constexpr LimitesArticulacion LIMITES[NUM_ARTICULACIONES] = {
  {"base",   0,   180, 90},
  {"hombro", 30,  150, 90},
  {"codo",   20,  160, 90},
  {"pinza",  30,  100, 100},
};
constexpr uint8_t PINZA_ABIERTA = 100;
constexpr uint8_t PINZA_CERRADA = 30;
#elif BRAZO == BRAZO_LASER
constexpr const char* NOMBRE_BRAZO = "laser";
constexpr const char* WIFI_SSID    = "Brazo-Laser";
constexpr LimitesArticulacion LIMITES[NUM_ARTICULACIONES] = {
  {"base",   0,   180, 90},
  {"hombro", 40,  140, 90},
  {"codo",   40,  140, 90},
  {"pinza",  20,  80,  80},
};
constexpr uint8_t PINZA_ABIERTA = 80;
constexpr uint8_t PINZA_CERRADA = 20;
#else
#error "BRAZO debe ser BRAZO_IMPRESO o BRAZO_LASER"
#endif

constexpr uint8_t ART_PINZA = 3;

// ---------------------------------------------------------------------------
// 5) Red inalámbrica: el ESP32-C3 crea su propia red (punto de acceso).
//    La app queda en http://192.168.4.1
// ---------------------------------------------------------------------------
constexpr const char* WIFI_CLAVE = "brazo2026";   // mínimo 8 caracteres

// ---------------------------------------------------------------------------
// 6) Entradas manuales
// ---------------------------------------------------------------------------
constexpr float    POT_FILTRO_ALFA = 0.2f;         // filtro exponencial del ADC
// En la tarjeta, R1–R3 (3.3 kΩ) en serie con cada potenciómetro de 10 kΩ bajan
// su tope a 3.3 V × 10 / 13.3 ≈ 2.48 V: dentro del rango útil del ADC del
// ESP32-C3 con la atenuación por defecto (0–2500 mV). Se usa un poco menos
// para que el giro completo llegue al 100 %.
constexpr uint16_t POT_MV_MAX = 2450;
constexpr uint16_t ANTIRREBOTE_MS = 30;

// Secuencia de diagnóstico (botón BOOT): cada articulación va a su mínimo, a
// su máximo y a su inicio, una por una.
constexpr uint16_t DIAG_PASO_MS = 1000;

// ---------------------------------------------------------------------------
// 7) Puerto serie (USB nativo del ESP32-C3)
// ---------------------------------------------------------------------------
constexpr uint32_t SERIE_BAUDIOS = 115200;
constexpr uint32_t PERIODO_CONTROL_MS = 20;        // 50 Hz, igual que el PWM de los servos
