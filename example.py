import board
import busio
from time import sleep
import adafruit_bus_device.i2c_device as i2c_device

i2cBus = busio.I2C(board.SCL, board.SDA)
module = i2c_device.I2CDevice(i2cBus, 0x70)

for octet in [1,2,4,8,16,32,64,128]:
    module.write(bytes([0])) # Spécifier l'adresse qui sera utilisée
    module.write(bytes([0,octet])) # Écrire les données à l'adresse
    sleep(1)
    module.write(bytes([0,0])) # Écrire les données (vides) à l'adresse