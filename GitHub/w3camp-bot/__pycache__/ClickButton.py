from telebot import TeleBot
from config import API_TOKEN
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

bot = TeleBot(API_TOKEN)


button1 = InlineKeyboardButton(text="Button1", callback_data="btn1")
button2 = InlineKeyboardButton(text="Button2", callback_data="btn2")
inlline_keyboard = InlineKeyboardMarkup(row_width=2)
inlline_keyboard.add(button1, button2)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Welcome to the Bot!", reply_markup= inlline_keyboard)


@bot.callback_query_handler(func=lambda call: True)
def check_button(call):
    if call.data =="btn1":
        bot.answer_callback_query(call.id, "Btn1 is prssed.", show_alert=True)

    elif call.data =="btn2":
        bot.answer_callback_query(call.id, "Btn2 is pressed")

        


bot.polling()


