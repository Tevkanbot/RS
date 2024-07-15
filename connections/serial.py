#default classes
import serial as sr

#imported classes

#custom classes
class Board:
    def __init__(self, port):
        self.port = port

    def read(self):
        with sr.Serial(port, baudrate=9600) as ser:
            data = ser.readline().decode()
            print(data)
            return data
    
    def write(self, data):
        with sr.Serial(port, baudrate=9600) as ser:
            ser.write(data.encode())
    
    class Do:
            
            def move_to(self, position):
                Board.write(f"m{position}")
