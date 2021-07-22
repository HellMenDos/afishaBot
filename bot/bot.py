
import urllib
import telebot
from aiogram import types
import requests
import aiogram.utils.markdown as fmt

bot = telebot.TeleBot('*')


@bot.message_handler(commands=["start", "back", "drinks"])
def start(message):
    response = requests.get(
        'http://127.0.0.1:8000/api/user/check/{}'.format(message.chat.id))

    if response.json()['have']:
        markup = types.ReplyKeyboardMarkup(True, True)
        search = types.KeyboardButton('Поиск мероприятия')
        game = types.KeyboardButton('Игра «Угадай комика»')
        setting = types.KeyboardButton('Мой профиль')
        title = 'Привет, чего ты хочешь ?'
        markup.add(search, game, setting)
    else:
        markup = types.ReplyKeyboardMarkup(True, True)
        cities = requests.get('http://127.0.0.1:8000/api/city/get/').json()
        for i in range(0, len(cities)):
            markup.add(types.KeyboardButton(cities[i]['name']))
        markup.add(types.KeyboardButton('Другое'))

        title = 'Выбери город'

    bot.send_message(
        message.chat.id, title, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'на главную':
        response = requests.get(
            'http://127.0.0.1:8000/api/user/check/{}'.format(message.chat.id))

        if response.json()['have']:
            markup = types.ReplyKeyboardMarkup(True, True)
            search = types.KeyboardButton('Поиск мероприятия')
            game = types.KeyboardButton('Игра «Угадай комика»')
            setting = types.KeyboardButton('Мой профиль')
            title = 'Привет, чего ты хочешь ?'
            markup.add(search, game, setting)
        else:
            markup = types.ReplyKeyboardMarkup(True, True)
            cities = requests.get('http://127.0.0.1:8000/api/city/get/').json()
            for i in range(0, len(cities)):
                markup.add(types.KeyboardButton(cities[i]['name']))
            markup.add(types.KeyboardButton('Другое'))

            title = 'Выбери город'

        bot.send_message(
            message.chat.id, title, reply_markup=markup)

    if message.text.lower() == 'другое':
        cities = requests.get('http://127.0.0.1:8000/api/city/get/').json()
        cityText = ''
        markup = types.ReplyKeyboardMarkup(True, True)
        for i in range(0, len(cities)):
            if i == (len(cities)-2):
                cityText += cities[i]['name'] + ' и '
            else:
                cityText += cities[i]['name'] + ' , '
            markup.add(types.KeyboardButton(cities[i]['name']))
        markup.add(types.KeyboardButton('Другое'))
        bot.send_message(message.chat.id, 'К сожалению я пока ищу только в {} но это ненадолго. Напиши из какого ты города и я уведомлю, когда смогу тебе помогать.'.format(
            cityText), reply_markup=markup)

    if message.text.lower() == 'поиск мероприятия':
        markup = types.ReplyKeyboardMarkup(True, True)
        tooday = types.KeyboardButton('Сегодня')
        toomorrow = types.KeyboardButton('Завтра')
        inWeek = types.KeyboardButton('На этой неделе')
        top = types.KeyboardButton('Топ на месяц')
        location = types.KeyboardButton('Поиск по геолокации')
        back = types.KeyboardButton('На главную')
        markup.add(tooday, toomorrow, inWeek, top, location, back)
        bot.send_message(
            message.chat.id, 'Выберите как вы хотите как вы хотите искать', reply_markup=markup)

    if message.text.lower() == 'привет':
        bot.send_message(
            message.chat.id, f"{fmt.hide_link('https://www.prikol.ru/wp-content/gallery/november-2011/geirangerfjord-01-big.jpg')}Кто бы мог подумать, что "
            f"в 2020 году в Telegram появятся видеозвонки!\n\nОбычные голосовые вызовы "
            f"возникли в Telegram лишь в 2017, заметно позже своих конкурентов. А спустя три года, "
            f"когда огромное количество людей на планете приучились работать из дома из-за эпидемии "
            f"коронавируса, команда Павла Дурова не растерялась и сделала качественные "
            f"видеозвонки на WebRTC!\n\nP.S. а ещё ходят слухи про демонстрацию своего экрана :)")

    if message.text.lower() == 'игра «угадай комика»':
        markup = types.ReplyKeyboardMarkup(True, True)
        photo = types.KeyboardButton('Угадай комика по фотке')
        joke = types.KeyboardButton('Угадай комика по шутке')
        back = types.KeyboardButton('На главную')
        markup.add(photo, joke, back)
        bot.send_message(
            message.chat.id, 'Выберите как вы хотите как вы хотите искать', reply_markup=markup)

    if message.text.lower() == 'угадай комика по шутке':
        startGame = requests.get(
            'http://127.0.0.1:8000/api/action/create/{0}/0/'.format(message.chat.id)).json()
        markup = types.ReplyKeyboardMarkup(True, True)
        back = types.KeyboardButton('На главную')
        markup.add(back)
        msg = bot.send_message(
            message.chat.id, startGame["question"]["question"], reply_markup=markup)
        bot.register_next_step_handler(msg, gameJokeMode)


def gameJokeMode(message):
    if not message.text == 'На главную':
        getHuman = requests.get(
            'http://127.0.0.1:8000/api/action/get/{0}'.format(message.chat.id)).json()
        if message.text == getHuman["question"]["human"]["name"]:
            requests.get('http://127.0.0.1:8000/api/user/add/points/{0}/{1}'.format(
                message.chat.id, getHuman["question"]["points"]))

            bot.send_message(message.chat.id, 'Праавильно, на ваш профиль зачислено {0} очков'.format(
                getHuman["question"]["points"]))

            startGame = requests.get(
                'http://127.0.0.1:8000/api/action/create/{0}/0/'.format(message.chat.id)).json()
            markup = types.ReplyKeyboardMarkup(True, True)
            back = types.KeyboardButton('На главную')
            markup.add(back)
            msg = bot.send_message(
                message.chat.id, startGame["question"]["question"], reply_markup=markup)
        else:
            markup = types.ReplyKeyboardMarkup(True, True)
            back = types.KeyboardButton('На главную')
            markup.add(back)
            msg = bot.send_message(message.chat.id,
                                   'Неправильно, попробуйте еще', reply_markup=markup)

        bot.register_next_step_handler(msg, gameJokeMode)
    else:
        markup = types.ReplyKeyboardMarkup(True, True)
        search = types.KeyboardButton('Поиск мероприятия')
        game = types.KeyboardButton('Игра «Угадай комика»')
        setting = types.KeyboardButton('Мой профиль')
        title = 'Привет, чего ты хочешь ?'
        markup.add(search, game, setting)
        msg = bot.send_message(message.chat.id, title, reply_markup=markup)
        bot.register_next_step_handler(msg, send_text)


@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        print(message.location)
        print("latitude: %s; longitude: %s" %
              (message.location.latitude, message.location.longitude))


bot.polling()
