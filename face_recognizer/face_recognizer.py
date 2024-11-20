import cv2 # Импортируем библиотеку openCV( распознование лица)
import cv2 # Импортируем библиотеку openCV (распознование лица)
from fer import FER # Импортируем библиотеку FER (распознование эмоций)
import matplotlib.pyplot as plt
import time
import asyncio

class FaceRecognizer:

    def __init__(self): # Исправлено: метод __init__ вместо init
        self.face_cascade_db = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.emotion_detector = FER(mtcnn=True) # Инициализируем FER с использованием MTCNN

        self.camera = cv2.VideoCapture(0)


    async def face_capture(self):
        try:
            while True:

                success, img = self.camera.read()

                if not success: # Проверка успешности считывания изображения
                    print("Ошибка: Не удалось получить изображение с камеры")
                    return False

                grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Делаем изображение серым (требуется для распознавания лица нейросетью)

                faces = self.face_cascade_db.detectMultiScale(grey_img, 1.1, 19)

                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2) # Рисуем прямоугольник вокруг лица

                    # Вырезаем область лица
                    face_roi = img[y:y + h, x:x + w]

                    # Распознаем эмоцию
                    emotions = self.emotion_detector.detect_emotions(face_roi) # Используем FER для распознавания эмоций
                    await asyncio.sleep(0,5)
                    # Если эмоция найдена, выводим ее на экран
                    if emotions:
                        emotions = emotions[0]
                        emotions = emotions["emotions"]
                        #print(emotions)
                        if emotions["angry"] > 0.5:
                            print("Внимание, подозрительная личность!")
                        
                #return False
                #cv2.imshow("rez", img) #для отображения лица на экран
                # if cv2.waitKey(1) & 0xff == ord('q'):
                #     pass
                    await asyncio.sleep(0.1)
        finally:
            self.camera.release()
            cv2.destroyAllWindows()




if __name__ == "__main__":
    face = FaceRecognizer()
    asyncio.run(face.face_capture())
    
