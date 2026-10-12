// simulador.cpp — Corre el firmware en la computadora detrás de un puerto serie virtual.
//
// Sirve para probar brazo_gui.py sin el brazo: el simulador imprime el nombre
// del puerto (por ejemplo /dev/pts/3) y la GUI se conecta a él como si fuera
// el ESP32-C3. Solo Linux y macOS.
//
// Uso:  make simulador && ./simulador
#include <fcntl.h>
#include <unistd.h>
#include <termios.h>
#include <iostream>
#include "Arduino.h"
#include "../firmware_brazo/config.h"
#include "../firmware_brazo/control.h"
#include "../firmware_brazo/puerto_serie.h"

int main() {
  const int maestro = posix_openpt(O_RDWR | O_NOCTTY);
  if (maestro < 0 || grantpt(maestro) || unlockpt(maestro)) { perror("pty"); return 1; }
  termios t{};
  tcgetattr(maestro, &t);
  cfmakeraw(&t);
  tcsetattr(maestro, TCSANOW, &t);
  fcntl(maestro, F_SETFL, O_NONBLOCK);
  std::cout << "Brazo " << NOMBRE_BRAZO << " simulado en " << ptsname(maestro) << std::endl;

  sim::pin_digital[PIN_INTERRUPTOR] = HIGH;
  for (uint8_t i = 0; i < NUM_POTS; i++) sim::mv_adc[PIN_POT[i]] = POT_MV_MAX / 2;
  puerto_serie::iniciar();
  control::iniciar();

  char buf[256];
  for (;;) {
    const ssize_t n = read(maestro, buf, sizeof(buf));
    if (n > 0) sim::entrada_serie.append(buf, n);
    puerto_serie::atender();
    control::ciclo(PERIODO_CONTROL_MS / 1000.0f);
    if (!sim::salida_serie.empty()) {
      if (write(maestro, sim::salida_serie.data(), sim::salida_serie.size()) > 0) sim::salida_serie.clear();
    }
    usleep(PERIODO_CONTROL_MS * 1000);
    sim::tiempo_ms += PERIODO_CONTROL_MS;
  }
}
