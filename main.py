import keyboard
import asyncio

from voise.addins.voise import Voise
from connections.robot import Robot
from data.data import *


async def wait_1():
    while True:

        if keyboard.is_pressed("1"):
            queue.add(1)
            queue.debug()

        await asyncio.sleep(0.1)

async def wait_2():
    while True:

        if keyboard.is_pressed("2"):
            queue.add(2)
            queue.debug()

        await asyncio.sleep(0.1 )

async def wait_3():
    while True:

        if keyboard.is_pressed("3"):
            queue.add(3)
            queue.debug()

        await asyncio.sleep(0.1)



async def main():

    while True:
        propable_pasanger = queue.get_first()
        queue.debug()

        if propable_pasanger:
            print(propable_pasanger)

            move_task = asyncio.create_task(ro.move_to(propable_pasanger))

            await move_task 
            # Робот доехал до вызывавшего его человека

            print(f"Мы у места под номером {propable_pasanger}")

            # Говорим здравствуйте

            # Спрашиваем, что нужно человеку

            # Едем за заказом

            # Возвращаемся

            # Говорим заказ доставлен

            # Открываем ящик с заказом

            # Репит




        await asyncio.sleep(1)

async def controller():

    global queue, ro, vo
    vo = Voise()
    ro = Robot()
    queue = Robot.Queue()

    vo.calibrate_recognizer()

    task1 = asyncio.create_task(wait_1())
    task2 = asyncio.create_task(wait_2())
    task3 = asyncio.create_task(wait_3())

    main_task = asyncio.create_task(main())
    print("start")
    await asyncio.gather(task1, task2, task3, main_task ) 

if __name__ == "__main__":
    asyncio.run(controller())