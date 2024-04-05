import os

from twilio.rest import Client
from datetime import datetime
from dotenv import load_dotenv
from django.core.exceptions import ObjectDoesNotExist

from .models import Reminder

load_dotenv()

account_sid = os.getenv('SID')
auth_token = os.getenv('TOKEN')
bot_number = os.getenv('NUMBER')

client = Client(account_sid, auth_token)


def add_reminder(author, text, time):
    '''Добавление Напоминания'''
    try:
        Reminder.objects.create(author=author, text=text, time=time)
    except Exception as error:
        print(f'Напоминание не сохранено. {error}')
    print('Напоминание успешно создано')


def send_msg(author, time):
    '''Отправка сообщения в чат'''
    reminder = Reminder.objects.get(author=author, time=time)
    message = client.messages.create(
                             body=reminder.text,
                             from_=f'whatsapp:{bot_number}',
                             to=f'whatsapp:{author}'
                         )
    print(f"Reminder sent: {message.sid}")


def reminder_list(author):
    '''Отправка списка всех напоминаний'''
    reminders = Reminder.objects.filter(author=author)
    for reminder in reminders:
        message = client.messages.create(
                             body=f'{reminder.time}:{reminder.text}',
                             from_=f'whatsapp:{bot_number}',
                             to=f'whatsapp:{author}'
                         )
        print(f"Reminder sent: {message.sid}")


def rm_delete(author, time):
    '''Удаление напоминания'''
    try:
        Reminder.objects.get(author=author, time=time).delete()
    except ObjectDoesNotExist:
        print('Напоминание не существует')
    print('Напоминание удалено')


def bot(request):
    '''Основная логика работы бота'''
    sender_number = request.POST['From']
    body = request.POST['Body']
    custom_message = body.split(' ')
    if 'add' in body:
        if len(custom_message) != 3:
            raise ValueError('Запрос не соответсвует формату')
        else:
            reminder_text, time_str = custom_message[1:]
            try:
                time = datetime.strptime(time_str, '%Y-%m-%d %H:%M')
                add_reminder(sender_number, reminder_text, time)
            except ValueError:
                print('Некорректный формат времени')
    elif body == 'list':
        reminder_list(sender_number)
    elif 'delete' in body:
        if len(custom_message) != 2:
            raise ValueError('Запрос не соответсвует формату')
        else:
            time_to_delete = custom_message[1]
            rm_delete(sender_number, time_to_delete)
    if Reminder.objects.filter(time=datetime.now()).exists():
        send_msg(sender_number, datetime.now())
