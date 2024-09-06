#default classes
import time
#imported classes

#custom classes
from connections.connect import Board

class Robot:
    def __init__(self):
        
        self.board = Board()

        Robot.display(mode = "logo")


    def move_to(self, position):

        self.board.write(f"m{position}") # Команда MOVE, значение устанавливаем извне

    def move_box(self, parameter):
        
        if type(parameter) == "bool" and parameter:
            self.board.write("b1") # Команда BOX команда, 1 значение
        else:
            self.board.write("b0") # Команда BOX команда, 0 значение
    
    def pay(self, cost):

        self.board.write(f"p{cost}") # Команда PAY, значение устанавливаем извне

        data = self.board.read()
        if data == "PayConfirmed":
            return True
        if data == "PayRejected":
            return False
    
    def display(self, mode, additional_parameter = None):
        if mode == "logo":
            self.board.write("d1") # Команда DISPLAY режим 1 - ЛОГО
        
        elif mode == "face":
            self.board.write("d2") # Команда DISPLAY режим 2 - ЛИЦО

        elif mode == "pay":
            self.board.write("d3") # Команда DISPLAY режим 3 - ОПЛАТА

        elif mode == "text":
            self.board.write("d4") # Команда DISPLAY режим 4 - ТЕКСТ

        

