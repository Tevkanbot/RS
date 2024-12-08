import cv2
import numpy as np

""""
                            ПРИМЕЧАНИЕ

для корректной работы изображения должны быть одинакого формата и размера

get_face работает по принципу попиксильного сравнения и при сдвиге на 1 пиксель коэф. совпадения будет 0

                        МЕСТНЫЕ ФУНКЦИИ

face_recog(face_cascade_db, camera) принимает каскад и камеру; возвращает координаты лица

get_face(image_path) принимает путь к файлу (или изображение); возвращает коэфицент совпадения
"""


# загрузка модели
model_path = r"C:\projects\RS\faces\data_face\res10_300x300_ssd_iter_140000.caffemodel"
config_path = r"C:\projects\RS\faces\data_face\deploy.prototxt"
net = cv2.dnn.readNetFromCaffe(config_path, model_path)

face_cascade_db = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


camera = cv2.VideoCapture(0)

def face_recog(face_cascade_db, camera):
    """Функция нахождения лица через камеру"""
    while True:  
        success, img = camera.read()
        if not success:
            print("Не удалось получить изображение с камеры.")
            return None

        grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade_db.detectMultiScale(grey_img, 1.1, 19)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Вырезаем область лица
            face_roi = img[y:y + h, x:x + w]
            cv2.imshow("Лица", face_roi)
            cv2.waitKey(2000)  # Пауза на 2 секунды
            cv2.destroyAllWindows()
            return face_roi 

        cv2.imshow("Камера", img)

        # Прерывание на клавишу "q"
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    return None


def get_face(image_path):
    # загрузка изображения
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Не удалось загрузить изображение")

    # преобразование в BLOB
    h, w = img.shape[:2]
    blob = cv2.dnn.blobFromImage(img, 1.0, (300, 300), (104.0, 177.0, 123.0))

    # пропуск через сеть
    net.setInput(blob)
    detections = net.forward()

    # извлечение лица
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:  # точность
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x1, y1, x2, y2) = box.astype("int")
            face = img[y1:y2, x1:x2]
            return face

    return None


camera_face = face_recog(face_cascade_db,camera)
file_face = get_face(r"C:\projects\RS\faces\data_face\2.jpg")

if camera_face is not None and file_face is not None:
    # Приводим лица к одинаковому размеру
    h, w = file_face.shape[:2]
    resized_camera_face = cv2.resize(camera_face, (w, h))

    # сравнение лиц
    diff = cv2.absdiff(resized_camera_face, file_face)
    similarity = 1 - (np.sum(diff) / (file_face.size * 255))
    print(f"Сходство лиц: {similarity:.2f}")
else:
    print("Не удалось найти лица в одном из изображений.")



























