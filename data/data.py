#python classes
import json

#imported classes

#custom classes
class Preferences():

    @staticmethod
    def load_all(): # Получаем параметры из файла prefs.json и возвращаем их в виде словаря

        with open("data/app_data.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        
        return data
    
    @staticmethod
    def dump_all(data): # Загружаем все параметры

        with open("data/app_data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            return True # Подтверждам успешное сохранение (для отладки мб пригодиться)
        
class Pasangers():

    @staticmethod
    def load_all():
        
        with open("data/pasangers.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        
        return data
    
    @staticmethod
    def dump_all(data):

        with open("data/pasangers.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            return True