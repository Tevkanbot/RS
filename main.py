import keyboard
import asyncio
import multiprocessing
from voise.voise import Voise
from connections.robot import Robot, Queue
#from data.data import *
from face_recognizer.face_recognizer import FaceRecognizer
from voise.triggers import Trigger
from voise.data import Data
import time


def work(res, ro, vo):
    data = Data.load()

    trigWord = res["trigger"]
    print("я в ворке")
    num = res["num"]
    if res["WordCount"] == "one":
        exec(data["one_word_actions"][trigWord]["command"])

    if res["WordCount"] == "two":
        exec(data["two_word_actions"][trigWord]["command"])


def tea(ro):
    ro.display("shop", "tea")
    print("я в чае")


def bar(ro):
    ro.display("shop", "bar")


def coffee(ro):
    ro.display("shop", "coffee")


def napkins(ro):
    ro.display("shop", "napkins")


def mask(ro):
    ro.display("shop", "mask")


def emotion_control():
    # Создаём FaceRecognizer внутри процесса, чтобы избежать ошибок pickling
    face = FaceRecognizer()
    face.face_capture()


def main():
    vo = Voise()
    ro = Robot()
    queue = Queue()
    vo.calibrate_recognizer()

    while True:
        bill = 0
        queue.update()
        pasanger_seat = queue.get_first()

        if pasanger_seat:
            ro.display("logo")
            print(pasanger_seat)
            time.sleep(1)
            ro.move_to(pasanger_seat)

            print(f"Мы у места под номером {pasanger_seat}")

            vo.say("Здравствуйте")

            while True:
                phrase = vo.get_phrase()
                if not phrase:
                    continue
                res = Trigger.search_trigger(phrase)
                print("res", res)

                if res["WordCount"] != 0:
                    work(res, ro, vo)  # Передаём ro и vo в функцию work
                    print(pasanger_seat, res)
                    print("bill", bill)

                    if res["trigger"] == "всё":
                        break

            ro.move_to(pasanger_seat, True)

            ro.move_box(True)
            vo.say("Ожидаю продукты")
            time.sleep(10)
            ro.move_box(False)
            time.sleep(1)
            ro.write(pasanger_seat)
            time.sleep(pasanger_seat)

            vo.say("Ваш заказ")
            ro.move_box(True)
            time.sleep(10)
            ro.move_box(False)
            time.sleep(1)
            ro.display("logo")


if __name__ == "__main__":
    # Запуск процессов
    #emotion_control_process = multiprocessing.Process(target=emotion_control)
    main_pr = multiprocessing.Process(target=main)
    #emotion_control_process.start()
    main_pr.start()

    # Ожидание завершения процессов (опционально)
    #emotion_control_process.join()
    main_pr.join()
