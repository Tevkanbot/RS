from .data import Data
from .commands import Buy, Informations, Tickets

class Trigger:
                
    def search_trigger(phrase): #ищем снала анктивационное слово, затем тригеры во фразе
        
        phrase = phrase.split() # Разделяем фразу на слова

        print("splited: ", phrase)

        data = Data.load() # Загружаем данные, в особенности тригерные слова

#----------------- Снача ищем двуСловные тригеры--------------------------------------------------------------------
        twoWordsTriggers = data["TwoWordsTriggers"]
        #print(twoWordsTriggers)

        num = 0

        for TWTList in twoWordsTriggers: # Перебираем все двуСловные тригеры

            TWTList = TWTList.split() # Превращаем двуСловный тригер в список
            #print (TWTList)
            for trigWord in TWTList: # Перебираем все тригеры(слова) из двуСловного тригера

                for word in phrase: # Перебираем все слова в фразе

                    if trigWord == word: # Если нашли совпадение


                        print("Первый из 2 тригеров найден!")
                        copy = TWTList.copy()

                        #TWTList.remove(trigWord)
                        
                        TWTList.remove(trigWord)
                        
                        remainWord = TWTList.pop(0)

                        for word in phrase:
                            if word == remainWord: #TWTList.pop(0)
                                print("Второй из 2 тригеров найден----", copy)
                                return {"WordCount": 2, "trigger": " ".join(copy), "num": num}
            

                                                                                                            

                        
#----------------Потом одноСловные тригеры---------------------------------------------------------

        for word in phrase:
            for trigger in data["OneWordTriggers"]:
                if trigger == word:
                    return {"WordCount": 1, "trigger": word, "num": num}
                else:
                    return {"WordCount": 0}    
        

    def search_number(fromSearch, phrase):

        print(fromSearch)#

        phrase = phrase.split()
        num = 0
        num_words = ["ноль", "один","два","три","четыре","пять","шесть","семь","восемь","девять"]

        if fromSearch["WordCount"] != 0: 
            for word in phrase:
                if word.isdigit(): 
                             
                    num = int(word)
                    break
                else:
                    #
                    for el in num_words:
                        if word == el:
                            num = el.index(el)
            fromSearch["num"] = num
            print("fr", fromSearch)#
            return fromSearch

        else:
            return fromSearch


    def work(fromReturn):

        data = Data.load()
        
        print(fromReturn)

        trigWord = fromReturn["trigger"]
        
        num = fromReturn["num"]
        if fromReturn["WordCount"] == 1:
            exec(data["OneWordActions"][trigWord]["command"])

            #print("я запустиль:", trigWord, ">>>", data["OneWordActions"][trigWord]["command"])

        if fromReturn["WordCount"] == 2:
            exec(data["TwoWordsActions"][trigWord]["command"])

            #print("я запустиль:", trigWord, ">>>", data["TwoWordsActions"][trigWord]["command"])