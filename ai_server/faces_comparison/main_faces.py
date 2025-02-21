import cv2
import numpy as np
import os
from pathlib import Path
import asyncio
from concurrent.futures import ThreadPoolExecutor
from sklearn.metrics.pairwise import cosine_similarity
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
from fastapi import UploadFile
from io import BytesIO

class FaceComparator:
    """Класс для работы с распознаванием и сравнением лиц."""
    def __init__(self):
        self.base_path = Path(__file__).resolve().parent
        self.data_path = self.base_path / "data_face"
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.detector = MTCNN(device=self.device)
        self.encoder = InceptionResnetV1(pretrained='vggface2').eval().to(self.device)
        self.executor = ThreadPoolExecutor(max_workers=os.cpu_count())
        self.database_encodings = self.preload_database()

    def preload_database(self):
        database_encodings = {}
        for seat_folder in self.data_path.iterdir():
            if not seat_folder.is_dir():
                continue
            seat_number = seat_folder.name
            encodings = []
            for image_file in seat_folder.iterdir():
                if image_file.suffix.lower() not in [".jpg", ".png"]:
                    continue
                image = cv2.imread(str(image_file))
                if image is None:
                    continue
                face = self.detect_face(image)
                if face is not None:
                    encoding = self.encode_face(face)
                    if encoding is not None:
                        encodings.append(encoding)
            if encodings:
                database_encodings[seat_number] = torch.stack(encodings).mean(dim=0)
        return database_encodings

    def detect_face(self, image):
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes, _ = self.detector.detect(rgb_image)
        if boxes is not None and len(boxes) > 0:
            x1, y1, x2, y2 = map(int, boxes[0])
            x1, y1 = max(0, x1), max(0, y1)
            face = image[y1:y2, x1:x2]
            face = cv2.resize(face, (160, 160))
            return face
        return None

    def encode_face(self, face):
        rgb_face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        face_tensor = torch.tensor(rgb_face).permute(2, 0, 1).unsqueeze(0).float() / 255.0
        face_tensor = face_tensor.to(self.device)
        with torch.no_grad():
            encoding = self.encoder(face_tensor).squeeze(0)
        return encoding

    def _process_comparison(self, file_bytes):
        image = cv2.imdecode(np.frombuffer(file_bytes, np.uint8), cv2.IMREAD_COLOR)
        if image is None:
            return {"status": "error", "message": "Не удалось прочитать изображение."}
        face = self.detect_face(image)
        if face is None:
            return {"status": "error", "message": "Изображение не содержит лица."}
        input_encoding = self.encode_face(face)
        if input_encoding is None:
            return {"status": "error", "message": "Не удалось закодировать лицо."}
        similarities = {}
        for seat_number, db_encoding in self.database_encodings.items():
            similarity = float(cosine_similarity([input_encoding.cpu().numpy()], [db_encoding.cpu().numpy()])[0][0])
            similarities[seat_number] = similarity
        if similarities:
            best_match_seat = max(similarities, key=similarities.get)
            highest_similarity = similarities[best_match_seat]
            if highest_similarity > 0.6:
                return {"status": "success", "data": {"seat": best_match_seat, "similarity": highest_similarity}}
        return {"status": "not_found", "message": "Лицо не совпало ни с одним в базе."}

    async def compare_with_database(self, file: UploadFile):
        try:
            file_bytes = await file.read()
            result = await asyncio.to_thread(self._process_comparison, file_bytes)
            return result
        except Exception as e:
            return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import cv2
    import asyncio
    from io import BytesIO
    from fastapi import UploadFile

    comparator = FaceComparator()

    async def test_with_camera():
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Не удалось получить доступ к камере.")
            return
        print("Нажмите 'q', чтобы выйти.")
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Не удалось получить изображение с камеры.")
                break
            _, buffer = cv2.imencode('.jpg', frame)
            file = UploadFile(filename="camera_frame.jpg", file=BytesIO(buffer.tobytes()))
            result = await comparator.compare_with_database(file)
            print(result)
            cv2.imshow("Камера", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    asyncio.run(test_with_camera())
