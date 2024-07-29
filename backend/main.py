from voise import Voise
from triggers import Trigger

#import os
#from data import Data
#from commands import Audio

def main():

    while True:
        phrase = Voise.get_phrase()
        print("phrase: ", phrase)#

        print(phrase.split()) 

        tr = Trigger.search_trigger(phrase)
        print("tr: ", tr)#

        res = Trigger.search_number(tr, phrase)
        print("res: ", res)#
        
        if res["WordCount"] != 0:
            Trigger.work(res)

            

if __name__ == "__main__":
    main()


