from serial import Board
bo = Board(port = "COM3")

bo.move_to(input())

bo.read()

bo.end()