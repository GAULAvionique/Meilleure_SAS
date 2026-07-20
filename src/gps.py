import pynmea2 #utiliser pour convertir la phrase NMEA que donne le GPS en objets 
import serial 

#Pour faire la connection avec les pins UART , baudrate de base du Neo 6M
seri = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=0.5)

data_line = seri.readline().decode('ascii').strip()

while True:
    try:
        if data_line[0:6] == "$GPRMC":
            data = pynmea2.parse(data_line)
            lat = data.latitude
            long = data.longitude
    except Exception as e:
        print(f"Erreur: {e}")


