import config
import telebot
import parsing
import working_in_db

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, 'Привет! Я -- бот для получения расписания в РГПУ им. Герцена 3 курс')
    bot.send_message(message.chat.id, 'Чтобы начать работу, тебе надо будет сначала написать свой институт или факультет')
    bot.send_message(message.chat.id, 'пример:')
    bot.send_message(message.chat.id, 'институт компьютерных наук и технологического образования:')
    bot.send_message(message.chat.id, 'Потом свою группу')
    bot.send_message(message.chat.id, 'пример:')
    bot.send_message(message.chat.id, 'бакалавриат, 3 курс, группа ИВТ ')
    bot.send_message(message.chat.id, 'А дальше уже день недели')
    bot.send_message(message.chat.id, 'Чтобы не ошибиться в написании института и факультета, пройди по ссылке')
    bot.send_message(message.chat.id, 'https://guide.herzen.spb.ru/static/schedule.php')

    bot.send_message(message.chat.id, 'Дополнительная информация тут /info')
    working_in_db.isExist(message.chat.id, 'Кык')
@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id, 'Чтобы изменить свою группу или факультет, просто напиши их названия, и все будет готово :)')
    bot.send_message(message.chat.id, 'Чтобы посмотреть, по какой группе и факультету ты получаешь расписание, нажми /show')
@bot.message_handler(commands=['show'])
def show_info(message):
    rows = working_in_db.show_info(message.chat.id)
    for row in rows:
        if(row is not None):
            bot.send_message(message.chat.id, row)
        else:
            bot.send_message(message.chat.id, 'Не заполнено поле')
@bot.message_handler(content_types=["text"])
def handle_text_doc(message):
    #parsing.chat_id(message.chat.id)
    mas_of_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    mas_of_days_rus = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота']
    word = message.text
    check = 0
    for day in mas_of_days_rus:
        day = day.lower()
        word = word.lower()
        if(word.find(day)>-1):
            check = 1
    if(check == 1):
        dayofweek = parsing.get_day(word)
        dayofweek = dayofweek.lower()
        print(dayofweek)
        try:
            raspisanie = parsing.get_raspisanie_na_den(dayofweek, message.chat.id)
            bot.send_photo(message.chat.id, raspisanie)
        except ValueError:
            bot.send_message(message.chat.id, 'Произошла ошибочка. Удотовертесь в том, что факультет\институт и Ваша группа соответствуют друг другу')
            bot.send_message(message.chat.id, 'Выполните /show, чтобы посмотреть Вашу группу и институт\факультет')
    else:
       # working_in_db.isExist(chat_id, word)
        word = word.lower()
        check = working_in_db.isExist(message.chat.id, word)
        print(check)
        if(len(check)>0):
            bot.send_message(message.chat.id, check)
    print(message.chat.id)




if __name__ == '__main__':
     bot.polling(none_stop=True)