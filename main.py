#default classes

#imported classes

#custom classes
from connections.serial import Board
def main():
    while True:
        bo = Board(port = "COM3")

        bo.move_to(input())

        bo.read()

if __name__ == "__main__":
    main()
