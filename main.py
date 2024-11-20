import keyboard
import asyncio
import multiprocessing
from voise.voise import Voise
from connections.robot import Robot
#from data.data import *
from face_recognizer.face_recognizer import FaceRecognizer
from voise.triggers import Trigger
from voise.data import Data
import time
def work(fromReturn):

    data = Data.load()
    
    #print(fromReturn)

    trigWord = fromReturn["trigger"]
    print ("я в ворке")
    num = fromReturn["num"]
    if fromReturn["WordCount"] == "one":
        exec(data["one_word_actions"][trigWord]["command"])

    if fromReturn["WordCount"] == "two":
        exec(data["two_word_actions"][trigWord]["command"])
    
def tea():
    ro.display("shop", "tea")
    #bill = bill + 50
    print("я в чае")

def bar():
    ro.display("shop", "bar")
    #bill = bill + 70

def coffee():
    ro.display("shop", "coffee")
    #bill = bill + 70

def napkins():
    ro.display("shop", "napkins")
    #bill = bill + 60

def mask():
    ro.display("shop", "mask")
    #bill = bill + 50
    
async def face_capture_func():
    await face.face_capture()
    

        
async def wait_1():
    while True:

        if keyboard.is_pressed("1"):
            queue.add(1)
            queue.debug()

        await asyncio.sleep(0.1)


async def main():
    
    vo.calibrate_recognizer()

    while True:
        #ro.display("logo")
        bill = 0
        propable_pasanger = queue.get_first()
        queue.debug()
        
        if propable_pasanger:
            ro.display("logo")
            print(propable_pasanger)
            time.sleep(1)
            ro.write("m1")

            # Робот доехал до вызывавшего его человека

            print(f"Мы у места под номером {propable_pasanger}")

            # Говорим здравствуйте
            vo.say("Здравствуйте")

            while True:
                phrase = vo.get_phrase()
                if not phrase:
                    continue
                res = Trigger.search_trigger(phrase)
                print("res", res)

                if res["WordCount"] != 0:
                    work(res)
                    print(propable_pasanger, res)
                    print("bill", bill)

                    if res["trigger"] == "всё":
                        break # Выход через слово ВСЁ

            
            time.sleep(1)
            ro.write("m0")

            time.sleep(2)

            ro.move_box(True)
            vo.say("Ожидаю продукты")
            time.sleep(5)
            ro.move_box(False)
            time.sleep(1)
            ro.write("m1")
            time.sleep(2)

            vo.say("Ваш заказ")
            ro.move_box(True)
            time.sleep(5)
            ro.move_box(False)
            time.sleep(1)
            ro.display("logo")
        await asyncio.sleep(1)

async def controller():

    global queue, ro, vo, face, bill
    vo = Voise()
    ro = Robot()
    queue = Robot.Queue()
    face = FaceRecognizer()
    

    task1 = asyncio.create_task(wait_1())
    face_controll_task = asyncio.create_task(face.face_capture())

    main_task = asyncio.create_task(main())
    print("start")
    await asyncio.gather(task1, face_controll_task, main_task) 

if __name__ == "__main__":
    
    asyncio.run(controller())