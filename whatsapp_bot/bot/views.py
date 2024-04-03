from twilio.rest import Client
from datetime import datetime
from .models import Reminder

# Инициализация бота
account_sid = 'YOUR_ACCOUNT_SID'
auth_token = 'YOUR_AUTH_TOKEN'
bot_number = ''
client = Client(account_sid, auth_token)

def say_hi(author):
    msg = f'Добрый день, {author}! если хотите создать напоминание, то напишите сообщение в формате ...'
    client.messages.create(
        body=msg,
        from_=f'whatsapp:{bot_number}',
        to=f'{author}'
    )

def add_reminder(author, text, time):
    try:
        Reminder.objects.create(author=author, text=text, time=time)
    except Exception as error:
        return f'Напоминание не сохранено.{error}'
    return 'напоминание успешно создано'


def send_msg(author, time):
    resiver = Reminder.objects.get(author=author, time=time).author
    msg = Reminder.objects.get(author=author, time=time).text
    message = client.messages.create(
                             body=msg,
                             from_=f'whatsapp:{bot_number}',
                             to=f'whatsapp:{resiver}'
                         )
    print(f"Reminder sent: {message.sid}")


def reminder_list(author):
    rm_lst = Reminder.objects.filter(author=author)
    for rm in rm_lst:
        print(rm.time, ':', rm.text)


def rm_delete(author, time):
    try:
        Reminder.objects.get(author=author, time=time).delete()
    except Exception as error:
        return f'проблемы при удалении. {error}'
    return 'Напоминание удалено'


def bot(request):
    sender_number = request.POST['From']
    body = request.POST['Body']
    sender_name = request.POST['ProfileName']
    if body == 'hi':
        say_hi(sender_name)
    elif 'add' in body:
        cmnd, rm, time_rm = body.split(' ')
        add_reminder(
            sender_number,
            rm,
            datetime.datetime.strptime(time_rm, '%Y-%m-%d %H:%M')
        )
    elif body == 'list':
        reminder_list(sender_number)
    elif 'delete' in body:
        time_rm = body.split(' ')[1]
        rm_delete(sender_number, time_rm)
    if Reminder.objects.filter(time=datetime.now()).exists():
        send_msg(sender_number, datetime.now())






'''# Подключение к базе данных для хранения напоминаний
conn = sqlite3.connect('reminders.db')
c = conn.cursor()
c.execute(CREATE TABLE IF NOT EXISTS reminders (id INTEGER PRIMARY KEY, time TEXT, message TEXT, recurring INTEGER))
conn.commit()

# Функция для добавления напоминания в базу данных
def add_reminder(time, message, recurring):
    c.execute('INSERT INTO reminders (time, message, recurring) VALUES (?, ?, ?)', (time, message, recurring))
    conn.commit()

# Функция для отправки уведомления на указанное время
def send_notification(time, message):
    current_time = datetime.now().strftime('%H:%M')
    if current_time == time:
        message = client.messages \
                        .create(
                             body=message,
                             from_='whatsapp:+14155238886',
                             to='whatsapp:<YOUR_PHONE_NUMBER>'
                         )
        print(f"Reminder sent: {message.sid}")

# Функция для отображения списка текущих напоминаний
def list_reminders():
    c.execute('SELECT * FROM reminders')
    reminders = c.fetchall()
    for reminder in reminders:
        print(reminder)

# Функция для удаления конкретного напоминания
def delete_reminder(id):
    c.execute('DELETE FROM reminders WHERE id=?', (id,))
    conn.commit()

# Функция для управления напоминаниями через команды бота
def handle_command(command):
    if command == 'list':
        list_reminders()
    elif command.startswith('delete'):
        parts = command.split(' ')
        id = parts[1]
        delete_reminder(id)
    # Другие команды...

# Пример использования
add_reminder('12:00', 'Meeting', 0)  # Добавляем напоминание в базу данных
send_notification('12:00', 'Meeting')  # Отправляем уведомление
handle_command('list')  # Отображаем список текущих напоминаний'''
