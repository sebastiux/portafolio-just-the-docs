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
// 2) Pines de la tarjeta v3 (ESP32-C3 Super Mini). Iguales en los dos brazos.
//    Fuente de verdad: el esquemático de assets/brazos/electronica/kicad-v3/.
// ---------------------------------------------------------------------------
constexpr uint8_t NUM_ARTICULACIONES = 4;                         // base, hombro, codo, pinza
constexpr uint8_t PIN_SERVO[NUM_ARTICULACIONES] = {5, 6, 7, 10};  // J3, J4, J5, J6

constexpr uint8_t NUM_POTS = 3;                    // base, hombro, codo
constexpr uint8_t PIN_POT[NUM_POTS] = {1, 0, 3};   // RV1 base, RV2 hombro, RV3 codo

constexpr uint8_t PIN_SW_PINZA = 21;   // SW1, INPUT_PULLUP
constexpr uint8_t PIN_SW_MODO  = 20;   // SW2, INPUT_PULLUP: elige manual o app

// D2 verde y D3 rojo: ánodo a 3V3 por 330 Ω, cátodo al GPIO. LOW = encendido.
constexpr uint8_t PIN_LED_ESTADO = 4;  // D2
constexpr uint8_t PIN_LED_DIAG   = 2;  // D3. Pin de arranque: R6 de 10 kΩ lo sube a 1 al encender
constexpr uint8_t PIN_BOTON_DIAG = 9;  // botón BOOT del módulo, INPUT_PULLUP, LOW = presionado

// Polaridad de los switches deslizables.
// PENDIENTE: confirmar con la tarjeta real qué posición del switch es cuál.
constexpr bool MODO_APP_EN_BAJO       = true;
constexpr bool PINZA_ABIERTA_EN_BAJO  = true;

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
//    La app queda en http://192.168.4.1 y el punto de acceso no se apaga al
//    cambiar de modo, para que el celular no pierda la conexión.
// ---------------------------------------------------------------------------
constexpr const char* WIFI_CLAVE = "brazo2026";   // mínimo 8 caracteres

// ---------------------------------------------------------------------------
// 6) Entradas manuales
// ---------------------------------------------------------------------------
constexpr float POT_FILTRO_ALFA = 0.2f;            // filtro exponencial del ADC
// Cada potenciómetro tiene su propia resistencia en serie de 3.3 kΩ desde 3V3
// (R1–R3), así que su tope teórico es 3.3 V × 10 / 13.3 = 2.48 V, dentro del
// rango útil del ADC del ESP32-C3. Se usa un poco menos para llegar al 100 %.
// PENDIENTE: ajustar con la medición en la pata de R1–R3 del lado del pot.
constexpr uint16_t POT_MV_MAX = 2400;
constexpr uint16_t ANTIRREBOTE_MS = 30;            // igual para SW1, SW2 y el botón DIAG

// ---------------------------------------------------------------------------
// 7) LEDs de estado
// ---------------------------------------------------------------------------
// D2 ESTADO: fijo en manual, parpadeo lento en app sin celulares, rápido con uno.
constexpr uint32_t LED_APP_SIN_CLIENTES_MS = 500;  // medio periodo: 1 Hz
constexpr uint32_t LED_APP_CON_CLIENTES_MS = 125;  // medio periodo: 4 Hz
// D3 DIAG: fijo si el último reinicio fue por brown-out; parpadea mientras se
// presiona el botón DIAG.
constexpr uint32_t LED_DIAG_PARPADEO_MS = 125;     // medio periodo: 4 Hz

// ---------------------------------------------------------------------------
// 8) Puerto serie (USB nativo del ESP32-C3). Solo diagnóstico: el control por
//    USB se retiró, el modo lo decide SW2.
// ---------------------------------------------------------------------------
constexpr uint32_t SERIE_BAUDIOS = 115200;
constexpr uint32_t PERIODO_CONTROL_MS = 20;        // 50 Hz, igual que el PWM de los servos
