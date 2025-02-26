from connect import Board
import asyncio
import time
import requests


class Robot:
    def __init__(self):

        self.board = Board("Robot")

    def move_to(self, position):
        position = int(position)
        self.board.write(f"m{position}")  # Передаём команду напрямую

        while True:

            recieved = self.board.read()
            if recieved == "done":
                break
            else:
                print("Получена неверная информация: ", recieved)

        return True

    def move_box(self, parameter):

        if parameter:
            self.board.write("b1")  # Команда BOX команда, 1 значение
            while True:
                recieved = self.board.read()
                if recieved == "done":
                    break
                else:
                    print("Получена неверная информация: ", recieved)

        else:
            self.board.write("b0")  # Команда BOX команда, 0 значение
            while True:

                recieved = self.board.read()
                if recieved == "done":
                    break
                else:
                    print("Получена неверная информация: ", recieved)

    def start_shopping(self):
        self.board.write("dshop")

    def write(self, param):
        self.board.write(param)


class Queue:
    def __init__(self):
        self.board = Board("Buttons")
        self.queue = []

    def update(self):  # Добовляем пасажра в конец очереди
        self.board.write("q")
        received_text = self.board.read()
        self.queue = received_text.split()

        print("Обновлена очередь: ", self.queue)

    def get_first(self):
        try:
            first = self.queue.pop(0)  # Удаляем первого пасажира из очереди
            self.board.write(first)
            return first

        except IndexError:
            return None

    def debug(self):
        print(self.queue)


if __name__ == "__main__":
    queue = Queue()
    robot = Robot()
