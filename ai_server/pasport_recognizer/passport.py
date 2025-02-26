import cv2
import easyocr
import torch
import asyncio
import re
import time
from rapidfuzz import fuzz

# Passenger data (updated structure)
PASSENGER_DATA = [
    {"FIO": ["карелин", "иван", "сергеевич"], "seat": 1, "van": 1},
    {"FIO": ["кирюхин", "дмитрий", "александрович"], "seat": 2, "van": 1},
    {"FIO": ["макеев", "дмитрий", "николаевич"], "seat": 1, "van": 1},
    {"FIO": ["симаков", "никита", "евгеньевич"], "seat": 2, "van": 1},
]

# Preprocess image to improve OCR quality
def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    filtered = cv2.bilateralFilter(gray, 9, 75, 75)
    equalized = cv2.equalizeHist(filtered)
    _, thresh = cv2.threshold(equalized, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    enlarged = cv2.resize(closed, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    return enlarged

# Recognize text from the image using OCR
def recognize_passport_text(image):
    preprocessed_image = preprocess_image(image)
    cv2.imshow("Preprocessed Image", preprocessed_image)
    cv2.waitKey(1)
    reader = easyocr.Reader(['ru'], gpu=False)
    results = reader.readtext(preprocessed_image, paragraph=True, detail=0)
    print("EasyOCR Results:", results)
    return " ".join(results).lower()

# Fuzzy matching function to compare FIO words with recognized words
def fuzzy_match(fio_words, recognized_words, threshold=80):
    match_count = 0
    for fio_word in fio_words:
        for rec_word in recognized_words:
            if fuzz.ratio(fio_word, rec_word) >= threshold:
                match_count += 1
                break
    required = len(fio_words) if len(fio_words) == 1 else len(fio_words) - 1
    return match_count >= required

# Compare recognized text with passenger data using fuzzy matching
def match_passenger_info(recognized_text, threshold=80):
    recognized_words = re.findall(r'\w+', recognized_text.lower())
    for passenger in PASSENGER_DATA:
        fio_words = [word.lower() for word in passenger["FIO"] if word]
        if fuzzy_match(fio_words, recognized_words, threshold):
            return {"van": passenger["van"], "seat": passenger["seat"]}
    return None

# Passport recognition class
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

    # Process the passport image
    def _process_passport(self, contents):
        import numpy as np
        image = cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR)
        if image is None:
            return {"status": "error", "message": "Unable to read the image."}
        
        start_time = time.time()
        recognized_text = self.recognize_text(image)
        match = self.match_passenger_info(recognized_text)
        end_time = time.time()
        time_taken = round(end_time - start_time, 2)

        if match:
            return {
                "status": "success",
                "data": match,
                "recognized_text": recognized_text,
                "time_elapsed": time_taken
            }
        else:
            return {
                "status": "not_found",
                "message": "Passenger not found",
                "recognized_text": recognized_text,
                "time_elapsed": time_taken
            }

    # Asynchronous method to handle passport recognition
    async def recognize(self, file):
        contents = await file.read()
        result = await asyncio.to_thread(self._process_passport, contents)
        return result

# Testing through the camera – recognition for the entire image without a frame
def main():
    import cv2
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Unable to access the camera")
        return
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error capturing image")
            break
        cv2.imshow("Camera Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            recognized_text = recognize_passport_text(frame)
            print("Recognized Text:", recognized_text)
            match = match_passenger_info(recognized_text)
            if match:
                print(f"Your train: {match['van']}, your seat: {match['seat']}")
            else:
                print("Sorry, you are not on the list. Please consult with the conductor.")
        elif key == ord('q'):
            print("Quit")
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
