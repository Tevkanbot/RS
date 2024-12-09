import cv2
import pytesseract

Json = [
    3,
    {
        "FIO": [
            "карелин",
            "иван",
            "сергеевич"
        ],
        "seat": 1,
        "van": 1
    },
    {
        "FIO": [
            "кирюхин",
            "дмитрий",
            "александрович"
        ],
        "seat": 2,
        "van": 1
    },
    {
        "FIO": [
            "макеев",
            "дмитрий",
            ""
        ],
        "seat": 3,
        "van": 1
    }
]

pytesseract.pytesseract.tesseract_cmd = r'E:\Tesseract-OCR\tesseract.exe'

custom_config = r'-c tessedit_char_whitelist=АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя -l rus'

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise IOError("Не удалось открыть камеру")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Ошибка получения изображения с камеры")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    text = pytesseract.image_to_string("C:\projects\RS\pasport_eye\image.jpg",lang="rus")#config = custom_config

    cv2.imshow('Камера', frame)

    if cv2.waitKey(1) & 0xFF == ord("s"):
        print("Распознанный текст:\n", text)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()