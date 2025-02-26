from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import asyncio
import socket
from emotion_recognizer.main_recog import EmotionRecognizer
from faces_comparison.main_faces import FaceComparator
from pasport_recognizer.passport import PassportRecognizer  # Импортируем обновлённый модуль для работы с паспортами 
from tqdm import tqdm
import time

app = FastAPI()

class AIManager:
    def __init__(self):
        total_steps = 3
        with tqdm(total=total_steps, desc="Initializing AI Components", bar_format="{l_bar}{bar} [elapsed: {elapsed}]") as progress_bar:
            self.emotion_recognizer = EmotionRecognizer()
            progress_bar.update(1)

            self.face_comparator = FaceComparator()
            progress_bar.update(1)

            self.passport_recognizer = PassportRecognizer()
            progress_bar.update(1)

    async def process_emotion(self, file: UploadFile):
        start_time = time.time()
        result = await self.emotion_recognizer.recognize(file)
        end_time = time.time()
        result["time_elapsed"] = end_time - start_time
        return result

    async def compare_faces(self, file: UploadFile):
        start_time = time.time()
        result = await self.face_comparator.compare_with_database(file)
        end_time = time.time()
        return {"result": result, "time_elapsed": end_time - start_time}

    async def process_passport(self, file: UploadFile):
        start_time = time.time()
        result = await self.passport_recognizer.recognize(file)
        end_time = time.time()
        return {"result": result, "time_elapsed": end_time - start_time}

ai_manager = AIManager()

class ImageRecognitionRequest(BaseModel):
    description: str

@app.post("/recognize/emotion")
async def recognize_emotion(file: UploadFile = File(...)):
    """Endpoint для распознавания эмоций"""
    try:
        result = await ai_manager.process_emotion(file)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/compare/faces")
async def compare_faces(file: UploadFile = File(...)):
    """Endpoint для сравнения лиц"""
    try:
        result = await ai_manager.compare_faces(file)
        return {"status": "success", "data": result["result"], "time_elapsed": result["time_elapsed"]}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/recognize/passport")
async def recognize_passport(file: UploadFile = File(...)):
    """Endpoint для распознавания паспорта и сопоставления с данными"""
    try:
        result = await ai_manager.process_passport(file)
        return {"status": "success", "data": result["result"], "time_elapsed": result["time_elapsed"]}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/status")
def status():
    """Health check endpoint"""
    return {"status": True}

if __name__ == "__main__":
    import uvicorn
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"Server is running at: http://{local_ip}:8008")
    uvicorn.run(app, host="0.0.0.0", port=8008)
