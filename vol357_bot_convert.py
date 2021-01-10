import telebot
from config import token, keys
from extensions import ExchangeException, Exchange

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start','help'])
def start(message: telebot.types.Message):
    text = '\n бот-Конвертер валют:' \
'\n - /help - вывести этот текст \
\n - /values - вывести список доступных валют\
\n - сконвертировать валюту, если наберешь: <имя валюты> <в какую валюту перевести>\
<количество переводимой валюты>'
    bot.send_message(message.chat.id, f"Welcome, {message.chat.username}! {text}")

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ExchangeException('Введите команду или 3 параметра')

        base, quote, amount = values
        #print(carr_from)
        total_text = Exchange.get_price(base, quote, amount)
    except ExchangeException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Что-то пошло не так с {e}')
    else:
       # text = f'Переводим из {base} в {quote}\n{amount} = {total_base}'
        text = f'Переводим из {base} в {quote}\n{total_text}'
        bot.send_message(message.chat.id, text)


bot.polling()
