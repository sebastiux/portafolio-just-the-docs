#include "Arduino.h"
namespace sim {
uint32_t tiempo_ms = 0;
int pin_digital[32] = {};
uint32_t mv_adc[32] = {};
uint32_t duty[32] = {};
std::string entrada_serie;
std::string salida_serie;
esp_reset_reason_t razon_reinicio = ESP_RST_POWERON;
}
SerieSimulada Serial;
