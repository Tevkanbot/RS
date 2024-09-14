import os
import vlc
class Buy:
    
    def tea():
        # Получаем путь к текущему файлу
        # Формируем полный путь к GIF-файлу
        #gif_path = os.path.join(current_dir, "MPiJ.gif")
        #os.startfile(gif_path) #это типо оплата (временная версия)
        # Формируем полный путь к аудиофайлу

        current_dir = os.path.dirname(os.path.abspath(__file__))
        audio_path = os.path.join(current_dir, "materials", "Voiceovers", "oplata_70.mp3")
        vlc.MediaPlayer(audio_path).play()

    def chocolate():
        # Получаем путь к текущему файлу
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Формируем полный путь к GIF-файлу
        gif_path = os.path.join(current_dir,"RS", "backend", "MPiJ.gif")
        os.startfile(gif_path) #надо вставить видео с загрузкой и оплатой

        # Формируем полный путь к аудиофайлу
        audio_path = os.path.join(current_dir,"Voiceovers", "oplata_100.mp3")
        os.startfile(audio_path) #это озвучка

    def coffee():
        # Получаем путь к текущему файлу
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Формируем полный путь к GIF-файлу
        gif_path = os.path.join(current_dir,"RS", "backend", "MPiJ.gif")
        os.startfile(gif_path) #надо вставить видео с загрузкой и оплатой

        # Формируем полный путь к аудиофайлу
        audio_path = os.path.join(current_dir,"RS", "backend", "Voiceovers", "oplata_80.mp3")
        os.startfile(audio_path) #это озвучка

    def napkins():
        # Получаем путь к текущему файлу
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Формируем полный путь к GIF-файлу
        gif_path = os.path.join(current_dir,"RS", "backend", "MPiJ.gif")
        os.startfile(gif_path) #надо вставить видео с загрузкой и оплатой

        # Формируем полный путь к аудиофайлу
        audio_path = os.path.join(current_dir,"RS", "backend", "Voiceovers", "oplata_50.mp3")
        os.startfile(audio_path) #это озвучка

class Informations:
    pass

class Tickets:
    pass


