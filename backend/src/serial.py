import serial
import threading
import queue
import time

class mySerial: 
    #classe grandement inspiré de ThreadedSerialReader (https://www.pyserial.com/docs/reading-data#threaded-reading).
    def __init__(self, ser, queue_size=1000):
        self.ser = ser
        self.data_queue = queue.Queue(maxsize=queue_size)
        self.running = True
        self.thread = None
    
    def start(self):
        """Start background reading thread"""
        self.thread = threading.Thread(target=self._read_loop)
        self.thread.daemon = True
        self.thread.start()
    
    def _read_loop(self):
        """Background reading loop"""
        while self.running:
            try:
                # écrire ici la solution:
                # 1. Accumuler les données dans un buffer
                # 2. Chercher symbol de départ
                # 3. Enregistrer les x prochains caractères
                # 4. Valider la trame
                # 5. Mettre dans objet queue

                """ if self.ser.in_waiting:
                    data = self.ser.read(self.ser.in_waiting)
                    if data:
                        try:
                            self.data_queue.put(data, timeout=0.1)
                        except queue.Full:
                            print("⚠️  Queue full, dropping data")
                else:
                    time.sleep(0.001)  # Small delay when no data """
            except Exception as e:
                if self.running:
                    print(f"Read thread error: {e}")
    
    def get_data(self, timeout=0.1):
        """Get data from queue"""
        try:
            return self.data_queue.get(timeout=timeout)
        except queue.Empty:
            return None
    
    def get_all_data(self):
        """Get all queued data"""
        data = []
        while not self.data_queue.empty():
            try:
                data.append(self.data_queue.get_nowait())
            except queue.Empty:
                break
        return b''.join(data)
    
    def stop(self):
        """Stop reading thread"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)

# Usage
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
reader = mySerial(ser)
reader.start()

try:
    while True:
        data = reader.get_data(timeout=1)
        if data:
            print(f"Got {len(data)} bytes")
        else:
            print("No data received")
        time.sleep(0.1)
finally:
    reader.stop()