import cv2
import pytesseract


pytesseract.pytesseract.tesseract_cmd = r'E:\Tesseract-OCR\tesseract.exe' 

# Установка русского языка для Tesseract
pytesseract.pytesseract.tesseract_lang = 'rus'

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise IOError("Не удалось открыть камеру")

while(True):
    ret, frame = cap.read()

    # Преобразование изображения в оттенки серого
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Распознавание текста
    text = pytesseract.image_to_string(thresh, lang='rus')

    print(text)

    cv2.imshow('Камера', frame)

    # Выход из цикла при нажатии клавиши 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Освобождение ресурсов
cap.release()
cv2.destroyAllWindows()
