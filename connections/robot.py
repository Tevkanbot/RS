from .connect import Board
import asyncio
import time
class Robot:
    def __init__(self):
        
        self.board = Board()
        self.display_status = "logo"


    def move_to(self, position):
        write = f"m{position}"
        if position == 0:
            self.board.write("m0") # Команда MOVE, значение устанавливаем извне
        else:
            self.board.write("m1") # Команда MOVE, значение устанавливаем извне



        #done_text = self.board.read()

        time.sleep(1)


        


    def move_box(self, parameter):
        
        if parameter:
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
            self.board.write("dlogo") # Команда DISPLAY режим 1 - ЛОГО
            self.display_status = "logo"
        
        elif mode == "face":
            self.board.write("dface") # Команда DISPLAY режим 2 - ЛИЦО
            self.display_status = "face"
            

        elif mode == "pay":
            self.board.write("dpayy") # Команда DISPLAY режим 3 - ОПЛАТА
            self.display_status = "payy"

        elif mode == "pays":
            self.board.write(f"dpays{additional_parameter}") # Команда DISPLAY режим 4 - Оплата
            self.display_status = "pays"

        elif mode == "shop":
            if additional_parameter:
                if self.display_status != "shop":
                    self.board.write(f"dshop")
                    time.sleep(1)
                self.board.write(f"dshop{additional_parameter}")
            else:
                self.board.write("dshop")
                self.display_status = "shop"

    def write (self, param):
        self.board.write(param)



        
        
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