#import keyboard
import asyncio
import time
#import multiprocessing


from voise.voise import Voise #Распознование и симуляция речи
from voise.trigger import Trigger #Распознование в речи
from connections.robot import Robot, Queue #Работа с механичкской частью и кнопками у пассажиров (Queue)


def work(trigger, ro, vo):
    """Execute the command associated with the given trigger"""
    if trigger:
        exec(trigger["command"])
    else:
        print("No action for the given trigger.")


def tea(ro):
    ro.display("shop", "tea")
    print("Executing tea command")


def bar(ro):
    ro.display("shop", "bar")
    print("Executing bar command")


def coffee(ro):
    ro.display("shop", "coffee")
    print("Executing coffee command")


def napkins(ro):
    ro.display("shop", "napkins")
    print("Executing napkins command")


def mask(ro):
    ro.display("shop", "mask")
    print("Executing mask command")



async def main():
    vo = Voise()
    ro = Robot()
    queue = Queue()
    vo.calibrate_recognizer()
    print("Классы созданы, начало работы.")

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
                trigger = Trigger.find_trigger(phrase)
                print("Trigger", trigger)

                if trigger:
                    work(trigger, ro, vo)
                    print(pasanger_seat, trigger)
                    print("bill", bill)

                    if trigger["phrase"] == "всё":
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

    asyncio.run(main())
