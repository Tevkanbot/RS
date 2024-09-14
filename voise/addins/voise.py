import speech_recognition

class Voise:
    def __init__(self):
        self.sr =  speech_recognition.Recognizer()

        self.sr.pause_threshold = 0.5
        self.sr.non_speaking_duration = 0.5

    def calibrate_recognizer(self):
        with speech_recognition.Microphone() as mic:
            print("Калибровка, ничего не говорите!")
            self.sr.adjust_for_ambient_noise(source=mic, duration=1)
            print("Калибровка завершена")
            

    def get_phrase(self):
        try:
            with speech_recognition.Microphone() as mic:
                print("<<<<<>>>>>")
                
                audio = self.sr.listen(source=mic, timeout=0.5)
                query = self.sr.recognize_google(audio_data=audio, language="ru-RU").lower()

                return query
            
        except speech_recognition.WaitTimeoutError:
            pass
        except speech_recognition.UnknownValueError:
            pass
        except speech_recognition.RequestError as e:
            pass
    
if __name__ == "__main__":
    vo = Voise()
    vo.calibrate_recognizer
    while True:
        print(vo.get_phrase())