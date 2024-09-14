from .connect import Board
import asyncio
import time
class Robot:
    def __init__(self):
        
        self.board = Board()

        Robot.display(mode = "logo")


    async def move_to(self, position):
        write = f"m{position}"

        self.board.write(write) # Команда MOVE, значение устанавливаем извне

        readed = self.board.read() # Ожидаем ответ от платы

        if readed == "Done":
            return True
        
        else: 
            raise (Exception("Плата какую-то шляпу ответила"))

    async def move_box(self, parameter):
        
        if type(parameter) == "bool" and parameter:
            self.board.write("b1") # Команда BOX команда, 1 значение
        else:
            self.board.write("b0") # Команда BOX команда, 0 значение
    
    async def pay(self, cost):

        self.board.write(f"p{cost}") # Команда PAY, значение устанавливаем извне

        data = self.board.read()
        if data == "PayConfirmed":
            return True
        if data == "PayRejected":
            return False
        

    async def display(self, mode, additional_parameter = None):
        if mode == "logo":
            self.board.write("dlogo") # Команда DISPLAY режим 1 - ЛОГО
        
        elif mode == "face":
            self.board.write("dface") # Команда DISPLAY режим 2 - ЛИЦО

        elif mode == "pay":
            self.board.write("d3") # Команда DISPLAY режим 3 - ОПЛАТА

        elif mode == "text":
            self.board.write("d4") # Команда DISPLAY режим 4 - ТЕКСТ

        
        
    class Queue:
        def __init__(self):
            self.queue = []

        def add(self, seat): # Добовляем пасажра в конец очереди
            self.queue.append(seat)


        def get_first(self):
            try:
                return self.queue.pop(0) # Удаляем первого пасажира из очереди
            
            except IndexError:
                return None
            
        def debug(self):
            print(self.queue)