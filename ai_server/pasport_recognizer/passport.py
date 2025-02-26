import cv2
import easyocr
import torch
import asyncio
import re
from rapidfuzz import fuzz

# Список данных пассажиров (обновлённая структура)
PASSENGER_DATA = [
    {"FIO": ["карелин", "иван", "сергеевич"], "seat": 1, "van": 1},
    {"FIO": ["кирюхин", "дмитрий", "александрович"], "seat": 2, "van": 1},
    {"FIO": ["макеев", "дмитрий", "николаевич"], "seat": 1, "van": 1},
    {"FIO": ["симаков", "никита", "евгеньевич"], "seat": 2, "van": 1},
]

def preprocess_image(image):
    """Улучшение изображения для OCR с использованием размытия, CLAHE и масштабирования."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    filtered = cv2.bilateralFilter(gray, 9, 75, 75)
    equalized = cv2.equalizeHist(filtered)
    _, thresh = cv2.threshold(equalized, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    enlarged = cv2.resize(closed, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    return enlarged

def recognize_passport_text(image):
    """Распознавание текста на изображении с улучшенной предобработкой."""
    preprocessed_image = preprocess_image(image)
    cv2.imshow("Preprocessed Image", preprocessed_image)
    cv2.waitKey(1)
    reader = easyocr.Reader(['ru'], gpu=False)
    results = reader.readtext(preprocessed_image, paragraph=True, detail=0)
    print("Результаты EasyOCR:", results)
    return " ".join(results).lower()

def fuzzy_match(fio_words, recognized_words, threshold=80):
    """
    Для каждого слова из fio_words ищем, есть ли слово из recognized_words с коэффициентом схожести >= threshold.
    Требуемое количество совпадений: если больше одного слова, то хотя бы len(fio_words)-1 совпадение,
    иначе — одно совпадение.
    """
    match_count = 0
    for fio_word in fio_words:
        for rec_word in recognized_words:
            if fuzz.ratio(fio_word, rec_word) >= threshold:
                match_count += 1
                break
    required = len(fio_words) if len(fio_words) == 1 else len(fio_words) - 1
    return match_count >= required

def match_passenger_info(recognized_text, threshold=80):
    """Сопоставление распознанного текста с данными пассажиров с использованием фаззи-сопоставления."""
    recognized_words = re.findall(r'\w+', recognized_text.lower())
    for passenger in PASSENGER_DATA:
        fio_words = [word.lower() for word in passenger["FIO"] if word]
        if fuzzy_match(fio_words, recognized_words, threshold):
            return {"van": passenger["van"], "seat": passenger["seat"]}
    return None

class PassportRecognizer:
    def __init__(self):
        self.use_gpu = True if torch.cuda.is_available() else False
        self.reader = easyocr.Reader(['ru'], gpu=self.use_gpu)
        self.passenger_data = PASSENGER_DATA

    def preprocess_image(self, image):
        return preprocess_image(image)

    def recognize_text(self, image):
        preprocessed_image = self.preprocess_image(image)
        results = self.reader.readtext(preprocessed_image, paragraph=True, detail=0)
        recognized = " ".join(results).lower()
        return recognized

    def match_passenger_info(self, recognized_text, threshold=80):
        return match_passenger_info(recognized_text, threshold)

    def _process_passport(self, contents):
        import numpy as np
        image = cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR)
        if image is None:
            return {"status": "error", "message": "Не удалось прочитать изображение."}
        recognized_text = self.recognize_text(image)
        match = self.match_passenger_info(recognized_text)
        if match:
            return {"status": "success", "data": match, "recognized_text": recognized_text}
        else:
            return {"status": "not_found", "message": "Пассажир не найден", "recognized_text": recognized_text}

    async def recognize(self, file):
        contents = await file.read()
        result = await asyncio.to_thread(self._process_passport, contents)
        return result

# Тестирование через камеру – распознавание всего изображения без рамки
def main():
    import cv2
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Не удалось получить доступ к камере")
        return
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Не удалось получить изображение с камеры")
            break
        cv2.imshow("Кадр с камеры", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            recognized_text = recognize_passport_text(frame)
            print("Распознанный текст:", recognized_text)
            match = match_passenger_info(recognized_text)
            if match:
                print(f"Ваш вагон: {match['van']}, ваше место: {match['seat']}")
            else:
                print("Извините, вас нет в списке пассажиров, обратитесь за справкой к проводнику")
        elif key == ord('q'):
            print("quit")
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
