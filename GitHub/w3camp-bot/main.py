from config import API_TOKEN
import telebot
from db import init_database, add_user, add_message

init_database()

bot = telebot.TeleBot(token=API_TOKEN)


@bot.message_handler(commands=["start"])
def start_message(message):
    add_user(
        message.chat.id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name,
    )
    bot.send_message(message.chat.id, "Please enter your name: ")
    bot.register_next_step_handler(message, process_name)


def process_name(message):
    name = message.text
    add_message(message.chat.id, message.text, "name")
    bot.send_message(message.chat.id, f"Hello {name}!\nHow old are you?")
    bot.register_next_step_handler(message, process_age)


def process_age(message):
    age = message.text
    add_message(message.chat.id, message.text, "age")
    bot.send_message(message.chat.id, f"You are {age} years old\nThank you.")


@bot.message_handler(func=lambda message: True)
def reply_func(message):
    if not message.text.startswith("/"):
        add_message(message.chat.id, message.text, "text")
        bot.reply_to(message, text="You message is replied !")


bot.polling()
