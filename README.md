# Установите все зависимости
pip install -r requirements.txt

# Запустите сервер
убедитесь что находитесь в директории с файлом manage.py если нет, то
cd .\task_manager\
и запуск сервера
python manage.py runserver
По умолчанию, сервер будет доступен по адресу http://127.0.0.1:8000/. 
http://127.0.0.1:8000/api/tasks/ чтобы создать таску
Возможно придется выполнить миграции 
python manage.py makemigrations
python manage.py migrate

# Запуск тестов
python manage.py test