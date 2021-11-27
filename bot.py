import telebot
import csv
from telebot import types
from MyToken import token

bot = telebot.TeleBot(token)

entry = {}

inline_keyboard = types.InlineKeyboardMarkup()
btn1 = types.InlineKeyboardButton('Доход', callback_data='income')
btn2 = types.InlineKeyboardButton ('Расход', callback_data='costs')
inline_keyboard.add(btn1, btn2)

@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    user = f'Имя пользователя: {message.from_user.last_name}, Фамилия пользователя: {message.from_user.first_name}'
    bot.send_message(chat_id, "Привет Сделайте Выбор", reply_markup=inline_keyboard)


@bot.callback_query_handler(func=lambda c: True)
def inline(c):
    if c.data == 'income':
        chat_id = c.message.chat.id
        income_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        k1 = types.KeyboardButton('Работа')
        k2 = types.KeyboardButton('Фриланс')
        k3 = types.KeyboardButton('Другое')
        income_keyboard.add(k1,k2,k3)
        msg = bot.send_message(chat_id, 'Выберите категорию', reply_markup=income_keyboard)
        bot.register_next_step_handler(msg, get_category_income)

    if c.data == 'costs':
        chat_id = c.message.chat.id
        costs_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        k1 = types.KeyboardButton('Еда')
        k2 = types.KeyboardButton('Одежда')
        k3 = types.KeyboardButton('Развлечение')
        costs_keyboard.add(k1,k2,k3)
        msg = bot.send_message(chat_id, 'Выберите категорию', reply_markup=costs_keyboard)
        bot.register_next_step_handler(msg, get_category_costs)
    
def get_category_income(message):
    chat_id = message.chat.id
    entry.update({'category': message})
    msg_ = bot.send_message(chat_id, 'Укажите Сумму')
    bot.register_next_step_handler(msg_, get_sum_income)



def get_category_costs(message):
    chat_id = message.chat.id
    entry.update({'category': message})
    msg_ = bot.send_message(chat_id, 'Укажите Сумму')
    bot.register_next_step_handler(msg_, get_sum_costs)


def get_sum_income(message):
    chat_id = message.chat.id
    entry.update({'sum': message})

    file_name = 'income.csv'

    with open(file_name, 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow((entry['category'], entry['sum']))
    
    bot.send_message(chat_id, "Ваши доходы добавлены", reply_markup=inline_keyboard)



def get_sum_costs(message): 
    chat_id = message.chat.id
    entry.update({'sum': message})

    file_name = 'costs.csv'

    with open(file_name, 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow((entry['category'], entry['sum']))
    
    bot.send_message(chat_id, "Ваши расходы добавлены", reply_markup=inline_keyboard)



bot.polling()

