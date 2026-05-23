from telebot import TeleBot
from config import API_TOKEN
from telebot.types import ReplyKeyboardMarkup
from db import init_database, add_user, add_message, add_button_click

init_database()

bot = TeleBot(API_TOKEN)

reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
reply_keyboard.add("Button1", "Button2")


@bot.message_handler(commands=["start"])
def send_welcome(message):
    add_user(
        message.chat.id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name,
    )
    bot.send_message(
        message.chat.id, "check the following keyboard", reply_markup=reply_keyboard
    )


@bot.message_handler(func=lambda message: True)
def check_button(message):
    if message.text == "Button1":
        add_button_click(message.chat.id, "Button1")
        add_message(message.chat.id, message.text, "button")
        bot.send_message(message.chat.id, "Button1 is pressed .")
    elif message.text == "Button2":
        add_button_click(message.chat.id, "Button2")
        add_message(message.chat.id, message.text, "button")
        bot.send_message(message.chat.id, "Button2 is pressed")
    else:
        add_message(message.chat.id, message.text, "text")
        bot.send_message(
            message.chat.id,
            f"Your message is :<b>{message.text}</b>, ",
            parse_mode="HTML",
        )


bot.polling()
