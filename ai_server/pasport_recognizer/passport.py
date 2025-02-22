import cv2
import easyocr
import torch
import asyncio

# Список данных пассажиров (обновлённая структура)
PASSENGER_DATA = [
    {"FIO": ["карелин", "иван", "сергеевич"], "seat": 1, "van": 1},
    {"FIO": ["кирюхин", "дмитрий", "александрович"], "seat": 2, "van": 1},
    {"FIO": ["макеев", "дмитрий", ""], "seat": 3, "van": 1}
]

# Параметры рамки для тестирования с камерой (оставляем без изменений)
FRAME_WIDTH, FRAME_HEIGHT = 400, 200
FRAME_X, FRAME_Y = 100, 100

def process_frame(frame):
    """Обрезка кадра по области рамки (используется только для тестирования)."""
    return frame[FRAME_Y:FRAME_Y + FRAME_HEIGHT, FRAME_X:FRAME_X + FRAME_WIDTH]

def preprocess_image(image):
    """Улучшение изображения для OCR."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    normalized = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
    binary = cv2.adaptiveThreshold(normalized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)
    return binary

def recognize_passport_text(image):
    """Распознавание текста на изображении для тестирования."""
    preprocessed_image = preprocess_image(image)
    cv2.imshow("Проверка обработки", preprocessed_image)
    cv2.waitKey(1)
    reader = easyocr.Reader(['ru'], gpu=False)
    results = reader.readtext(preprocessed_image, paragraph=True, detail=0)
    print("Результаты EasyOCR:", results)
    return " ".join(results).lower()

def match_passenger_info(recognized_text):
    """Сопоставление распознанного текста с данными пассажиров для тестирования."""
    recognized_words = set(recognized_text.split())
    for passenger in PASSENGER_DATA:
        fio = set(passenger["FIO"])
        if fio.issubset(recognized_words):
            return {"van": passenger["van"], "seat": passenger["seat"]}
    return None

class PassportRecognizer:
    def __init__(self):
        self.use_gpu = True if torch.cuda.is_available() else False
        self.reader = easyocr.Reader(['ru'], gpu=self.use_gpu)
        self.passenger_data = PASSENGER_DATA

    def preprocess_image(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        normalized = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
        binary = cv2.adaptiveThreshold(normalized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY, 11, 2)
        return binary

    def recognize_text(self, image):
        preprocessed_image = self.preprocess_image(image)
        results = self.reader.readtext(preprocessed_image, paragraph=True, detail=0)
        recognized = " ".join(results).lower()
        return recognized

    def match_passenger_info(self, recognized_text):
        recognized_words = set(recognized_text.split())
        for passenger in self.passenger_data:
            fio = set(passenger["FIO"])
            if fio.issubset(recognized_words):
                return {"van": passenger["van"], "seat": passenger["seat"]}
        return None

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
        cv2.rectangle(frame, (FRAME_X, FRAME_Y), (FRAME_X + FRAME_WIDTH, FRAME_Y + FRAME_HEIGHT), (0, 255, 0), 2)
        cv2.putText(frame, "Поместите паспорт в рамку", (FRAME_X, FRAME_Y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.imshow("Кадр с камеры", frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            passport_frame = process_frame(frame)
            cv2.imshow("Обрезанное изображение", passport_frame)
            cv2.waitKey(1)
            recognized_text = recognize_passport_text(passport_frame)
            print("Распознанный текст:", recognized_text)
            match = match_passenger_info(recognized_text)
            if match:
                print(f"Ваш вагон: {match['van']}, ваше место: {match['seat']}")
            else:
                print("Извините, вас нет в списке пассажиров, обратитесь за справкой к проводнику")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("quit")
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
