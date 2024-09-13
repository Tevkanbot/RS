import cv2
import pytesseract

# Установка пути к Tesseract
pytesseract.pytesseract.tesseract_cmd = r'E:\Tesseract-OCR\tesseract.exe' # Замените путь на свой

# Установка русского языка для Tesseract
pytesseract.pytesseract.tesseract_lang = 'rus'

# Загрузка камеры
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise IOError("Не удалось открыть камеру")

while(True):
    # Получение кадра
    ret, frame = cap.read()

    # Преобразование изображения в оттенки серого
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Улучшение изображения для OCR (необязательно)
    # Например, использование порогового значения
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Распознавание текста
    text = pytesseract.image_to_string("C:\RS\pasport_eye\паспорт.jpg", lang='rus')

    # Вывод текста
    print(text)

    # Отображение изображения (необязательно)
    cv2.imshow('Камера', frame)

    # Выход из цикла при нажатии клавиши 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Освобождение ресурсов
cap.release()
cv2.destroyAllWindows()
