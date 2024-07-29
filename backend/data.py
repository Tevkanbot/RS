import json
import os

class Data():
    def load(): # Получаем словарь из файла users.json и возвращаем его
        data = {} # рабочий словарь
        
        # Получаем путь к текущему файлу
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Формируем полный путь к файлу data.json
        file_path = os.path.join(current_dir, "data.json")

        with open(file_path, "r+", encoding="utf-8") as file:
            data = json.load(file)
        
        return data

    def dump(data): # Проверяем что аргумент это словарь, и если это словарь, то сохраняем его в файл

        if type(data)!= dict:
            raise TypeError("Argument must be a dict")

        # Получаем путь к текущему файлу
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Формируем полный путь к файлу data.json
        file_path = os.path.join(current_dir, "data.json")

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file)
            return True # Подтверждам успешное сохранение (для отладки)
