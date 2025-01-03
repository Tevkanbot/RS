import cv2 # Импортируем библиотеку openCV( распознование лица)
from fer import FER # Импортируем библиотеку FER(распознование эмоций)
import matplotlib.pyplot as plt 
import time

def face_capture():
    
    face_cascade_db = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml")
    emotion_detector = FER(mtcnn=True) # Инициализируем FER с использованием MTCNN

    camera = cv2.VideoCapture(0)

    while True:  
        success,img = camera.read()

        grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)# делаем изображение серым(требуется для распознования лица нейросетью)

        faces = face_cascade_db.detectMultiScale(grey_img, 1.1, 19)

        for (x, y, w, h) in faces:
            cv2.rectangle(img,(x, y), (x+w, y+h), (0,255,0), 2)

            # Вырезаем область лица
            face_roi = img[y:y+h, x:x+w]

            # Распознаем эмоцию
            emotions = emotion_detector.detect_emotions(face_roi) # Используем FER для распознавания эмоций

            # Если эмоция найдена, выводим ее на экран
            if emotions:

                emotions = emotions[0]
                emotions = emotions["emotions"]

                if emotions["angry"]> 0.5:
                    print("Внимание, подозрительная личность!")

                print(emotions)   
                time.sleep(2)
                
        #cv2.imshow("rez", img) для отображения лица на экран
        
        if cv2.waitKey(1)& 0xff == ord('q'):
            break
        
    camera.release()
    cv2.destroyAllWindows()   

def main():
    face_capture()

if __name__ == "__main__":
    main()
