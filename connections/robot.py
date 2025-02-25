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

  git config --global user.email "Tevkanbot@yandex.ru"
  git config --global user.name "Ivan"
    def move_to(self, position, reverse=None):
        position = int(position)
        self.board.write(f"m{position}")  # Передаём команду напрямую

    def move_box(self, parameter):
        
        if parameter:
            self.board.write("b1") # Команда BOX команда, 1 значение
        else:
            self.board.write("b0") # Команда BOX команда, 0 значение

    def write (self, param):
        self.board.write(param)


class Queue:
    def __init__(self):
        self.board = Board("Buttons")
        self.queue = []

    def update(self): # Добовляем пасажра в конец очереди
        self.board.write("q")
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

    