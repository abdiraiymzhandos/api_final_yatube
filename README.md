# api_final
api final
Yatube API
Описание
Yatube API — это RESTful API для социальной сети блогеров, позволяющий пользователям делиться текстовыми постами, комментировать их, подписываться на других пользователей и просматривать сообщества. Этот проект предоставляет бэкенд и API-интерфейс для взаимодействия с платформой Yatube, где пользователи могут выражать свои мысли и идеи через публикации.

Технологии
Python 3.9
Django 3.2
Django REST Framework
Simple JWT - для аутентификации через JWT-токены
Установка
Для запуска проекта локально следуйте инструкциям:

Клонирование репозитория
bash
Copy code
git clone https://github.com/ваш_username/api_final_yatube.git
cd api_final_yatube
Настройка виртуального окружения
bash
Copy code
python -m venv venv
source venv/bin/activate  # Для Unix-подобных систем
venv\Scripts\activate     # Для Windows
Установка зависимостей
bash
Copy code
pip install -r requirements.txt
Выполнение миграций
bash
Copy code
python manage.py makemigrations
python manage.py migrate
Запуск проекта
bash
Copy code
python manage.py runserver
Использование
API поддерживает следующие эндпоинты:

/api/posts/ - GET, POST, PUT, DELETE для постов
/api/groups/ - GET для просмотра списка сообществ
/api/follow/ - GET, POST для подписок
/api/comments/ - GET, POST, PUT, DELETE для комментариев к постам
Аутентификация пользователей осуществляется через JWT-токены. Получить токен можно через эндпоинт /api/token/.

Примеры запросов
Пример POST запроса для создания нового поста:

bash
Copy code
curl -X POST http://localhost:8000/api/posts/ \
     -H 'Authorization: Bearer ваш_токен' \
     -d 'text=Пример текста поста'