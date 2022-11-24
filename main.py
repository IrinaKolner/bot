# pip install pytelegrambotapi
# сам бот -> Cur_conv_bot

import telebot
from telebot import types

from config import *
from extensions import Converter, ApiException


def create_markup(base=None):
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    buttons = []
    for val in exchanges.keys():
        if val != base:
            buttons.append(types.KeyboardButton(val.capitalize()))

    markup.add(*buttons)
    return markup


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help', 'go'])
def start(message: telebot.types.Message):
    text = 'Здравствуйте. Список команд: \n/values - список доступных валют \n/convert - конвертировать одну валюту в другую'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(commands=['convert'])
def values(message: telebot.types.Message):
    text = 'Выберите валюту, из которой конвертировать: '
    bot.send_message(message.chat.id, text, reply_markup=create_markup())
    bot.register_next_step_handler(message, base_handler)

def base_handler(message: telebot.types.Message):
    base = message.text.strip().lower()
    text = 'Выберите валюту, в которую конвертировать: '
    bot.send_message(message.chat.id, text, reply_markup=create_markup(base))
    bot.register_next_step_handler(message, sym_handler, base)

def sym_handler(message: telebot.types.Message, base):
    sym = message.text.strip()
    text = 'Выберите количество конвертируемой валюты: '
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, base, sym)

def amount_handler(message: telebot.types.Message, base, sym):
    amount = message.text.strip()
    try:
        new_price = Converter.get_price(base, sym, amount)
    except ApiException as e:
        bot.send_message(message.chat.id, f'Ошибка в конвертации: \n{e}')
    else:
        text = f'Цена {amount} {base} в {sym}: {new_price}'
        bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['voice'])
def voice_reaction(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'Красивый голос^_^')


@bot.message_handler(content_types=['photo'])
def photo_reaction(message: telebot.types.Message):
    pic = 'https://i.pinimg.com/236x/a1/ce/ac/a1ceac569886aefede76c412f015b237.jpg'
    bot.send_message(message.chat.id, pic)



bot.polling()
