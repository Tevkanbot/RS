import pytesseract
import cv2
import json

camera = cv2.VideoCapture(0)



def extract_passport_data(output_file="passport_data.json"):

    # Загрузка изображения
    image = cv2.imread("C:\RS\backend\паспорт.jpg")

    # Преобразование изображения в оттенки серого
    grey_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)# делаем изображение серым(требуется для распознования лица нейросетью)

    # Бинаризация изображения
    thresh = cv2.threshold(grey_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Удаление шума
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

    # Распознавание текста
    text = pytesseract.image_to_string(opening, lang='rus') # Изменить 'rus' на подходящий язык

    # Извлечение данных
    data = {}
    lines = text.splitlines()
    for line in lines:
        parts = line.split(":")
        if len(parts) == 2:
            key = parts[0].strip()
            value = parts[1].strip()
            data[key] = value

    # Сохранение данных в JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return data

extract_passport_data(output_file="passport_data.json")