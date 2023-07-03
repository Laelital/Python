import telebot
from config import keys, TOKEN
from exception import ConvertionException, ValueConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['help', 'start'])
def help_start(message: telebot.types.Message):
    text = 'Чтобы воспользоваться ботом, введите команду в следующем виде: ' \
           '\n<имя валюты, цену которой хотите узнать> ' \
           '\n<имя валюты, в которую нужно перевести> ' \
           '\n<количество переводимой валюты> \nУвидеть список доступных валют: /values'

    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Неверное количество параметров.')

        quote, base, amount = values
        total_base = ValueConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
