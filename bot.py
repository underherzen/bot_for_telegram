import config
import telebot
import parsing
from telebot import types
bot = telebot.TeleBot(config.token)
mas = parsing.mas

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, 'Привет! Я -- бот для получения расписания в РГПУ им. Герцена')
    bot.send_message(message.chat.id, 'Чтобы получить инструкцию, как получить расписание своей группы, напишите /instr')
    bot.send_message(message.chat.id, 'Нажми /list чтобы получить список групп')

    bot.send_message(message.chat.id, 'Если же лень писать полностью свою группу, можешь просто перейти на страницу с расписанием всех факультетов и институтов ')
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Расписание", url="https://guide.herzen.spb.ru/static/schedule.php")
    keyboard.add(url_button)
    bot.send_message(message.chat.id, "Кликни по кнопочке снизу", reply_markup=keyboard)
@bot.message_handler(commands=['list'])
def get_list(message):
    for name in mas:
        bot.send_message(message.chat.id, name[0])
@bot.message_handler(commands=['instr'])
def get_instr(message):
    bot.send_message(message.chat.id, 'Сначала вы пишите ступень образования, курс, название группы')
    bot.send_message(message.chat.id, 'Пример: магистратура, 2 курс, группа А')
@bot.message_handler(content_types=["text"])
def handle_text_doc(message):
    for name in mas:
        if(name[0].find(message.text)>-1):
            bot.send_message(message.chat.id, name[1])


if __name__ == '__main__':
     bot.polling(none_stop=True)