import cv2
import numpy as np
from fer import FER
from fastapi import UploadFile
import asyncio
import time

class EmotionRecognizer:
    def __init__(self):
        # Инициализируем детектор лиц и анализатор эмоций
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.emotion_detector = FER(mtcnn=True)

    def _process_image(self, image_bytes, start_time):
        image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
        if image is None:
            end_time = time.time()
            return {
                "status": "error",
                "message": "Не удалось декодировать изображение.",
                "time_taken": f"{end_time - start_time:.4f} seconds"
            }
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=7, minSize=(50, 50))
        if len(faces) == 0:
            end_time = time.time()
            return {
                "status": "no_face_detected",
                "message": "No face detected in the image.",
                "time_taken": f"{end_time - start_time:.4f} seconds"
            }
        for (x, y, w, h) in faces:
            face = image[y:y + h, x:x + w]
            analysis = self.emotion_detector.detect_emotions(face)
            if analysis:
                emotions = analysis[0]['emotions']
                if emotions.get('angry', 0) > 0.4 or emotions.get('disgust', 0) > 0.5 or emotions.get('sad', 0) > 0.5:
                    end_time = time.time()
                    return {
                        "status": "aggression_detected",
                        "message": "Slight aggression detected.",
                        "time_taken": f"{end_time - start_time:.4f} seconds"
                    }
        end_time = time.time()
        return {
            "status": "no_aggression_detected",
            "message": "No aggression detected.",
            "time_taken": f"{end_time - start_time:.4f} seconds"
        }

    async def recognize(self, file: UploadFile):
        start_time = time.time()
        try:
            image_bytes = await file.read()
            # Выполнение тяжёлой обработки в отдельном потоке
            result = await asyncio.to_thread(self._process_image, image_bytes, start_time)
            return result
        except Exception as e:
            end_time = time.time()
            return {
                "status": "error",
                "message": str(e),
                "time_taken": f"{end_time - start_time:.4f} seconds"
            }

if __name__ == "__main__":
    # Тестирование через веб-камеру (оставляем без изменений)
    import cv2
    from io import BytesIO
    from starlette.datastructures import UploadFile as TestUploadFile

    recognizer = EmotionRecognizer()

    async def test_with_webcam():
        cap = cv2.VideoCapture(0)
        print("Press 'q' to quit.")
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture image from camera.")
                break
            _, buffer = cv2.imencode('.jpg', frame)
            file_like = BytesIO(buffer.tobytes())
            upload_file = TestUploadFile(filename="test.jpg", file=file_like)
            result = await recognizer.recognize(upload_file)
            print("API Response:", result)
            cv2.imshow("Camera", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    asyncio.run(test_with_webcam())
