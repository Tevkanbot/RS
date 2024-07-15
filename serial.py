import serial

class Board:
    def __init__(self, port):
        self.port = port

    def move_to(self, position):
        with serial.Serial(port, baudrate=9600) as ser:
            self.ser.write(f"m{position}".encode())

    def read(self):
        with serial.Serial(port, baudrate=9600) as ser:
            data = ser.readline().decode()
            print(data)
            return data

# Метод close() теперь не нужен, так как мы используем with блок
