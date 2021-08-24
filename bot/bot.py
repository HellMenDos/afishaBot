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
    city = State()


async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(command="/start",
                         description="Главная"),
        types.BotCommand(command="/search", description="Поиск 🔍"),
        types.BotCommand(command="/tooday",
                         description="Мероприятия на сегодня 😄"),
        types.BotCommand(command="/tomorrow",
                         description="Мероприятия на завтра ⌚️"),
        types.BotCommand(command="/game",
                         description="Игры 🎲 "),
        types.BotCommand(command="/profile", description="Профиль 🤖 "),
    ]
    await bot.set_my_commands(commands)


async def main():

    botInit = Bot(token='1882761591:AAHEJh8otU_roGCQ_c0fOKarGFvxl4Wgvoc')
    bot = Dispatcher(botInit, storage=MemoryStorage())
    print(3)
    # Start chat

    @bot.message_handler(commands="start")
    async def start(message: types.Message):
        response = requests.get(
            'https://telegramexpert.ru/api/user/check/{0}'.format(message.chat.id))

        if response.json()['have']:
            markup = types.ReplyKeyboardMarkup(True, True)
            search = types.KeyboardButton('Поиск 🔍')
            game = types.KeyboardButton('Игры 🎲')
            setting = types.KeyboardButton('Профиль 🤖')
            title = 'Привет!☺️  \nВыбери, что тебя интересует?👇'
            markup.add(search, game, setting)
        else:
            markup = types.ReplyKeyboardMarkup(True, True)
            cities = requests.get(
                'https://telegramexpert.ru/api/city/get/').json()
            for i in range(0, len(cities)):
                markup.add(types.KeyboardButton(cities[i]['name']))
            markup.add(types.KeyboardButton('Другое'))

            title = "Привет! ✋☺️  \n\nЯ Stand Up бот! \n\nЯ могу быстро и удобно искать Stand Up мероприятия в твоем городе. От больших концертов до открытых микрофонов. Платные и бесплатные. \n\n📌 Что я умею:\n\n▪️ Искать Stand Up мероприятия на сегодня, завтра, неделю и по геопозиции;\n▪️ Сохранять список твоих кумиров (в разделе профиль) и присылать уведомления об их концертах;\n▪️ Могу развлечь играми (угадай комика по фото или угадай комика по шутке)\n\nПодскажи, из какого ты города? 👇"

        await message.answer(title, reply_markup=markup)
    userId = 0

    @bot.message_handler()
    async def send_text(message: types.Message, state: FSMContext):
        if message.text.lower() == 'профиль 🤖' or message.text == '/profile':
            cities = requests.get(
                'https://telegramexpert.ru/api/user/get/{0}'.format(str(message.chat.id))).json()
            idols = requests.get(
                'https://telegramexpert.ru/api/user/idols/get/{0}'.format(cities['id'])).json()
            if idols:
                idols = ', '.join(idols)
            else:
                idols = ' У вас нет кумиров'

            textAbout = "<b>Ваш профиль:</b>\n\nВаш уникальный номер: <u>{0}</u>\nВаш город: <u>{1}</u>\nВаше количество очков: <u>{2}</u>\n \nКумиры: {3}\n\nТы можешь выбрать кумиров и я сообщу об их концертах!  \nБудь внимателен, при каждом сохранении все кумиры обновляются. Выбирай всех за раз🤓👇  \n\n<a href='https://t.me/KulikovVladimir'>«Написать владельцу»</a>".format(
                cities["token"], cities["location"]["name"], cities["points"], idols)
            markup = types.ReplyKeyboardMarkup(True, True)
            changeLocation = types.KeyboardButton('Поменять город')
            setIdols = types.KeyboardButton('Выбрать кумиров')
            markup.add(changeLocation, setIdols)
            await message.answer(textAbout, parse_mode=types.ParseMode.HTML, reply_markup=markup, disable_web_page_preview=True)

        if message.text.lower() == 'выбрать кумиров':
            cities = requests.get(
                'https://telegramexpert.ru/api/human/get/').json()
            markup = types.ReplyKeyboardMarkup(True, True)
            markup.add(types.KeyboardButton('Сохранить список'))
            markup.add(types.KeyboardButton('Назад'))
            for i in range(0, len(cities)):
                markup.add(types.KeyboardButton(cities[i]['name']))
            title = 'Выбери кумиров'
            await message.answer(title, reply_markup=markup)
            await Game.human.set()

        if message.text.lower() == 'поменять город':
            cities = requests.get(
                'https://telegramexpert.ru/api/city/get/').json()
            markup = types.ReplyKeyboardMarkup(True, True)
            for i in range(0, len(cities)):
                markup.add(types.KeyboardButton(cities[i]['name']))
            markup.add(types.KeyboardButton('Другое'))

            title = 'Выбери город'
            await message.answer(title, reply_markup=markup)

        cities = requests.get('https://telegramexpert.ru/api/city/get/').json()
        for i in range(0, len(cities)):
            if message.text.lower() == cities[i]['name'].lower():
                create = requests.post(
                    'https://telegramexpert.ru/api/user/reg/', json={"token": message.chat.id, "city": message.text})

                markup = types.ReplyKeyboardMarkup(True, True)
                search = types.KeyboardButton('Поиск 🔍')
                game = types.KeyboardButton('Игры 🎲')
                setting = types.KeyboardButton('Профиль 🤖')
                markup.add(search, game, setting)

                await message.answer('Привет!☺️  \nВыбери, что тебя интересует?👇', reply_markup=markup)

        if message.text.lower() == 'назад' or message.text.lower() == 'на главную':
            create = requests.post(
                'https://telegramexpert.ru/api/user/reg/', json={'token': message.chat.id, 'city': message.text})

            markup = types.ReplyKeyboardMarkup(True, True)
            search = types.KeyboardButton('Поиск 🔍')
            game = types.KeyboardButton('Игры 🎲')
            setting = types.KeyboardButton('Профиль 🤖')
            markup.add(search, game, setting)

            await message.answer('Привет!☺️  \nВыбери, что тебя интересует?👇', reply_markup=markup)

        if message.text.lower() == 'другое':
            cities = requests.get(
                'https://telegramexpert.ru/api/city/get/').json()
            cityText = ''
            markup = types.ReplyKeyboardMarkup(True, True)
            for i in range(0, len(cities)):
                if i == (len(cities)-2):
                    cityText += cities[i]['name'] + ' и '
                else:
                    cityText += cities[i]['name'] + ' , '
            markup.add(types.KeyboardButton('Свой город'))
            await message.answer('К сожалению я пока ищу только в {} 😔, но это ненадолго. Нажми на кнопку «Свой город» и напиши из какого ты города, и я уведомлю, когда смогу тебе помогать👇'.format(
                cityText), reply_markup=markup)
        if message.text.lower() == 'свой город':
            await message.answer('Напиши из какого ты города, и я уведомлю, когда смогу тебе помогать👇')
            await Game.city.set()

        if message.text.lower() == 'игры 🎲' or message.text == '/game':
            requests.get(
                'https://telegramexpert.ru/api/stat/add/{0}/{1}'.format(message.chat.id, 'ИграУгадайКомика'))
            markup = types.ReplyKeyboardMarkup(True, True)
            photo = types.KeyboardButton('Угадай комика по фотке')
            joke = types.KeyboardButton('Угадай комика по шутке')

            markup.add(photo, joke)
            await message.answer('Чтобы ответить на вопрос, необходимо ввести текстом имя и фамилию комика. \nЗа каждый ответ начисляются баллы, в зависимости от сложности. \nОбщее кол-во набранных балов можно посмотреть в разделе «Профиль» 🤖\n\nВыбери вид игры 🎲👇', reply_markup=markup)

        if message.text.lower() == 'угадай комика по шутке':
            requests.get(
                'https://telegramexpert.ru/api/stat/add/{0}/{1}'.format(message.chat.id, 'УгадайПоШутке'))
            startGame = requests.get(
                'https://telegramexpert.ru/api/action/create/{0}/0/'.format(message.chat.id)).json()
            markup = types.ReplyKeyboardMarkup(True, True)
            back = types.KeyboardButton('На главную')
            markup.add(back)
            await message.answer(startGame['question']['question'], reply_markup=markup)
            await Game.question.set()

        if message.text.lower() == 'угадай комика по фотке':
            requests.get(
                'https://telegramexpert.ru/api/stat/add/{0}/{1}'.format(message.chat.id, 'УгадайПоФотке'))
            startGame = requests.get(
                'https://telegramexpert.ru/api/action/create/{0}/1/'.format(message.chat.id)).json()
            markup = types.ReplyKeyboardMarkup(True, True)
            back = types.KeyboardButton('На главную')
            markup.add(back)
            await message.answer(
                f"{fmt.hide_link('https://telegramexpert.ru{0}'.format(startGame['question']['photo']))} Кто это на фотографии ?",
                parse_mode=types.ParseMode.HTML, reply_markup=markup)
            await Game.photo.set()
        # if message.text.lower() == 'Поиск 🔍':
        #     typesOfPost = requests.get(
        #         'https://telegramexpert.ru/api/types/get/').json()
        #     markup = types.ReplyKeyboardMarkup(True, True)
        #     for i in range(0, len(typesOfPost)):
        #         markup.add(types.KeyboardButton(typesOfPost[i]['name']))
        #     await message.answer('Выберите какой тип мероприятий', reply_markup=markup)

        if message.text.lower()[0:2] == '/i':
            requests.get('https://telegramexpert.ru/api/stat/add/{0}/{1}'.format(
                message.chat.id, 'ПереходНаПостНомер{0}'.format(message.text.lower()[2:])))
            post = requests.get(
                'https://telegramexpert.ru/api/post/one/{0}'.format(message.text.lower()[2:])).json()
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

            markup.add(types.InlineKeyboardButton(
                text='Карта 🗺', callback_data=post['id']))
            photo = ''
            if post['photo']:
                photoHTTPS = f"https:{post['photo'].split(':')[1]}"
                photo = fmt.hide_link(photoHTTPS)

            humans = ''
            for k in range(0, len(post['human'])):
                humans += '{0}'.format(post['human'][k]['name'])
                if not k == (len(post['human']) - 1):
                    humans += ', '

            if post['costType'] == 0:
                cost = str(post['cost']) + \
                    ' р.' if post['cost'] else 'Бесплатно'
            elif post['costType'] == 1:
                cost = 'Депозит в размере ' + \
                    str(post['cost']) + \
                    ' р.' if post['cost'] else 'Бесплатно'
            elif post['costType'] == 2:
                cost = f"Донат (любая купюра мин: {post['cost']} р.) "

            await message.answer(
                f"{photo}"
                f"<b>{post['title']}</b> \n\n"
                f"{post['describe']} \n"
                f"Местоположение: {post['location']} \n\n"
                f"Начало:  <u>{post['timeStart'].split('T')[0]} - {post['timeStart'].split('T')[1][:-1]}</u>\n"
                f"Вход:  <u>{post['timeEnd'].split('T')[0]} - {post['timeEnd'].split('T')[1][:-1]}</u>\n\n"
                f"Выступает: {humans} \n"
                f"Цена: {cost} \n",
                parse_mode=types.ParseMode.HTML, reply_markup=markup, disable_web_page_preview=False)

        if message.text.lower() == 'поиск 🔍' or message.text == '/search':
            requests.get(
                'https://telegramexpert.ru/api/stat/add/{0}/{1}'.format(message.chat.id, 'ПоискМероприятия'))
            markup = types.ReplyKeyboardMarkup(True, True)
            count = requests.get(
                'https://telegramexpert.ru/api/posts/count/{0}'.format(message.chat.id)).json()

            tooday = types.KeyboardButton(f'Сегодня({count["tooday"]})')
            toomorrow = types.KeyboardButton(f'Завтра({count["tomorrow"]})')
            inWeek = types.KeyboardButton(f'Неделя({count["week"]})')
            top = types.KeyboardButton(f'Топ({count["best"]}) 🔝')
            location = types.KeyboardButton('По гео 📍')
            back = types.KeyboardButton('На главную')
            markup.add(tooday, toomorrow, inWeek, top, location, back)
            await message.answer('Выбери, как ты хочешь искать🧐👇', reply_markup=markup)
            await Game.typesOfPosts.set()

        if message.text == '/tooday' or message.text == '/tomorrow':
            index = 1 if message.text == '/tomorrow' else 0
            print(index)
            markup = types.ReplyKeyboardMarkup(True, True)
            main = types.KeyboardButton('На главную')
            markup.add(main)

            resp = requests.get(
                'https://telegramexpert.ru/api/post/types/{0}/{1}'.format(index, message.chat.id)).json()
            if resp:

                paidText = ''
                freeText = ''
                depositText = ''
                donationText = ''
                for i in range(0, len(resp)):
                    if resp[i]['cost'] == 0:
                        freeText = freeText + \
                            f"\n\n● {resp[i]['timeEnd'].split('T')[0]} <b>{resp[i]['title']}</b> <u>{resp[i]['location']}</u>\n Вход - {str(resp[i]['cost']) + ' р.' if resp[i]['cost'] else 'Бесплатно'} (Подробнее -> /i{resp[i]['id']})"
                    else:
                        if resp[i]['costType'] == 0:
                            paidText = paidText + \
                                f"\n\n● {resp[i]['timeEnd'].split('T')[0]} <b>{resp[i]['title']}</b> <u>{resp[i]['location']}</u>\n Вход - {str(resp[i]['cost']) + ' р.' if resp[i]['cost'] else 'Бесплатно'} (Подробнее -> /i{resp[i]['id']})"
                        if resp[i]['costType'] == 1:
                            depositText = depositText + \
                                f"\n\n● {resp[i]['timeEnd'].split('T')[0]} <b>{resp[i]['title']}</b> <u>{resp[i]['location']}</u>\n Вход - Депозит в размере {str(resp[i]['cost']) + ' р.' if resp[i]['cost'] else 'Бесплатно'} (Подробнее -> /i{resp[i]['id']})"
                        if resp[i]['costType'] == 2:
                            donationText = donationText + \
                                f"\n\n● {resp[i]['timeEnd'].split('T')[0]} <b>{resp[i]['title']}</b> <u>{resp[i]['location']}</u>\n Вход - Донат (любая купюра мин: {resp[i]['cost']} р.) (Подробнее -> /i{resp[i]['id']})"

                if not paidText:
                    paidText = 'Мероприятий не найдено'
                if not freeText:
                    freeText = 'Мероприятий не найдено'
                if not depositText:
                    depositText = 'Мероприятий не найдено'
                if not donationText:
                    donationText = 'Мероприятий не найдено'

                mainTitle = f'<b>Мероприятия:</b> \n\n <u>Платно:</u>  {paidText} \n\n <u>Бесплатно:</u>  {freeText} \n\n <u>Депозит:</u>  {depositText} \n\n <u>Донаты:</u>  {donationText}'

                await message.answer(mainTitle, parse_mode=types.ParseMode.HTML, reply_markup=markup, disable_web_page_preview=True)
            else:
                await message.answer('Извините пока таких мероприятий нет', reply_markup=markup)

    @bot.message_handler(state=Game.question)
    async def send_text(message: types.Message, state: FSMContext):
        if not message.text == 'На главную':
            getHuman = requests.get(
                'https://telegramexpert.ru/api/action/get/{0}'.format(message.chat.id)).json()
            if message.text.lower() == getHuman["question"]["human"]["name"].lower():
                requests.get('https://telegramexpert.ru/api/user/add/points/{0}/{1}'.format(
                    message.chat.id, getHuman["question"]["points"]))

                await message.answer('Правильно, на ваш профиль зачислено {0} очков'.format(
                    getHuman["question"]["points"]))

                startGame = requests.get(
                    'https://telegramexpert.ru/api/action/create/{0}/0/'.format(message.chat.id)).json()
                markup = types.ReplyKeyboardMarkup(True, True)
                back = types.KeyboardButton('На главную')
                skip = types.KeyboardButton('Пропустить')
                markup.add(back, skip)
                await message.answer(startGame["question"]["question"], reply_markup=markup)

            elif message.text == 'Пропустить':
                startGame = requests.get(
                    'https://telegramexpert.ru/api/action/create/{0}/0/'.format(message.chat.id)).json()
                markup = types.ReplyKeyboardMarkup(True, True)
                back = types.KeyboardButton('На главную')
                skip = types.KeyboardButton('Пропустить')
                markup.add(back, skip)
                await message.answer(startGame["question"]["question"], reply_markup=markup)

            else:
                markup = types.ReplyKeyboardMarkup(True, True)
                back = types.KeyboardButton('На главную')
                skip = types.KeyboardButton('Пропустить')
                markup.add(back, skip)
                await message.answer('Неправильно, попробуйте еще', reply_markup=markup)

        else:
            await state.finish()
            markup = types.ReplyKeyboardMarkup(True, True)
            search = types.KeyboardButton('Поиск 🔍')
            game = types.KeyboardButton('Игры 🎲')
            setting = types.KeyboardButton('Профиль 🤖')
            title = 'Привет!☺️  \nВыбери, что тебя интересует?👇'
            markup.add(search, game, setting)
            await message.answer(title, reply_markup=markup)

    @bot.message_handler(state=Game.photo)
    async def send_text(message: types.Message, state: FSMContext):
        if not message.text == 'На главную':
            getHuman = requests.get(
                'https://telegramexpert.ru/api/action/get/{0}'.format(message.chat.id)).json()
            if message.text.lower() == getHuman["question"]["human"]["name"].lower():
                requests.get('https://telegramexpert.ru/api/user/add/points/{0}/{1}'.format(
                    message.chat.id, getHuman["question"]["points"]))

                await message.answer('Праавильно, на ваш профиль зачислено {0} очков'.format(
                    getHuman["question"]["points"]))

                startGame = requests.get(
                    'https://telegramexpert.ru/api/action/create/{0}/1/'.format(message.chat.id)).json()
                markup = types.ReplyKeyboardMarkup(True, True)
                back = types.KeyboardButton('На главную')
                skip = types.KeyboardButton('Пропустить')
                markup.add(back, skip)

                await message.answer(
                    f"{fmt.hide_link('https://telegramexpert.ru{0}'.format(startGame['question']['photo']))} Кто это на фотографии ?",
                    parse_mode=types.ParseMode.HTML, reply_markup=markup)
            elif message.text == 'Пропустить':
                startGame = requests.get(
                    'https://telegramexpert.ru/api/action/create/{0}/1/'.format(message.chat.id)).json()
                markup = types.ReplyKeyboardMarkup(True, True)
                back = types.KeyboardButton('На главную')
                skip = types.KeyboardButton('Пропустить')
                markup.add(back, skip)

                await message.answer(
                    f"{fmt.hide_link('https://telegramexpert.ru{0}'.format(startGame['question']['photo']))} Кто это на фотографии ?",
                    parse_mode=types.ParseMode.HTML, reply_markup=markup)
            else:
                markup = types.ReplyKeyboardMarkup(True, True)
                back = types.KeyboardButton('На главную')
                skip = types.KeyboardButton('Пропустить')
                markup.add(back, skip)
                await message.answer('Неправильно, попробуйте еще', reply_markup=markup)

        else:
            await state.finish()
            markup = types.ReplyKeyboardMarkup(True, True)
            search = types.KeyboardButton('Поиск 🔍')
            game = types.KeyboardButton('Игры 🎲')
            setting = types.KeyboardButton('Профиль 🤖')
            title = 'Привет!☺️  \nВыбери, что тебя интересует?👇'
            markup.add(search, game, setting)
            await message.answer(title, reply_markup=markup)

    @bot.message_handler(state=Game.typesOfPosts)
    @bot.callback_query_handler()
    async def send_text(message, state: FSMContext):
        if not 'text' in message:
            requests.get(
                'https://telegramexpert.ru/api/post/map/send/{0}/{1}/'.format(message.data, message['from']['id']))
        else:
            if 'Сегодня' in message.text:
                requests.get(
                    'https://telegramexpert.ru/api/stat/add/{0}/{1}'.format(message.chat.id, 'Сегодня'))
                await state.update_data(postType=0)
            elif 'Завтра' in message.text:
                requests.get(
                    'https://telegramexpert.ru/api/stat/add/{0}/{1}'.format(message.chat.id, 'Завтра'))
                await state.update_data(postType=1)
            elif 'Неделя' in message.text:
                requests.get(
                    'https://telegramexpert.ru/api/stat/add/{0}/{1}'.format(message.chat.id, 'НаЭтойНеделе'))
                await state.update_data(postType=2)
            elif 'Топ' in message.text:
                requests.get(
                    'https://telegramexpert.ru/api/stat/add/{0}/{1}'.format(message.chat.id, 'Топ'))
                await state.update_data(postType=3)
            elif 'По гео' in message.text:
                requests.get(
                    'https://telegramexpert.ru/api/stat/add/{0}/{1}'.format(message.chat.id, 'Геолокация'))
                await state.update_data(postType=0)
            elif '/profile' in message.text or '/search' in message.text or '/tooday' in message.text or '/tomorrow' in message.text or '/game' in message.text or '/start' in message.text:
                await message.answer('Чтобы использовать команды нажмите кнопку назад')
            elif message.text.lower() == 'на главную':
                await state.finish()
                markup = types.ReplyKeyboardMarkup(True, True)
                search = types.KeyboardButton('Поиск 🔍')
                game = types.KeyboardButton('Игры 🎲')
                setting = types.KeyboardButton('Профиль 🤖')
                title = 'Привет!☺️  \nВыбери, что тебя интересует?👇'
                markup.add(search, game, setting)
                await message.answer(title, reply_markup=markup)

            current_state = await state.get_data()
            resp = requests.get(
                'https://telegramexpert.ru/api/post/types/{0}/{1}'.format(current_state.get('postType'), message.chat.id)).json()

            # if message.text.lower() == 'бесплатные' or message.text.lower() == 'платные' or message.text.lower() == 'назад':
            #     # {fmt.hide_link('https://telegramexpert.ru{0}'.format(resp[0]['photo']))}
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
                await state.finish()

                requests.get(
                    'https://telegramexpert.ru/api/stat/add/{0}/{1}'.format(message.chat.id, 'ПереходНаПостНомер{0}'.format(message.text.lower()[2:])))
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

                        markup.add(types.InlineKeyboardButton(
                            text='Карта 🗺', callback_data=resp[i]['id']))

                        photo = ''
                        if resp[i]['photo']:
                            photo = fmt.hide_link(
                                'https://telegramexpert.ru{0}'.format(resp[i]['photo']))

                        if resp[i]['costType'] == 0:
                            cost = str(resp[i]['cost']) + \
                                ' р.' if resp[i]['cost'] else 'Бесплатно'
                        elif resp[i]['costType'] == 1:
                            cost = 'Депозит в размере ' + \
                                str(resp[i]['cost']) + \
                                ' р.' if resp[i]['cost'] else 'Бесплатно'
                        elif resp[i]['costType'] == 2:
                            cost = f"Донат (любая купюра мин: {resp[i]['cost']} р.) "

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
                            f"Начало:  <u>{resp[i]['timeStart'].split('T')[0]} - {resp[i]['timeStart'].split('T')[1][:-1]}</u>\n"
                            f"Вход:  <u>{resp[i]['timeEnd'].split('T')[0]} - {resp[i]['timeEnd'].split('T')[1][:-1]}</u>\n\n"
                            f"Выступает: {humans} \n"
                            f"Цена: {cost} \n",
                            parse_mode=types.ParseMode.HTML, reply_markup=markup, disable_web_page_preview=False)

            elif message.text.lower() == 'назад':
                requests.get(
                    'https://telegramexpert.ru/api/stat/add/{0}/{1}'.format(message.chat.id, 'ПоискМероприятия'))
                markup = types.ReplyKeyboardMarkup(True, True)
                count = requests.get(
                    'https://telegramexpert.ru/api/posts/count/{0}'.format(message.chat.id)).json()

                tooday = types.KeyboardButton(f'Сегодня({count["tooday"]})')
                toomorrow = types.KeyboardButton(
                    f'Завтра({count["tomorrow"]})')
                inWeek = types.KeyboardButton(f'Неделя({count["week"]})')
                top = types.KeyboardButton(f'Топ({count["best"]}) 🔝')
                location = types.KeyboardButton('По гео 📍')
                back = types.KeyboardButton('На главную')
                markup.add(tooday, toomorrow, inWeek, top, location, back)
                await message.answer('Выбери, как ты хочешь искать🧐👇', reply_markup=markup)

            elif message.text.lower() == 'по гео 📍':
                await state.finish()
                title = 'Чтобы найти ближайшие к тебе мероприятия, отправь своё местоположение: \n● Нажми 📎 \n● Выбери «Геопозиция»\n● Нажми «Отправить свою геопозицию» (локацию можно изменить перед отправкой).'
                await message.answer(title)
            else:
                markup = types.ReplyKeyboardMarkup(True, True)
                main = types.KeyboardButton('На главную')
                back = types.KeyboardButton('Назад')
                markup.add(main, back)

                if resp:

                    paidText = ''
                    freeText = ''
                    depositText = ''
                    donationText = ''
                    for i in range(0, len(resp)):
                        if resp[i]['cost'] == 0:
                            freeText = freeText + \
                                f"\n\n● {resp[i]['timeEnd'].split('T')[0]} <b>{resp[i]['title']}</b> <u>{resp[i]['location']}</u>\n Вход - {str(resp[i]['cost']) + ' р.' if resp[i]['cost'] else 'Бесплатно'} (Подробнее -> /i{resp[i]['id']})"
                        else:
                            if resp[i]['costType'] == 0:
                                paidText = paidText + \
                                    f"\n\n● {resp[i]['timeEnd'].split('T')[0]} <b>{resp[i]['title']}</b> <u>{resp[i]['location']}</u>\n Вход - {str(resp[i]['cost']) + ' р.' if resp[i]['cost'] else 'Бесплатно'} (Подробнее -> /i{resp[i]['id']})"
                            if resp[i]['costType'] == 1:
                                depositText = depositText + \
                                    f"\n\n● {resp[i]['timeEnd'].split('T')[0]} <b>{resp[i]['title']}</b> <u>{resp[i]['location']}</u>\n Вход - депозит в размере {str(resp[i]['cost']) + ' р.' if resp[i]['cost'] else 'Бесплатно'} (Подробнее -> /i{resp[i]['id']})"
                            if resp[i]['costType'] == 2:
                                donationText = donationText + \
                                    f"\n\n● {resp[i]['timeEnd'].split('T')[0]} <b>{resp[i]['title']}</b> <u>{resp[i]['location']}</u>\n Вход - Донат (любая купюра мин: {resp[i]['cost']} р.) (Подробнее -> /i{resp[i]['id']})"

                    if not paidText:
                        paidText = 'Мероприятий не найдено'
                    if not freeText:
                        freeText = 'Мероприятий не найдено'
                    if not depositText:
                        depositText = 'Мероприятий не найдено'
                    if not donationText:
                        donationText = 'Мероприятий не найдено'

                    mainTitle = f'<b>Мероприятия (можешь сразу открыть несколько постов):</b> \n\n <u>Платно:</u> {paidText} \n\n <u>Бесплатно:</u> {freeText} \n\n <u>Депозит:</u> {depositText} \n\n <u>Донаты:</u> {donationText}'

                    await message.answer(mainTitle, parse_mode=types.ParseMode.HTML, reply_markup=markup, disable_web_page_preview=True)
                else:
                    await message.answer('Извините пока таких мероприятий нет', reply_markup=markup)
    data = []

    @bot.message_handler(state=Game.city)
    async def send_text(message: types.Message, state: FSMContext):
        await state.finish()
        requests.post('https://telegramexpert.ru/api/city/type/',
                      json={"city": message.text.lower()})

        await message.answer('Спасибо! \nЯ уведомлю, когда смогу тебе помочь🤓')
        response = requests.get(
            'https://telegramexpert.ru/api/user/check/{0}'.format(message.chat.id))

        if response.json()['have']:
            markup = types.ReplyKeyboardMarkup(True, True)
            search = types.KeyboardButton('Поиск 🔍')
            game = types.KeyboardButton('Игры 🎲')
            setting = types.KeyboardButton('Профиль 🤖')
            title = 'Привет!☺️  \nВыбери, что тебя интересует?👇'
            markup.add(search, game, setting)
        else:
            markup = types.ReplyKeyboardMarkup(True, True)
            cities = requests.get(
                'https://telegramexpert.ru/api/city/get/').json()
            for i in range(0, len(cities)):
                markup.add(types.KeyboardButton(cities[i]['name']))
            markup.add(types.KeyboardButton('Другое'))

            title = "Привет! ✋☺️  \n\nЯ Stand Up бот! \n\nЯ могу быстро и удобно искать Stand Up мероприятия в твоем городе. От больших концертов до открытых микрофонов. Платные и бесплатные. \n\n📌 Что я умею:\n\n▪️ Искать Stand Up мероприятия на сегодня, завтра, неделю и по геопозиции;\n▪️ Сохранять список твоих кумиров (в разделе профиль) и присылать уведомления об их концертах;\n▪️ Могу развлечь играми (угадай комика по фото или угадай комика по шутке)\n\nПодскажи, из какого ты города? 👇"

        await message.answer(title, reply_markup=markup)

    @bot.message_handler(state=Game.human)
    async def send_text(message: types.Message, state: FSMContext):
        print(message.text)
        if message.text == 'Сохранить список':
            requests.post('https://telegramexpert.ru/api/user/idols/', json={
                "token": message.chat.id,
                "humans": data
            }
            )

            data.clear()
            await state.finish()
            markup = types.ReplyKeyboardMarkup(True, True)
            search = types.KeyboardButton('Поиск 🔍')
            game = types.KeyboardButton('Игры 🎲')
            setting = types.KeyboardButton('Профиль 🤖')
            title = 'Привет!☺️  \nВыбери, что тебя интересует?👇'
            markup.add(search, game, setting)
            await message.answer(title, reply_markup=markup)

        elif message.text == 'Назад':
            await state.finish()
            markup = types.ReplyKeyboardMarkup(True, True)
            search = types.KeyboardButton('Поиск 🔍')
            game = types.KeyboardButton('Игры 🎲')
            setting = types.KeyboardButton('Профиль 🤖')
            title = 'Привет!☺️  \nВыбери, что тебя интересует?👇'
            markup.add(search, game, setting)
            await message.answer(title, reply_markup=markup)
        else:
            data.append(message.text)
            await message.answer('Успешно добавлено, чтобы применить изменения нажмите - Сохранить список')

    @bot.message_handler(content_types=["location"])
    async def loc_handler(message):
        print(message)
        resp = requests.get('https://telegramexpert.ru/api/post/coord/{0}/{1}'.format(
            message.location.latitude, message.location.longitude)).json()
        title = f'<b>Ближайшие мероприятия (можешь сразу открыть несколько постов):</b> \n'
        for i in range(0, len(resp)):
            cost = ''
            if resp[i][1]['cost'] == 0:
                cost = 'Бесплатно'
            else:
                if(resp[i][1]['costType'] == 0):
                    cost = str(resp[i][1]['cost']) + ' р.'
                elif(resp[i][1]['costType'] == 1):
                    cost = 'Депозит в размере ' + \
                        str(resp[i][1]['cost']) + ' р.'
                else:
                    cost = 'Любая купюра'
            if not resp[i][0] == 99999999:
                title = title + \
                    f"\nРасстояние: <b>{resp[i][0]} метров</b>  \n● {resp[i][1]['timeEnd'].split('T')[0]} <b>{resp[i][1]['title']}</b> <u>{resp[i][1]['location']}</u>\n Вход - {cost} (Подробнее -> /i{resp[i][1]['id']}) \n"
        await message.answer(title, parse_mode=types.ParseMode.HTML, disable_web_page_preview=True)

    await set_commands(botInit)
    await bot.start_polling()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    task1 = loop.create_task(main())
    group = asyncio.gather(task1)
    loop.run_until_complete(group)
