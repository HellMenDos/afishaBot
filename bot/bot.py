import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
import aiogram.utils.markdown as fmt
import asyncio
import requests
from requests.api import post
from requests.models import Response, codes


class Game(StatesGroup):
    question = State()
    photo = State()
    typesOfPosts = State()
    human = State()
    postType = State()


async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(command="/profile", description="Профиль 🤖 "),
        types.BotCommand(command="/search", description="Поиск 🔍"),
        types.BotCommand(command="/tooday",
                         description="Мероприятия на сегодня 😄"),
        types.BotCommand(command="/tomorrow",
                         description="Мероприятия на завтра ⌚️"),
        types.BotCommand(command="/game",
                         description="Игра 🎲 "),
        types.BotCommand(command="/start",
                         description="Главная")
    ]
    await bot.set_my_commands(commands)


async def main():

    botInit = Bot(token='1921418522:AAGhuuELsBbOeby0OcjyjlGO5lqAbypl30c')
    bot = Dispatcher(botInit, storage=MemoryStorage())

    # Start chat
    @bot.message_handler(commands="start")
    async def start(message: types.Message):
        response = requests.get(
            'http://45.147.178.7:8000/api/user/check/{}'.format(message.chat.id))

        if response.json()['have']:
            markup = types.ReplyKeyboardMarkup(True, True)
            search = types.KeyboardButton('Поиск 🔍')
            game = types.KeyboardButton('Игра 🎲')
            setting = types.KeyboardButton('Профиль 🤖')
            title = 'Привет, чего ты хочешь ?'
            markup.add(search, game, setting)
        else:
            markup = types.ReplyKeyboardMarkup(True, True)
            cities = requests.get(
                'http://45.147.178.7:8000/api/city/get/').json()
            for i in range(0, len(cities)):
                markup.add(types.KeyboardButton(cities[i]['name']))
            markup.add(types.KeyboardButton('Другое'))

            title = 'Выбери город'

        await message.answer(title, reply_markup=markup)
    userId = 0

    @bot.message_handler()
    async def send_text(message: types.Message, state: FSMContext):
        if message.text.lower() == 'профиль 🤖' or message.text == '/profile':
            cities = requests.get(
                'http://45.147.178.7:8000/api/user/get/{0}'.format(str(message.chat.id))).json()
            idols = requests.get(
                'http://45.147.178.7:8000/api/user/idols/get/{0}'.format(cities['id'])).json()
            if idols:
                idols = ', '.join(idols)
            else:
                idols = ' У вас нет кумиров'

            textAbout = "<b>Ваш профиль:</b>\n\nВаш уникальный номер: <u>{0}</u>\nВаш город: <u>{1}</u>\nВаше количество очков: <u>{2}</u>\n \nКумиры: {3}".format(
                cities["token"], cities["location"]["name"], cities["points"], idols)
            markup = types.ReplyKeyboardMarkup(True, True)
            changeLocation = types.KeyboardButton('Поменять город')
            setIdols = types.KeyboardButton('Выбрать кумиров')
            markup.add(changeLocation, setIdols)
            await message.answer(textAbout, parse_mode=types.ParseMode.HTML, reply_markup=markup)

        if message.text.lower() == 'выбрать кумиров':
            cities = requests.get(
                'http://45.147.178.7:8000/api/human/get/').json()
            markup = types.ReplyKeyboardMarkup(True, True)
            for i in range(0, len(cities)):
                markup.add(types.KeyboardButton(cities[i]['name']))
            markup.add(types.KeyboardButton('Сохранить список кумиров'))
            markup.add(types.KeyboardButton('Очистить список'))
            title = 'Выбери кумиров'
            await message.answer(title, reply_markup=markup)
            await Game.human.set()

        if message.text.lower() == 'поменять город':
            cities = requests.get(
                'http://45.147.178.7:8000/api/city/get/').json()
            markup = types.ReplyKeyboardMarkup(True, True)
            for i in range(0, len(cities)):
                markup.add(types.KeyboardButton(cities[i]['name']))
            markup.add(types.KeyboardButton('Другое'))

            title = 'Выбери город'
            await message.answer(title, reply_markup=markup)

        cities = requests.get('http://45.147.178.7:8000/api/city/get/').json()
        for i in range(0, len(cities)):
            if message.text.lower() == cities[i]['name']:
                create = requests.get(
                    'http://45.147.178.7:8000/api/user/reg/{0}/{1}'.format(message.chat.id, message.text))

                markup = types.ReplyKeyboardMarkup(True, True)
                search = types.KeyboardButton('Поиск 🔍')
                game = types.KeyboardButton('Игра 🎲')
                setting = types.KeyboardButton('Профиль 🤖')
                markup.add(search, game, setting)

                await message.answer('Привет, чего ты хочешь ?', reply_markup=markup)

        if message.text.lower() == 'назад':
            create = requests.get(
                'http://45.147.178.7:8000/api/user/reg/{0}/{1}'.format(message.chat.id, message.text))

            markup = types.ReplyKeyboardMarkup(True, True)
            search = types.KeyboardButton('Поиск 🔍')
            game = types.KeyboardButton('Игра 🎲')
            setting = types.KeyboardButton('Профиль 🤖')
            markup.add(search, game, setting)

            await message.answer('Привет, чего ты хочешь ?', reply_markup=markup)

        if message.text.lower() == 'другое':
            cities = requests.get(
                'http://45.147.178.7:8000/api/city/get/').json()
            cityText = ''
            markup = types.ReplyKeyboardMarkup(True, True)
            for i in range(0, len(cities)):
                if i == (len(cities)-2):
                    cityText += cities[i]['name'] + ' и '
                else:
                    cityText += cities[i]['name'] + ' , '
                markup.add(types.KeyboardButton(cities[i]['name']))
            markup.add(types.KeyboardButton('Другое'))
            await message.answer('К сожалению я пока ищу только в {} но это ненадолго. Напиши из какого ты города и я уведомлю, когда смогу тебе помогать.'.format(
                cityText), reply_markup=markup)

        if message.text.lower() == 'игра 🎲' or message.text == '/game':
            requests.get(
                'http://45.147.178.7:8000/api/stat/add/{0}/{1}'.format(message.chat.id, 'ИграУгадайКомика'))
            markup = types.ReplyKeyboardMarkup(True, True)
            photo = types.KeyboardButton('Угадай комика по фотке')
            joke = types.KeyboardButton('Угадай комика по шутке')

            markup.add(photo, joke)
            await message.answer('Выберите как вы хотите как вы хотите искать', reply_markup=markup)

        if message.text.lower() == 'угадай комика по шутке':
            requests.get(
                'http://45.147.178.7:8000/api/stat/add/{0}/{1}'.format(message.chat.id, 'УгадайПоШутке'))
            startGame = requests.get(
                'http://45.147.178.7:8000/api/action/create/{0}/0/'.format(message.chat.id)).json()
            markup = types.ReplyKeyboardMarkup(True, True)
            back = types.KeyboardButton('На главную')
            markup.add(back)
            await message.answer(startGame["question"]["question"], reply_markup=markup)
            await Game.question.set()

        if message.text.lower() == 'угадай комика по фотке':
            requests.get(
                'http://45.147.178.7:8000/api/stat/add/{0}/{1}'.format(message.chat.id, 'УгадайПоФотке'))
            startGame = requests.get(
                'http://45.147.178.7:8000/api/action/create/{0}/1/'.format(message.chat.id)).json()
            markup = types.ReplyKeyboardMarkup(True, True)
            back = types.KeyboardButton('На главную')
            markup.add(back)
            await message.answer(
                f"{fmt.hide_link(startGame['question']['photo'])} Кто это на фотографии ?",
                parse_mode=types.ParseMode.HTML, reply_markup=markup)
            await Game.photo.set()
        # if message.text.lower() == 'Поиск 🔍':
        #     typesOfPost = requests.get(
        #         'http://45.147.178.7:8000/api/types/get/').json()
        #     markup = types.ReplyKeyboardMarkup(True, True)
        #     for i in range(0, len(typesOfPost)):
        #         markup.add(types.KeyboardButton(typesOfPost[i]['name']))
        #     await message.answer('Выберите какой тип мероприятий', reply_markup=markup)

        if message.text.lower()[0:2] == '/i':
            requests.get('http://45.147.178.7:8000/api/stat/add/{0}/{1}'.format(
                message.chat.id, 'ПереходНаПостНомер{0}'.format(message.text.lower()[2:])))
            post = requests.get(
                'http://45.147.178.7:8000/api/post/one/{0}'.format(message.text.lower()[2:])).json()
            markup = types.InlineKeyboardMarkup(True, True)
            if post['link']:
                link = types.InlineKeyboardButton(
                    'Ссылка на покупку', url=post['link'])
                markup.add(link)
            if post['linkForChat']:
                linkForChat = types.InlineKeyboardButton(
                    'Ссылка на чат', url=post['linkForChat'])
                markup.add(linkForChat)
            if post['linkRegistr']:
                linkRegistr = types.InlineKeyboardButton(
                    'Ссылка на регистрацию', url=post['linkRegistr'])
                markup.add(linkRegistr)

            photo = ''
            if post['photo']:
                photo = fmt.hide_link(post['photo'])

            humans = ''
            for k in range(0, len(post['human'])):
                humans += '{0}'.format(post['human'][k]['name'])
                if not k == (len(post['human']) - 1):
                    humans += ', '

            await message.answer(
                f"{photo}"
                f"<b>{post['title']}</b> \n\n"
                f"{post['describe']} \n"
                f"Местоположение: {post['location']} \n\n"
                f"Начало:  <u>{post['timeStart'].split('T')[0]} - {post['timeStart'].split('T')[1][:-1]}</u>\n"
                f"Вход:  <u>{post['timeEnd'].split('T')[0]} - {post['timeEnd'].split('T')[1][:-1]}</u>\n\n"
                f"Выступает: {humans} \n"
                f"Цена: {str(post['cost']) + ' р.' if post['cost'] else 'Бесплатно'} \n",
                parse_mode=types.ParseMode.HTML, reply_markup=markup)

        if message.text.lower() == 'поиск 🔍' or message.text == '/search':
            requests.get(
                'http://45.147.178.7:8000/api/stat/add/{0}/{1}'.format(message.chat.id, 'ПоискМероприятия'))
            markup = types.ReplyKeyboardMarkup(True, True)
            count = requests.get(
                'http://45.147.178.7:8000/api/posts/count/').json()

            tooday = types.KeyboardButton(f'Сегодня({count["tooday"]}) 😄')
            toomorrow = types.KeyboardButton(f'Завтра({count["tomorrow"]}) ⌚️')
            inWeek = types.KeyboardButton(f'На неделе ({count["week"]}) 🗓️')
            top = types.KeyboardButton(f'Топ ({count["best"]}) 🔝')
            location = types.KeyboardButton('По геолокации 📍')
            markup.add(tooday, toomorrow, inWeek, top, location)
            await message.answer('Выберите как вы хотите как вы хотите искать', reply_markup=markup)
            await Game.typesOfPosts.set()

            if message.text == '/tooday' or message.text == '/tomorrow':
                index = 1 if message.text == '/tomorrow' else 0

                resp = requests.get(
                    'http://45.147.178.7:8000/api/post/types/{0}'.format(index)).json()
                if resp:

                    paidText = ''
                    freeText = ''
                    depositText = ''
                    donationText = ''
                    for i in range(0, len(resp)):
                        if resp[i]['cost'] == 0:
                            freeText = freeText + \
                                f"\n● {resp[i]['timeEnd'].split('T')[0]} <b>{resp[i]['title']}</b> <u>{resp[i]['location']}</u>\n Вход - {str(resp[i]['cost']) + ' р.' if resp[i]['cost'] else 'Бесплатно'} (/i{resp[i]['id']})"
                        else:
                            if resp[i]['costType'] == 0:
                                paidText = paidText + \
                                    f"\n● {resp[i]['timeEnd'].split('T')[0]} <b>{resp[i]['title']}</b> <u>{resp[i]['location']}</u>\n Вход - {str(resp[i]['cost']) + ' р.' if resp[i]['cost'] else 'Бесплатно'} (/i{resp[i]['id']})"
                            if resp[i]['costType'] == 1:
                                depositText = depositText + \
                                    f"\n● {resp[i]['timeEnd'].split('T')[0]} <b>{resp[i]['title']}</b> <u>{resp[i]['location']}</u>\n Вход - депозит в размере{str(resp[i]['cost']) + ' р.' if resp[i]['cost'] else 'Бесплатно'} (/i{resp[i]['id']})"
                            if resp[i]['costType'] == 2:
                                donationText = donationText + \
                                    f"\n● {resp[i]['timeEnd'].split('T')[0]} <b>{resp[i]['title']}</b> <u>{resp[i]['location']}</u>\n Вход - донат (любая купюра)(/i{resp[i]['id']})"

                    if not paidText:
                        paidText = 'Мероприятий не найдено'
                    if not freeText:
                        freeText = 'Мероприятий не найдено'
                    if not depositText:
                        depositText = 'Мероприятий не найдено'
                    if not donationText:
                        donationText = 'Мероприятий не найдено'

                    mainTitle = f'<b>Мероприятия:</b> \n\n <u>Платно:</u> \n {paidText} \n\n <u>Бесплатно:</u> \n {freeText} \n\n <u>Депозит:</u> \n {depositText} \n\n <u>Донаты:</u> \n {donationText}'

                    await message.answer(mainTitle, parse_mode=types.ParseMode.HTML, reply_markup=markup)
                else:
                    await message.answer('Извините пока таких мероприятий нет', reply_markup=markup)

    @bot.message_handler(state=Game.question)
    async def send_text(message: types.Message, state: FSMContext):
        if not message.text == 'На главную':
            getHuman = requests.get(
                'http://45.147.178.7:8000/api/action/get/{0}'.format(message.chat.id)).json()
            if message.text == getHuman["question"]["human"]["name"]:
                requests.get('http://45.147.178.7:8000/api/user/add/points/{0}/{1}'.format(
                    message.chat.id, getHuman["question"]["points"]))

                await message.answer('Праавильно, на ваш профиль зачислено {0} очков'.format(
                    getHuman["question"]["points"]))

                startGame = requests.get(
                    'http://45.147.178.7:8000/api/action/create/{0}/0/'.format(message.chat.id)).json()
                markup = types.ReplyKeyboardMarkup(True, True)
                back = types.KeyboardButton('На главную')
                markup.add(back)
                await message.answer(startGame["question"]["question"], reply_markup=markup)
            else:
                markup = types.ReplyKeyboardMarkup(True, True)
                back = types.KeyboardButton('На главную')
                markup.add(back)
                await message.answer('Неправильно, попробуйте еще', reply_markup=markup)

        else:
            await state.finish()
            markup = types.ReplyKeyboardMarkup(True, True)
            search = types.KeyboardButton('Поиск 🔍')
            game = types.KeyboardButton('Игра 🎲')
            setting = types.KeyboardButton('Профиль 🤖')
            title = 'Привет, чего ты хочешь ?'
            markup.add(search, game, setting)
            await message.answer(title, reply_markup=markup)

    @bot.message_handler(state=Game.photo)
    async def send_text(message: types.Message, state: FSMContext):
        if not message.text == 'На главную':
            getHuman = requests.get(
                'http://45.147.178.7:8000/api/action/get/{0}'.format(message.chat.id)).json()
            if message.text == getHuman["question"]["human"]["name"]:
                requests.get('http://45.147.178.7:8000/api/user/add/points/{0}/{1}'.format(
                    message.chat.id, getHuman["question"]["points"]))

                await message.answer('Праавильно, на ваш профиль зачислено {0} очков'.format(
                    getHuman["question"]["points"]))

                startGame = requests.get(
                    'http://45.147.178.7:8000/api/action/create/{0}/1/'.format(message.chat.id)).json()
                markup = types.ReplyKeyboardMarkup(True, True)
                back = types.KeyboardButton('На главную')
                markup.add(back)

                await message.answer(
                    f"{fmt.hide_link(startGame['question']['photo'])} Кто это на фотографии ?",
                    parse_mode=types.ParseMode.HTML)
            else:
                markup = types.ReplyKeyboardMarkup(True, True)
                back = types.KeyboardButton('На главную')
                markup.add(back)
                await message.answer('Неправильно, попробуйте еще', reply_markup=markup)

        else:
            await state.finish()
            markup = types.ReplyKeyboardMarkup(True, True)
            search = types.KeyboardButton('Поиск 🔍')
            game = types.KeyboardButton('Игра 🎲')
            setting = types.KeyboardButton('Профиль 🤖')
            title = 'Привет, чего ты хочешь ?'
            markup.add(search, game, setting)
            await message.answer(title, reply_markup=markup)

    @bot.message_handler(state=Game.typesOfPosts)
    async def send_text(message, state: FSMContext):

        if 'Сегодня' in message.text:
            requests.get(
                'http://45.147.178.7:8000/api/stat/add/{0}/{1}'.format(message.chat.id, 'Сегодня'))
            await state.update_data(postType=0)
        elif 'Завтра' in message.text:
            requests.get(
                'http://45.147.178.7:8000/api/stat/add/{0}/{1}'.format(message.chat.id, 'Завтра'))
            await state.update_data(postType=1)
        elif 'На этой неделе' in message.text:
            requests.get(
                'http://45.147.178.7:8000/api/stat/add/{0}/{1}'.format(message.chat.id, 'НаЭтойНеделе'))
            await state.update_data(postType=2)
        elif 'Топ' in message.text:
            requests.get(
                'http://45.147.178.7:8000/api/stat/add/{0}/{1}'.format(message.chat.id, 'Топ'))
            await state.update_data(postType=3)
        elif 'По геолокации' in message.text:
            requests.get(
                'http://45.147.178.7:8000/api/stat/add/{0}/{1}'.format(message.chat.id, 'Геолокация'))
            await state.update_data(postType=0)

        current_state = await state.get_data()
        resp = requests.get(
            'http://45.147.178.7:8000/api/post/types/{0}'.format(current_state.get('postType'))).json()

        # if message.text.lower() == 'бесплатные' or message.text.lower() == 'платные' or message.text.lower() == 'назад':
        #     # {fmt.hide_link('http://45.147.178.7:8000{0}'.format(resp[0]['photo']))}
        #     markup = types.ReplyKeyboardMarkup(True, True)
        #     main = types.KeyboardButton('На главную')
        #     markup.add(main)

        #     if resp:
        #         title = '<b>Мероприятия:</b> \n'
        #         for i in range(0, len(resp)):
        #             title = title + \
        #                 f"\n● {resp[i]['timeEnd'].split('T')[0]} <b>{resp[i]['title']}</b> <u>{resp[i]['location']}</u>\n Вход - {str(resp[i]['cost']) + ' р.' if resp[i]['cost'] else 'Бесплатно'} (/i{resp[i]['id']})"
        #         await message.answer(title, parse_mode=types.ParseMode.HTML, reply_markup=markup)
        #     else:
        #         await message.answer('Извините пока таких мероприятий нет', reply_markup=markup)
        if message.text.lower()[0:2] == '/i':
            requests.get(
                'http://45.147.178.7:8000/api/stat/add/{0}/{1}'.format(message.chat.id, 'ПереходНаПостНомер{0}'.format(message.text.lower()[2:])))
            for i in range(0, len(resp)):
                if message.text.lower() == f"/i{resp[i]['id']}":

                    markup = types.InlineKeyboardMarkup(True, True)
                    if resp[i]['link']:
                        link = types.InlineKeyboardButton(
                            'Ссылка на покупку', url=resp[i]['link'])
                        markup.add(link)
                    if resp[i]['linkForChat']:
                        linkForChat = types.InlineKeyboardButton(
                            'Ссылка на чат', url=resp[i]['linkForChat'])
                        markup.add(linkForChat)
                    if resp[i]['linkRegistr']:
                        linkRegistr = types.InlineKeyboardButton(
                            'Ссылка на регистрацию', url=resp[i]['linkRegistr'])
                        markup.add(linkRegistr)

                    photo = ''
                    if resp[i]['photo']:
                        photo = fmt.hide_link(resp[i]['photo'])

                    humans = ''
                    for k in range(0, len(resp[i]['human'])):
                        humans += '{0}'.format(resp[i]['human'][k]['name'])
                        if not k == (len(resp[i]['human']) - 1):
                            humans += ', '
                    await message.answer(
                        f"{photo}"
                        f"<b>{resp[i]['title']}</b> \n\n"
                        f"{resp[i]['describe']} \n"
                        f"Местоположение: {resp[i]['location']} \n\n"
                        f"Начало:  <u>{resp[i]['timeStart'].split('T')[i]} - {resp[i]['timeStart'].split('T')[1][:-1]}</u>\n"
                        f"Вход:  <u>{resp[i]['timeEnd'].split('T')[i]} - {resp[i]['timeEnd'].split('T')[1][:-1]}</u>\n\n"
                        f"Выступает: {humans} \n"
                        f"Цена: {str(resp[i]['cost']) + ' р.' if resp[i]['cost'] else 'Бесплатно'} \n",
                        parse_mode=types.ParseMode.HTML, reply_markup=markup)

        elif message.text.lower() == 'на главную':
            await state.finish()
            markup = types.ReplyKeyboardMarkup(True, True)
            search = types.KeyboardButton('Поиск 🔍')
            game = types.KeyboardButton('Игра 🎲')
            setting = types.KeyboardButton('Профиль 🤖')
            title = 'Привет, чего ты хочешь ?'
            markup.add(search, game, setting)
            await message.answer(title, reply_markup=markup)
        elif message.text.lower() == 'По геолокации 📍':
            await state.finish()
            title = 'Чтобы найти ближайшие к Вам кинотеатры, отправьте своё местоположение: \n● Нажмите 📎 \n● Выберите «Location»\n● Нажмите «Send my current location» (локацию можно изменить перед отправкой).'
            await message.answer(title)
        else:
            markup = types.ReplyKeyboardMarkup(True, True)
            main = types.KeyboardButton('На главную')
            markup.add(main)

            if resp:

                paidText = ''
                freeText = ''
                depositText = ''
                donationText = ''
                for i in range(0, len(resp)):
                    if resp[i]['cost'] == 0:
                        freeText = freeText + \
                            f"\n● {resp[i]['timeEnd'].split('T')[0]} <b>{resp[i]['title']}</b> <u>{resp[i]['location']}</u>\n Вход - {str(resp[i]['cost']) + ' р.' if resp[i]['cost'] else 'Бесплатно'} (/i{resp[i]['id']})"
                    else:
                        if resp[i]['costType'] == 0:
                            paidText = paidText + \
                                f"\n● {resp[i]['timeEnd'].split('T')[0]} <b>{resp[i]['title']}</b> <u>{resp[i]['location']}</u>\n Вход - {str(resp[i]['cost']) + ' р.' if resp[i]['cost'] else 'Бесплатно'} (/i{resp[i]['id']})"
                        if resp[i]['costType'] == 1:
                            depositText = depositText + \
                                f"\n● {resp[i]['timeEnd'].split('T')[0]} <b>{resp[i]['title']}</b> <u>{resp[i]['location']}</u>\n Вход - депозит в размере{str(resp[i]['cost']) + ' р.' if resp[i]['cost'] else 'Бесплатно'} (/i{resp[i]['id']})"
                        if resp[i]['costType'] == 2:
                            donationText = donationText + \
                                f"\n● {resp[i]['timeEnd'].split('T')[0]} <b>{resp[i]['title']}</b> <u>{resp[i]['location']}</u>\n Вход - донат (любая купюра)(/i{resp[i]['id']})"

                if not paidText:
                    paidText = 'Мероприятий не найдено'
                if not freeText:
                    freeText = 'Мероприятий не найдено'
                if not depositText:
                    depositText = 'Мероприятий не найдено'
                if not donationText:
                    donationText = 'Мероприятий не найдено'

                mainTitle = f'<b>Мероприятия:</b> \n\n <u>Платно:</u> \n {paidText} \n\n <u>Бесплатно:</u> \n {freeText} \n\n <u>Депозит:</u> \n {depositText} \n\n <u>Донаты:</u> \n {donationText}'

                await message.answer(mainTitle, parse_mode=types.ParseMode.HTML, reply_markup=markup)
            else:
                await message.answer('Извините пока таких мероприятий нет', reply_markup=markup)

    data = []

    @bot.message_handler(state=Game.human)
    async def send_text(message: types.Message, state: FSMContext):
        print(message.text)
        if message.text == 'Сохранить список кумиров':
            requests.post('http://45.147.178.7:8000/api/user/idols/', json={
                "token": message.chat.id,
                "humans": data
            }
            )
            await state.finish()
            markup = types.ReplyKeyboardMarkup(True, True)
            search = types.KeyboardButton('Поиск 🔍')
            game = types.KeyboardButton('Игра 🎲')
            setting = types.KeyboardButton('Профиль 🤖')
            title = 'Привет, чего ты хочешь ?'
            markup.add(search, game, setting)
            await message.answer(title, reply_markup=markup)

        elif message.text == 'Очистить список':
            requests.post('http://45.147.178.7:8000/api/user/idols/', json={
                "token": message.chat.id,
                "humans": []
            }
            )
            await state.finish()
            markup = types.ReplyKeyboardMarkup(True, True)
            search = types.KeyboardButton('Поиск 🔍')
            game = types.KeyboardButton('Игра 🎲')
            setting = types.KeyboardButton('Профиль 🤖')
            title = 'Привет, чего ты хочешь ?'
            markup.add(search, game, setting)
            await message.answer(title, reply_markup=markup)
        else:
            data.append(message.text)
            await message.answer('Успешно добавлено, чтобы применить изменения нажмите - Сохранить список кумиров')

    @bot.message_handler(content_types=["location"])
    async def loc_handler(message):
        print(message)
        resp = requests.get('http://45.147.178.7:8000/api/post/coord/{0}/{1}'.format(
            message.location.latitude, message.location.longitude)).json()
        title = '<b>Ближайшие мероприятия:</b> \n'
        for i in range(0, len(resp)):
            cost = ''
            if resp[i][1]['cost'] == 0:
                cost = 'Беспалтно'
            else:
                if(resp[i][1]['costType'] == 0):
                    cost = str(resp[i][1]['cost']) + ' р.'
                elif(resp[i][1]['costType'] == 1):
                    cost = 'Депозит в размере' + \
                        str(resp[i][1]['cost']) + ' р.'
                else:
                    cost = 'Любая купюра'
            if not resp[i][0] == 99999999:
                title = title + \
                    f"\nРасстояние: <b>{resp[i][0]} метров</b>  \n● {resp[i][1]['timeEnd'].split('T')[0]} <b>{resp[i][1]['title']}</b> <u>{resp[i][1]['location']}</u>\n Вход - {cost} (/i{resp[i][1]['id']}) \n"
        await message.answer(title, parse_mode=types.ParseMode.HTML)

    await set_commands(botInit)
    await bot.start_polling()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    task1 = loop.create_task(main())
    group = asyncio.gather(task1)
    loop.run_until_complete(group)
