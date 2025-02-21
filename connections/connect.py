import serial.tools.list_ports
import time
class Board:
    
    @staticmethod
    def find_arduino(board_type=None):
        ports = list(serial.tools.list_ports.comports())
        arduino_ports = []

        # Поиск всех доступных Arduino
        for port in ports:
            if "Arduino" in port.description:
                arduino_ports.append(port.device)
        
        if not arduino_ports:
            print("No Arduino connected")
            return None

        # Считываем ответ от каждой платы, чтобы понять, что это за плата
        for port in arduino_ports:
            with serial.Serial(port, baudrate=9600, timeout=2) as ser:
                #ser.write(b"Identify")  # Отправка команды для идентификации
                response = ser.readline().decode('utf-8').strip()
                if response == board_type:
                    print(f"Found {board_type} at {port}")
                    return port
        print(f"{board_type} not found.")
        return None

    def __init__(self, board_type):
        self.port = Board.find_arduino(board_type)
        if self.port is None:
            raise Exception(f"{board_type} not found.")

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
    ro = Board("Robot")
    time.sleep(3)
    ro.write("u")

    print(ro.read())
