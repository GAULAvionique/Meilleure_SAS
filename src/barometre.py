import time
import board
import adafruit_bmp280

i2c = board.I2C() #Connecter avec les 2 pins GPIO2 et GPIO3 (SDA et SCL) du raspberry pi 
bmp = adafruit_bmp280.Adafruit_BMP280_I2C(i2c) #

while True: 
    try:
        print(f"Temperature {bmp.temperature}")
        print(f"Pression {bmp.pressure}")
    except Exception as e:
        print(f"Erreur : {e}")