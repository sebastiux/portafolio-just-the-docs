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
// 2) Pines de la tarjeta (ESP32-C3 Super Mini). Iguales en los dos brazos.
//    Se evitan GPIO2, GPIO8 y GPIO9 (pines de arranque) para entradas y servos.
// ---------------------------------------------------------------------------
constexpr uint8_t NUM_ARTICULACIONES = 4;          // base, hombro, codo, pinza
constexpr uint8_t PIN_SERVO[NUM_ARTICULACIONES] = {4, 5, 6, 7};

constexpr uint8_t NUM_POTS = 3;                    // base, hombro, codo
constexpr uint8_t PIN_POT[NUM_POTS] = {0, 1, 3};   // ADC1_CH0, ADC1_CH1, ADC1_CH3

constexpr uint8_t PIN_INTERRUPTOR = 10;            // a GND, con pull-up interno
constexpr uint8_t PIN_LED = 8;                     // LED azul de la placa, activo en bajo

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
// En la tarjeta, R2 (1 kΩ) alimenta los 3 potenciómetros desde 3.3 V, así que
// su tope queda en ≈2.54 V: dentro del rango útil del ADC del ESP32-C3 con la
// atenuación por defecto (0–2500 mV). Se usa un poco menos para llegar al 100 %.
constexpr uint16_t POT_MV_MAX = 2450;
constexpr uint8_t  UMBRAL_TOMA_MANUAL_GRADOS = 4;  // giro de pot que devuelve el mando al manual
constexpr uint16_t ANTIRREBOTE_MS = 30;

// ---------------------------------------------------------------------------
// 7) Puerto serie (USB nativo del ESP32-C3)
// ---------------------------------------------------------------------------
constexpr uint32_t SERIE_BAUDIOS = 115200;
constexpr uint32_t PERIODO_CONTROL_MS = 20;        // 50 Hz, igual que el PWM de los servos
