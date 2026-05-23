from config import API_TOKEN
import telebot

bot = telebot.TeleBot(token=API_TOKEN)


user_id = []


@bot.message_handler(commands=["start"])
def welcome(message):
    bot.send_message(message.chat.id, "welcome to w3camp bot.")
    if message.chat.id not in user_id:
        user_id.append(message.chat.id)


@bot.message_handler(commands=["Update"])
def send_update(message):
    for id in user_id:
        bot.send_message(id, "A new product is available")


@bot.message_handler(regexp="2024")
def handle_message(message):
    bot.reply_to(message, "This message contains 2024")


def text_message(message):
    return message.document.mime_type == "text/plain"


@bot.message_handler(func=text_message, content_types="document")
def handle_text_doc(message):
    bot.reply_to(message, "This a text file .")


@bot.message_handler(commands=["start"])
def send_start(message):
    bot.reply_to(message, "Emoji or start")


@bot.message_handler(func=lambda m: "😂" in m.text)
def send_emoji(message):
    bot.reply_to(message, "Emoji or start")


bot.polling()
