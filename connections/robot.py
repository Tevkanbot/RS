from connect import Board
import asyncio
import time
class Robot:
    def __init__(self):
        
        self.board = Board("Robot")
        self.display_status = "logo"

    def get_dist(self):
        self.board.write("u")
        recieved = self.board.read().split()
        print(recieved)
        if recieved[1] < 10 or recieved[0] < 10:
            return False
        return True


    def move_to(self, position, reverse=None):
        position = int(position)
        if reverse:
            for i in range(position):
                self.board.write("u")
                recieved = self.board.read().split()
                recieved[0] = int(recieved[0])
                recieved[1] = int(recieved[1])
                print(recieved)
                if recieved[0] < 10:
                    raise Exception("ПРЕПЯТСТВИЕ")
                self.board.write("m1")
                time.sleep(1)
        else:
            for i in range(position):
                self.board.write("u")
                recieved = self.board.read().split()
                recieved[0] = int(recieved[0])
                recieved[1] = int(recieved[1])
                print(recieved)
                if recieved[1] < 10:
                    raise Exception("ПРЕПЯТСТВИЕ")
                self.board.write("m0")
                time.sleep(1)
        
        # Убираем эту строку:
        # self.board.write = f"m{position}"
        self.board.write(f"m{position}")  # Передаём команду напрямую
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
                    self.board.write("dshop")
                    time.sleep(1)
                self.board.write(f"dshop{additional_parameter}")
            else:
                self.board.write("dshop")
                self.display_status = "shop"

    def write (self, param):
        self.board.write(param)



        
        
class Queue:
    def __init__(self):
        self.board = Board("Buttons")
        self.queue = []

    def update(self): # Добовляем пасажра в конец очереди
        self.board.write("g")
        received_text = self.board.read()
        
        self.queue = received_text.split()
        print(self.queue)


    def get_first(self):
        try:
            first = self.queue.pop(0) # Удаляем первого пасажира из очереди
            self.board.write(first)
            return first
        
        except IndexError:
            return None
        
    def debug(self):
        print(self.queue)


if __name__ == "__main__":
    queue = Queue()
    robot = Robot()
    while True:
        
        robot.move_to(2)
        robot.move_to(2, True)

    