from uuid import uuid4
import requests
import logging
import re
import paramiko
import os
import psycopg2

from psycopg2 import Error
from pathlib import Path
from dotenv import load_dotenv

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

dotenv_path = Path('data.env')
load_dotenv(dotenv_path=dotenv_path)

TOKEN = os.getenv('TOKEN')
host = os.getenv('HOST')
port = os.getenv('PORT')
username = os.getenv('USER')
password = os.getenv('PASSWORD')
username_db = os.getenv('USER_DB')
password_db = os.getenv('PASSWORD_DB')
database = os.getenv('DATABASE')
connection = None

# Подключаем логирование
logging.basicConfig(
    filename='logfile.txt', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

FIND_PHONE, PHONE = range(2)
FIND_EMAIL, EMAIL = range(2,4)

def get_release(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('cat /etc/os-release')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def get_uname(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('uname -a')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
 
def get_uptime(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('uptime')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
 
def get_df(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('df -h')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
 
def get_free(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('free')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
 
def get_mpstat(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('mpstat -P ALL')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
 
def get_w(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('w')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
 
def get_auths(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('last | head -10 ')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
 
def get_critical(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('journalctl -r -p crit -n 5')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
 
def get_ps(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('ps aux | head -10')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
 
def get_ss(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('ss -s')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
 
def get_apt_list_com(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('apt list --installed | head -10')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    update.message.reply_text("Хотите узнать информацию о конкретном пакете?(Для отмены введите \"нет\")")
    return 'get_apt_list'

def get_apt_list(update: Update, context):
    user_input = update.message.text
    if user_input == "нет":
        return ConversationHandler.END
    else:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=username, password=password, port=port)
        stdin, stdout, stderr = client.exec_command(f'apt list {user_input}')
        data = stdout.read() + stderr.read()
        client.close()
        data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
        update.message.reply_text(data)
        return ConversationHandler.END
    
def get_services(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('systemctl list-units | head -10')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def get_repl_logs(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('cat /var/log/postgresql/postgresql-15-main.log  | grep repl_user')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def get_phone_numbers(update: Update, context):
    try:
        connection = psycopg2.connect(user=username_db,
                                    password=password_db,
                                    host=host,
                                    port="5432", 
                                    database=database)

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM phone_numbers;")
        connection.commit() # сохранение изменений
        data = cursor.fetchall()
        result = []
        for row in data:
            result.append(row[1])
        update.message.reply_text("\n".join(result))
        logging.info("Команда успешно выполнена")
    except (Exception, Error) as error:
        logging.error("Ошибка при работе с PostgreSQL: %s", error)
    finally:
        if connection is not None:
            cursor.close()
            connection.close()

def get_emails(update: Update, context):
    try:
        connection = psycopg2.connect(user=username_db,
                                    password=password_db,
                                    host=host,
                                    port="5432", 
                                    database=database)

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM emails;")
        connection.commit() # сохранение изменений
        data = cursor.fetchall()
        result = []
        for row in data:
            result.append(row[1])
        update.message.reply_text("\n".join(result))
        logging.info("Команда успешно выполнена")
    except (Exception, Error) as error:
        logging.error("Ошибка при работе с PostgreSQL: %s", error)
    finally:
        if connection is not None:
            cursor.close()
            connection.close()
    
def findPhoneNumbersCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска телефонных номеров: ')

    return FIND_PHONE

def findPhoneNumbers (update: Update, context):
    user_input = update.message.text # Получаем текст, содержащий(или нет) номера телефонов

    phoneNumRegex = re.compile(r'(?:8|\+7)[ -]?\(?\d{3}\)?[ -]?\d{3}[ -]?\d{2}[ -]?\d{2}') # формат 8 (000) 000-00-00

    phoneNumberList = phoneNumRegex.findall(user_input) # Ищем номера телефонов

    key = "key_phone"
    context.user_data[key] = phoneNumberList

    if not phoneNumberList: # Обрабатываем случай, когда номеров телефонов нет
        update.message.reply_text('Телефонные номера не найдены')
        return ConversationHandler.END
    
    phoneNumbers = '' # Создаем строку, в которую будем записывать номера телефонов
    for i in range(len(phoneNumberList)):
        phoneNumbers += f'{i+1}. {phoneNumberList[i]}\n' # Записываем очередной номер

    update.message.reply_text(phoneNumbers)
    update.message.reply_text("Если желаете внести данные в базу введите 'да', в противном случае введите другое")
    return PHONE

def phone_db(update: Update, context):
    key = "key_phone"
    value = context.user_data.get(key, 'Not found')

    user_input = update.message.text
    if user_input == "да":
        try:
            connection = psycopg2.connect(user=username_db,
                                        password=password_db,
                                        host=host,
                                        port="5432", 
                                        database=database)
            cursor = connection.cursor()
            for i in range(len(value)):
                cursor.execute(f"INSERT INTO phone_numbers (number) VALUES ('{value[i]}');")
            connection.commit() # сохранение изменений
            logging.info("Команда успешно выполнена")
            update.message.reply_text("Запись успешно внесена")
        except (Exception, Error) as error:
            logging.error("Ошибка при работе с PostgreSQL: %s", error)
            update.message.reply_text("При записи данных произошла ошибка")
        finally:
            if connection is not None:
                cursor.close()
                connection.close()
            return ConversationHandler.END
    else:
        return ConversationHandler.END

def findEmailCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска Email\'ов:' )

    return FIND_EMAIL

def findEmails (update: Update, context):
    user_input = update.message.text # Получаем текст, содержащий(или нет) номера телефонов

    # EmailNumRegex = re.compile(r'[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+\.ru|[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+\.com') 
    EmailNumRegex = re.compile(r'\b[a-zA-Z0-9_%+-]+(?<!\.\.)@[a-zA-Z0-9.-]+(?<!\.)\.[a-zA-Z]{2,}\b') 

    EmailNumberList = EmailNumRegex.findall(user_input) # Ищем номера телефонов

    key = "key_email"
    context.user_data[key] = EmailNumberList

    if not EmailNumberList: # Обрабатываем случай, когда номеров телефонов нет
        update.message.reply_text('Email\'ы не найдены')
        return ConversationHandler.END
    
    Emails = '' # Создаем строку, в которую будем записывать номера телефонов
    for i in range(len(EmailNumberList)):
        Emails += f'{i+1}. {EmailNumberList[i]}\n' # Записываем очередной номер
        
    update.message.reply_text(Emails) # Отправляем сообщение пользователю
    update.message.reply_text("Если желаете внести данные в базу введите 'да', в противном случае введите другое")
    return EMAIL

def email_db(update: Update, context):
    key = "key_email"
    value = context.user_data.get(key, 'Not found')

    user_input = update.message.text
    if user_input == "да":
        try:
            connection = psycopg2.connect(user=username_db,
                                        password=password_db,
                                        host=host,
                                        port="5432", 
                                        database=database)
            cursor = connection.cursor()
            for i in range(len(value)):
                cursor.execute(f"INSERT INTO emails (email) VALUES ('{value[i]}');")
            connection.commit() # сохранение изменений
            logging.info("Команда успешно выполнена")
            update.message.reply_text("Запись успешно внесена")
        except (Exception, Error) as error:
            logging.error("Ошибка при работе с PostgreSQL: %s", error)
            update.message.reply_text("При записи данных произошла ошибка")
        finally:
            if connection is not None:
                cursor.close()
                connection.close()
            return ConversationHandler.END
    else:
        return ConversationHandler.END

def verify_password_command(update: Update, context):
    update.message.reply_text('Введите пароль для проверки: ')
    return 'verify_password'
def verify_password (update: Update, context):
    user_input = update.message.text

    Regex = re.compile(r'(?=.*[0-9])(?=.*[!@#$%^&*()])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!@#$%^&*()]{8,}') 

    result = Regex.match(user_input) 

    if result:
        update.message.reply_text('Пароль сложный')
    else:
        update.message.reply_text('Пароль простой')
    return ConversationHandler.END

def start(update: Update, context):
    user = update.effective_user
    update.message.reply_text(f'Привет {user.full_name}!')

def helpCommand(update: Update, context):
    update.message.reply_text('Help!')
    

def echo(update: Update, context):
    update.message.reply_text(update.message.text)


def main():
		# Создайте программу обновлений и передайте ей токен вашего бота
    updater = Updater(TOKEN, use_context=True)

    # Получаем диспетчер для регистрации обработчиков
    dp = updater.dispatcher

    convHandlerFindPhoneNumbers = ConversationHandler(
        entry_points=[CommandHandler('find_phone_number', findPhoneNumbersCommand)],
        states={
            FIND_PHONE: [MessageHandler(Filters.text & ~Filters.command, findPhoneNumbers)],
            PHONE: [MessageHandler(Filters.text & ~Filters.command, phone_db)],
        },
        fallbacks=[]
    )
    convHandlerFindEmails = ConversationHandler(
        entry_points=[CommandHandler('find_email', findEmailCommand)],
        states={
            FIND_EMAIL: [MessageHandler(Filters.text & ~Filters.command, findEmails)],
            EMAIL: [MessageHandler(Filters.text & ~Filters.command, email_db)],
        },
        fallbacks=[]
    )
    convHandlerVerifyPass = ConversationHandler(
        entry_points=[CommandHandler('verify_password', verify_password_command)],
        states={
            'verify_password': [MessageHandler(Filters.text & ~Filters.command, verify_password)],
        },
        fallbacks=[]
    )
    convHandlerAPT = ConversationHandler(
        entry_points=[CommandHandler('get_apt_list', get_apt_list_com)],
        states={
            'get_apt_list': [MessageHandler(Filters.text & ~Filters.command, get_apt_list)],
        },
        fallbacks=[]
    )

		# Регистрируем обработчики команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", helpCommand))
    dp.add_handler(CommandHandler("get_release", get_release))
    dp.add_handler(CommandHandler("get_uname", get_uname))
    dp.add_handler(CommandHandler("get_uptime", get_uptime))
    dp.add_handler(CommandHandler("get_df", get_df))
    dp.add_handler(CommandHandler("get_free", get_free))
    dp.add_handler(CommandHandler("get_mpstat", get_mpstat))
    dp.add_handler(CommandHandler("get_w", get_w))
    dp.add_handler(CommandHandler("get_auths", get_auths))
    dp.add_handler(CommandHandler("get_critical", get_critical))
    dp.add_handler(CommandHandler("get_ps", get_ps))
    dp.add_handler(CommandHandler("get_ss", get_ss))
    dp.add_handler(CommandHandler("get_emails", get_emails))
    dp.add_handler(CommandHandler("get_phone_numbers", get_phone_numbers))
    dp.add_handler(convHandlerAPT)
    dp.add_handler(CommandHandler("get_services", get_services))
    dp.add_handler(CommandHandler("get_repl_logs", get_repl_logs))
    dp.add_handler(convHandlerFindPhoneNumbers)
    dp.add_handler(convHandlerFindEmails)
    dp.add_handler(convHandlerVerifyPass)
		
		# Регистрируем обработчик текстовых сообщений
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
		
		# Запускаем бота
    updater.start_polling()

		# Останавливаем бота при нажатии Ctrl+C
    updater.idle()


if __name__ == '__main__':
    main()
