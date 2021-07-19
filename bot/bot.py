
import telebot
from telebot import types

bot = telebot.TeleBot('1921418522:AAGhuuELsBbOeby0OcjyjlGO5lqAbypl30c')


@bot.message_handler(commands=["geo"])
def geo(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(
        text="Отправить местоположение", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(
        message.chat.id, "Привет! Нажми на кнопку и передай мне свое местоположение", reply_markup=keyboard)


@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        print(message.location)
        print("latitude: %s; longitude: %s" %
              (message.location.latitude, message.location.longitude))


bot.polling()
