import cv2
import easyocqqr

json = [
    3,
    {
        "FIO": ["карелин", "иван", "сергеевич"],
        "seat": 1,
        "van": 1
    },
    {
        "FIO": ["кирюхин", "дмитрий", "александрович"],
        "seat": 2,
        "van": 1
    },
    {
        "FIO": ["макеев", "дмитрий", ""],
        "seat": 3,
        "van": 1
    }
]

# Инициализация easyocr для русского языка
#reader = easyocr.Reader(['ru'])
custom_config = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя'

cap = cv2.VideoCapture(0)

# Размеры рамки и её положение на экране
frame_width = 400
frame_height = 200
frame_x = 100  
frame_y = 100  

while True:
    ret, frame = cap.read() 

    if not ret:
        print("Не удалось получить изображение с камеры")
        break

   
    cv2.rectangle(
        frame, 
        (frame_x, frame_y), 
        (frame_x + frame_width, frame_y + frame_height), 
        (0, 255, 0), 2
    )
    
    
    cv2.putText(
        frame, 
        "Поместите паспорт в рамку", 
        (frame_x, frame_y - 10), 
        cv2.FONT_HERSHEY_SIMPLEX, 
        0.6, 
        (0, 255, 0), 
        2
    )

    # Отображение изображения на экране
    cv2.imshow("Кадр с камеры", frame)

   
    if cv2.waitKey(1) & 0xFF == ord('s'):
        # Обрезаем кадр по области рамки
        passport_frame = frame[frame_y:frame_y + frame_height, frame_x:frame_x + frame_width]

        # Распознавание текста в выделенной области
        results = 0#reader.readtext(passport_frame, paragraph=True, detail=0, allowlist=custom_config)
        print(results)

       
        
        if results != None:
            text = results.split("\n") #разделяем текст по строкам

            print(text)
            text = text.lower()
            text = text.split(" ")

            i = 1
            for i in range(3):
                i = 1
                fio = json[i].get("FIO") #вытаскиваем данные билетов

                #сортируем
                fio = fio.sort()
                #text = text.sort()

                #если данные билета соответствуют данным паспорта, то выводим место
                if fio == text:
                    print(f"ваш вагон: {json[2].get("van")}, ваше место: {json[2].get("seat")}")
                    break

                else:
                    i+=1
                    
            if i>= json[0]:
                print("Извините, вас нет в списке пассажиров, обратитесь за справкой к проводнику")
                
    # Выход из программы по нажатию 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Освобождение ресурсов
cap.release()
cv2.destroyAllWindows()