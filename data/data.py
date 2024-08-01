#python classes
import json

#imported classes

#custom classes
class Preferences():

    @staticmethod
    def load_all(): # Получаем параметры из файла prefs.json и возвращаем их в виде словаря

        with open("data/prefs.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        
        return data
    
    @staticmethod
    def dump_all(data): # Загружаем все параметры

        with open("data/prefs.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            return True # Подтверждам успешное сохранение (для отладки мб пригодиться)
        
    @staticmethod
    def change_parameter(parameter, value): # Проверяем значение параметра через controller, если валидация успешна, то меняем значение параметра
                                  # True - удачная запись, False - некоректные данные, но запись произведена, в других случаях вызываются ошибки
        
        value = str(value)

        data = Preferences.load_all()

        try:
            controller = data["controller"][parameter] # Читаем допустимые значения параметров
            
        except KeyError:
            print(parameter)
            exit("Несуществующий параметр")

        # Валидируем параметр    
        if isinstance(controller, list):
            try:
                value = int(value)

                if value in range(int(controller[0]), int(controller[1])):
                    data[parameter] = value
                    Preferences.dump_all(data)
                    return True

                else:
                    print("NE TUDA")
                    if value > int(controller[1]):
                        print(f"{parameter} должен быть в диапазоне от {controller[0]} до {controller[1]}, установленно максимальное значение {controller[1]}")
                        data[parameter] = controller[1]
                    if value < int(controller[0]):
                        print(f"{parameter} должен быть в диапазоне от {controller[0]} до {controller[1]}, установленно минимальное значение {controller[0]}")
                        data[parameter] = controller[0]
                Preferences.dump_all(data)
                return False  
            except ValueError:
                pass
                  
        elif controller == "bool":
            if value.lower() == "true":
                value = True
            elif value.lower() == "false":
                value = False

            if type(value) == bool:
                # Валидация пройдена, загружаем параметр
                data[parameter] = value
                Preferences.dump_all(data)
                return True

        elif controller == "str":
            if type(value) == str:
                # Валидация пройдена, загружаем параметр
                data[parameter] = value.lower()
                Preferences.dump_all(data)
                return True
            
        else:
            raise Exception("Неизвестный тип параметра")
        
    @staticmethod
    def create_new_parameter(parameter, type):
        data = Preferences.load_all()
        if parameter not in data:
            if type == "bool" or type == "str" or isinstance(type, list) and len(type) == 2 and type[0].isdigit and type[1].isdigit and type[0] > type[1]:
                data["controller"][parameter] = type
                data[parameter] = None
                Preferences.dump_all(data)
                return True
            raise Exception("Неверно указан тип параметра")
        raise Exception("Параметр уже существует")
            

    @staticmethod
    def delete_parameter(parameter):
        data = Preferences.load_all()
        if parameter in data:
            del data[parameter]
            del data["controller"][parameter]
            Preferences.dump_all(data)
            return True
        raise Exception("Параметр не существует")
    
    def get_parameter(parameter):
        data = Preferences.load_all()
        if parameter in data:
            return data[parameter]
        raise Exception("Параметр не существует")