## Проект Блогикум

Блогикум - учебный проект для Яндекс Практикум. Реализация Backend для простого блога с во

### Технологии:

Pytho 3.9, Django 3.2, SQLLite

### Как запустить проект:

- Клонировать репозиторий:
```
https://github.com/AntonSerebryakov/[Blogicum]
```

- Перейти в скипированную папку:

```
cd anfisa2sprint
```

Cоздать и активировать виртуальное окружение:

Windows
```
python -m venv venv
source venv/Scripts/activate
```
Linux/macOS
```
python3 -m venv venv
source venv/bin/activate
```

Обновить PIP

Windows
```
python -m pip install --upgrade pip
```
Linux/macOS
```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

Windows
```
python manage.py makemigrations
python manage.py migrate
```

Linux/macOS
```
python3 manage.py makemigrations
python3 manage.py migrate
```

Запустить проект:

Windows
```
python manage.py runserver
```

Linux/macOS
```
python3 manage.py runserver
```

Просмотр контента:

```
Перейти по адресу http://127.0.0.1:8000/.
```
