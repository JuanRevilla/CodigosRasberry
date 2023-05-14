import smbus

# Definir las direcciones de los dispositivos esclavos
direccion_dispositivo_1 = 0x12
direccion_dispositivo_2 = 0x34

# Crear una instancia del bus I2C
bus = smbus.SMBus(0)  # El número indica qué bus I2C se está utilizando (0 o 1)

# Enviar el primer entero al primer dispositivo
def mandaAngulo(Ax,Ay):
    bus.write_byte(direccion_dispositivo_1, Ax)
# Enviar el segundo entero al segundo dispositivo
    bus.write_byte(direccion_dispositivo_2, Ay)