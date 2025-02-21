# Создать виртуальное окружение
python -m venv .server_venv

# Активировать виртуальное окружение
.\.server_venv\Scripts\activate

# Обновить pip до последней версии
python.exe -m pip install --upgrade pip

# Установить зависимости из requirements.txt
python -m pip install -r requirements.txt

# Запустить сервер
py -m api_server --test