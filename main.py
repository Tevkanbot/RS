#default classes

#imported classes

#custom classes
from connections.serial import Board as bo
from data.data import Preferences as prefs

def main():
    while True:
        arduino = bo(port = input())

        arduino.Do.move_to(int(input()))

        arduino.read()


if __name__ == "__main__":
    main()
