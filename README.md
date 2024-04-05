# Watsapp_Reminder
## Описание

Бот позволяет:
- сохранять напоминания;
- удалять напоминания;
- получать список напоминаний;
- Получать уведомление о напоминаниях;

## Стек технологий
- Python 3.11
- Django 3.2
- twilio 9.0

## Запуск проекта
Клонировать репозиторий:
```
git@github.com:Glebchik57/whatsapp_bot_for_bb.git
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py makemigrations
```

```
python3 manage.py migrate
```
Зарегистрируйтесь на сайте www.twilio.com

Создайте в приложении bot файл .env и добавьте следующие переменные:
```
SID = 'YOUR_ACCOUNT_SID'
TOKEN = 'YOUR_AUTH_TOKEN'
NUMBER = 'YOUR_NUMBER'
```
На сайте twillio перейдите в настройки чата и пропишите адрес своего django сервиса

Запукстить проект:

```
python3 manage.py runserver
```
## Работа с чатом

Для добавления напоминания напишите в чат сообщение следующего формата:
```
add ВАШЕ_СООБЩЕНИЕ ДАТА_И_ВРЕМЯ_В_ФОРМАТЕ(YYYY-MM-DD HH:MM.) 
```

Для запроста всего списка напоинаний, напишите в чат команду:
```
list
```
Для удаления напоминания напишите сообщение в чат следующего формата:
```
delete ДАТА_И_ВРЕМЯ_В_ФОРМАТЕ(YYYY-MM-DD HH:MM.) 
```

## Автор
[Sevostyanov Gleb](https://github.com/Glebchik57)
