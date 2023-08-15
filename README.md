python3 -m venv venv && . venv/bin/activate python -m pip install --upgrade pip python -m pip install -r requirements.txt

при SQLITE просто python3 manage.py runserver из папки chart


в папке chart пример файла .env для доступа к БД

python manage.py migrate выполнить миграции и должно работать

python3 manage.py runserver
