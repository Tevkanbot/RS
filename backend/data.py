import json
class Data():
    def load(): # Получаем словарь из файла users.json и возвращаем его
        data = {} # рабочий словарь

        with open("data.json", "r+", encoding="utf-8") as file:
            data = json.load(file)
        
        return data

    def dump(data): # Проверяем что аргумент это словарь, и если это словарь, то сохраняем его в файл

        if type(data)!= dict:
            raise TypeError("Argument must be a dict")

        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(data, file)
            return True # Подтверждам успешное сохранение (для отладки мб пригодиться)
        
        
            

