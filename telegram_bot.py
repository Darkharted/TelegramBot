from abc import get_cache_token
from os import write
from six import byte2int
import telebot
import csv
from telebot import types
from MyToken import token

bot = telebot.TeleBot(token)

entry = {}

inline_keyboard = types.InlineKeyboardMarkup()
btn1 = types.InlineKeyboardButton('Большую', callback_data='income')
btn2 = types.InlineKeyboardButton ('Маленькую', callback_data='costs')
inline_keyboard.add(btn1, btn2)

@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Какую вы хотите пиццу? Большую или маленькую?", reply_markup=inline_keyboard)


@bot.callback_query_handler(func=lambda c: True)
def inline(c):
    if c.data == 'income':
        chat_id = c.message.chat.id
        income_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        k1 = types.InlineKeyboardButton('Картой', callback_data='cartai')
        k2 = types.KeyboardButton('Наличкой')
        income_keyboard.add(k1,k2)
        msg = bot.send_message(chat_id, 'Как вы будете платить??', reply_markup=income_keyboard)
        bot.register_next_step_handler(msg, get_category_income)

    if c.data == 'costs':
        chat_id = c.message.chat.id
        costs_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        k1 = types.InlineKeyboardButton('Картой', callback_data='cartai')
        k2 = types.KeyboardButton('Наличкой')
        costs_keyboard.add(k1,k2)
        msg = bot.send_message(chat_id, 'Как вы будете платить?', reply_markup=costs_keyboard)
        bot.register_next_step_handler(msg, get_category_costs)
        print(c)


def get_category_income(message):
    chat_id = message.chat.id
    entry.update({'category': message})
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes1')
    key_no= types.InlineKeyboardButton(text='Нет', callback_data='no1')
    keyboard.add(key_yes, key_no)
    msg_ = bot.send_message(chat_id, f'Вы хотите большую пиццу, оплата - {message.text}?', reply_markup=keyboard)
    bot.register_next_step_handler(msg_, get_sum_income)




def get_category_costs(message):
    chat_id = message.chat.id
    entry.update({'category': message})
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes1')
    key_no= types.InlineKeyboardButton(text='Нет', callback_data='no1')
    keyboard.add(key_yes, key_no)
    msg_ = bot.send_message(chat_id, f'Вы хотите маленькую пиццу, оплата - {message.text}?', reply_markup=keyboard)


    bot.register_next_step_handler(msg_, get_sum_costs)



def get_sum_income(message):
    chat_id = message.chat.id
    entry.update({'sum': message})

    file_name = 'income.csv'

    with open(file_name, 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow((entry['category'], entry['sum']))
    
    bot.send_message(chat_id, "Спасибо за заказ")


def get_sum_costs(message): 
    chat_id = message.chat.id
    entry.update({'sum': message})

    file_name = 'costs.csv'

    with open(file_name, 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow((entry['category'], entry['sum']))
    
    bot.send_message(chat_id, "Спасибо за заказ")




bot.polling()

