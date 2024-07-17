#python classes
import serial

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
            raise ConnectionError("Arduino is not conected")
        
        return arduino_port
    
    def __init__(self):

        self.port = Board.find_arduino_uno()

    def read(self):

        with serial.Serial(self.port, baudrate=9600) as ser:
            data = ser.readline().decode()
            return data
    
    def write(self, data):

        with serial.Serial(self.port, baudrate=9600) as ser:
            ser.write(data.encode())
    
    class Do:
            
        def move_to(self, position):

            Board.write(f"m{position}")