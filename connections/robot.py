#default classes
import time
#imported classes

#custom classes
from connections.connect import Board

class Robot:
    def __init__(self):

        self.board = Board()



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