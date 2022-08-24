## Установка

1. Клонировать репозиторий
2. `pip install -r requirements.txt`
3. `python main.py`

Приложение будет развернуто на локальном сервере `localhost:5000`

## API

1. Регистрация - POST `localhost:5000/api/register`, аргументы email, password
2. Авторизация - POST `localhost:5000/api/login`, аргументы email, password
3. Выход - GET `localhost:5000/api/logout`
4. Получение данных - GET `localhost:5000/api/data`