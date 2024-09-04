import json 


data = {} # рабочий словарь

with open("C:/RS/backend/ticket.json", "r+", encoding="utf-8") as file:
    data = json.load(file)

print(data)

