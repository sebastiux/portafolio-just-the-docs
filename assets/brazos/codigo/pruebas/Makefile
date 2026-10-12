# Pruebas del firmware en la computadora (g++). Corre las de los dos brazos.
FW   = ../firmware_brazo
SRC  = prueba_firmware.cpp stub/sim.cpp $(FW)/articulaciones.cpp $(FW)/control.cpp $(FW)/entradas.cpp $(FW)/puerto_serie.cpp
OPTS = -std=c++17 -Wall -Wextra -Istub -I$(FW)

pruebas: prueba_impreso prueba_laser
	./prueba_impreso
	./prueba_laser

prueba_impreso: $(SRC) $(FW)/*.h
	g++ $(OPTS) -DBRAZO=BRAZO_IMPRESO $(SRC) -o $@

prueba_laser: $(SRC) $(FW)/*.h
	g++ $(OPTS) -DBRAZO=BRAZO_LASER $(SRC) -o $@

# El target 'simulador' se retiró junto con simulador.cpp: existía para
# brazo_gui.py, que ya no es un modo de mando. Está en assets/brazos/archivo/.

clean:
	rm -f prueba_impreso prueba_laser
