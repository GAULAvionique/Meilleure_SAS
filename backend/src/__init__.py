import serial


port = serial.Serial(
    port='/dev/ttys022',
    baudrate=9600,
    timeout=2
)

port.write(b'HxWeTa$aP)5Bc$*')
print('data envoyés')