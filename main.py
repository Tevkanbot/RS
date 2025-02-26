# import keyboard
import asyncio
import time
# import multiprocessing


from voise.voise import Voise  # Распознование и симуляция речи
from voise.trigger import Trigger  # Распознование в речи
# Работа с механичкской частью и кнопками у пассажиров (Queue)
from connections.robot import Robot, Queue


def work(trigger, ro, vo):
    """Execute the command associated with the given trigger"""
    if trigger:
        exec(trigger["command"])
    else:
        print("No action for the given trigger.")


async def main():
    vo = Voise()
    ro = Robot()
    queue = Queue()
    vo.calibrate_recognizer()
    print("Классы созданы, начало работы.")

    while True:
        queue.update()
        pasanger_seat = queue.get_first()

        if pasanger_seat:

            ro.move_to(pasanger_seat)

            print(f"Мы у места под номером {pasanger_seat}")

            vo.say("Здравствуйте")
            vo.say("Ассортимент")
            ro.start_shopping()

            while True:
                phrase = vo.get_phrase()
                if not phrase:
                    continue

                trigger = Trigger.find_trigger(phrase)

                if trigger:
                    work(trigger, ro, vo)
                    # print(pasanger_seat, trigger)

                    if trigger["phrase"] == "всё":
                        break

            ro.move_to(0)
            ro.move_box(True)
            vo.say("Ожидаю продукты")
            while True:
                phrase = vo.get_phrase()
                if not phrase:
                    continue

                if trigger["phrase"] == "всё":
                    break

            ro.move_box(False)
            time.sleep(1)
            ro.move_to(pasanger_seat)

            vo.say("Ваш заказ")
            ro.move_box(True)
            while True:
                phrase = vo.get_phrase()
                if not phrase:
                    continue

                if trigger["phrase"] == "всё":
                    break
            ro.move_box(False)


if __name__ == "__main__":

    asyncio.run(main())
