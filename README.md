# Сайт Foodgram «Продуктовый помощник». Дипломный проект учебного курса Яндекс.Практикум.

![example event parameter](https://github.com/Alexandra1624/foodgram-project-react/actions/workflows/yamdb_workflow.yml/badge.svg?event=push)
## _Описание_
Написан онлайн-сервис и API для него. На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов в pdf формате, необходимых для приготовления одного или нескольких выбранных блюд.


Для приложения **Foodgram** (https://github.com/Alexandra1624/foodgram-project-react) настроены Continuous Integration и Continuous Deployment. Реализовано:
- проверка кода на соответствие стандарту **PEP8** (с помощью пакета **flake8**);
- сборка и доставка докер-образа для контейнера **backend** на **Docker Hub**;
- автоматический деплой проекта на боевой сервер;
- отправка уведомления в **Telegram** о том, что процесс деплоя успешно завершился.

## Технологии
- Python 3.7.9
- Django 3.2.15
- Django Rest Framework 3.13.1
- Djangorestframework Simplejwt 4.8.0
- PostgreSQL 13.0
- gunicorn 20.0.4
- nginx 1.21.3

## Установка
1. **Клонируйте репозиторий:**
```sh
git clone https://github.com/Alexandra1624/foodgram-project-react

```

2. **Перейдите в папку infra. Создайте файл .env с переменными окружения для работы с базой данных:**
```sh
SECRET_KEY=secret_key # секретный ключ для работы settings.py
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
```

3. **Запустите создание образов и развертывание контейнеров:**
```sh
sudo docker-compose up -d
```
4. **Создайте миграции:**
```sh
sudo docker-compose exec backend python manage.py makemigrations --no-input
```
5. **Примените миграции:**
```sh
sudo docker-compose exec backend python manage.py migrate --no-input
```
6. **Соберите статику:**
```sh
sudo docker-compose exec backend python manage.py collectstatic --no-input
```
7. **Создайте суперпользователя:**
```sh
sudo docker-compose exec backend python manage.py createsuperuser
```
8. **Добавьте тэги и ингридиенты в БД:**
```sh
sudo docker-compose exec backend python manage.py tags
sudo docker-compose exec backend python manage.py ingr
```

Локально сервер запущен на странице:     
http://localhost/             
Страница администратора:            
http://localhost/admin          
Спецификация и эндпоинты доступны в документации:       
http://localhost/api/docs/redoc.html

## Автор

**_Александра Радионова_**      
https://github.com/Alexandra1624        
https://t.me/alexandra_R1624            
sashamain@yandex.ru