import speech_recognition
from audioplayer import AudioPlayer
import os
class Voise:
    def __init__(self):
        self.sr =  speech_recognition.Recognizer()

        self.sr.pause_threshold = 1 #0.5
        self.sr.non_speaking_duration = 1


    def calibrate_recognizer(self):
        with speech_recognition.Microphone() as mic:
            print("Калибровка, ничего не говорите!")
            self.sr.adjust_for_ambient_noise(source=mic, duration=1)
            print("Калибровка завершена")
            

    def get_phrase(self):
        try:
            with speech_recognition.Microphone() as mic:
                print("<<<<<>>>>>")
                
                audio = self.sr.listen(source=mic, timeout= 0.5, phrase_time_limit= 5)
                query = self.sr.recognize_google(audio_data=audio, language="ru-RU").lower()

                return query
            
        except speech_recognition.WaitTimeoutError:
            pass
        except speech_recognition.UnknownValueError:
            pass
        except speech_recognition.RequestError as e:
            pass

    def say(self, phrase):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        voiselines_path = os.path.join(current_dir,  "materials", "voicelines")
        if phrase == "Здравствуйте":
            
            AudioPlayer(os.path.join(voiselines_path, "Здравствуйте.mp3")).play(block=True)
        if phrase == "Сколько до прибытия":

            AudioPlayer(os.path.join(voiselines_path, "Время до прибытия.mp3")).play(block=True)

        if phrase == "Где туалет":
            AudioPlayer(os.path.join(voiselines_path, "Где туалет.mp3")).play(block=True)

        if phrase == "Ассортимент":
            AudioPlayer(os.path.join(voiselines_path, "Ассортимент.mp3")).play(block=True)
        
        if phrase == "Ожидаю продукты":
            AudioPlayer(os.path.join(voiselines_path, "Ожидаю.mp3")).play(block=True)

        if phrase == "Ваш заказ":
            AudioPlayer(os.path.join(voiselines_path, "Ваш заказ.mp3")).play(block=True)
        
        if phrase == "дмитрий":
            AudioPlayer(os.path.join(voiselines_path, "Дмитрий.mp3")).play(block=True)

        if phrase == "иван":
            AudioPlayer(os.path.join(voiselines_path, "Иван.mp3")).play(block=True)

        if phrase == "Девиантное предупреждение":
            AudioPlayer(os.path.join(voiselines_path, "Девиантное предупреждение.mp3")).play(block=True)



            

if __name__ == "__main__":
    vo = Voise()
    vo.calibrate_recognizer
    #while True:
    #    print(vo.get_phrase())
    vo.say("Девиантное предупреждение")