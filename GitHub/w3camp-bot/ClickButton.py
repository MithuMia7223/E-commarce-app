from telebot import TeleBot
from config import API_TOKEN
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from db import init_database, add_user, add_message, add_button_click

init_database()

bot = TeleBot(API_TOKEN)


button1 = InlineKeyboardButton(text="Button1", callback_data="btn1")
button2 = InlineKeyboardButton(text="Button2", callback_data="btn2")
inline_keyboard = InlineKeyboardMarkup(row_width=2)
inline_keyboard.add(button1, button2)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    add_user(
        message.chat.id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name,
    )
    bot.send_message(
        message.chat.id, "Welcome to the Bot!", reply_markup=inline_keyboard
    )


@bot.callback_query_handler(func=lambda call: True)
def check_button(call):
    if call.data == "btn1":
        add_button_click(call.message.chat.id, "Button1")
        bot.answer_callback_query(call.id, "Btn1 is pressed.", show_alert=True)

    elif call.data == "btn2":
        add_button_click(call.message.chat.id, "Button2")
        bot.answer_callback_query(call.id, "Btn2 is pressed")


bot.polling()
