#python classes
import serial.tools.list_ports
#imported classes
#custom classes

class Board:

    def find_arduino_uno():
        ports = list(serial.tools.list_ports.comports())
        arduino_port = None

        for port in ports:
            if "Arduino Uno" in port.description or "VID:PID=2341:0043" in port.hwid:
                arduino_port = port.device
        
        if arduino_port == None:
            print ("Arduino is not conected")
        
        return arduino_port
    
    def __init__(self):

        self.port = Board.find_arduino_uno()

    def read(self):

        with serial.Serial(self.port, baudrate=9600, dsrdtr=True) as ser:
            ser.dtr = False
            data = ser.readline()
            return data.decode(encoding="utf-8").strip()
    
    def write(self, data):

        with serial.Serial(self.port, baudrate=9600, dsrdtr=True) as ser:
            ser.dtr = False
            ser.write(data.encode())

if __name__ == "__main__":
    board = Board()
    board.write("m1")
    
