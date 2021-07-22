# # from aiogram import Bot, Dispatcher, executor, types
# import asyncio

# # # Объект бота
# # bot = Bot(token="1921418522:AAGhuuELsBbOeby0OcjyjlGO5lqAbypl30c")
# # # Регистрация команд, отображаемых в интерфейсе Telegram


# async def set_commands(bot: Bot):
#     commands = [
#         types.BotCommand(command="/drinks", description="Заказать напитки"),
#         types.BotCommand(command="/food", description="Заказать блюда"),
#         types.BotCommand(command="/cancel",
#                          description="Отменить текущее действие")
#     ]
#     await bot.set_my_commands(commands)


# async def main():

#     bot = Bot(token='1921418522:AAGhuuELsBbOeby0OcjyjlGO5lqAbypl30c')
#     dp = Dispatcher(bot)

#     @dp.message_handler(commands="drinks")
#     async def cmd_test1(message: types.Message):
#         await message.reply("Test 1")

#     # Установка команд бота
#     await set_commands(bot)

#     # Запуск поллинга
#     # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
#     await dp.start_polling()

# if __name__ == '__main__':
#     asyncio.run(main())


# API_TOKEN = '1921418522:AAGhuuELsBbOeby0OcjyjlGO5lqAbypl30c'


# bot = Bot(token=API_TOKEN)

# # For example use simple MemoryStorage for Dispatcher.
# storage = MemoryStorage()
# dp = Dispatcher(bot, storage=storage)

# # States


# class Form(StatesGroup):
#     name = State()  # Will be represented in storage as 'Form:name'
#     age = State()  # Will be represented in storage as 'Form:age'
#     gender = State()  # Will be represented in storage as 'Form:gender'


# @dp.message_handler(commands="test4")
# async def with_hidden_link(message: types.Message):
#     print(message.chat.id)
#     await message.answer(
#         f"{fmt.hide_link('https://www.prikol.ru/wp-content/gallery/november-2011/geirangerfjord-01-big.jpg')}Кто бы мог подумать, что "
#         f"в 2020 году в Telegram появятся видеозвонки!\n\nОбычные голосовые вызовы "
#         f"возникли в Telegram лишь в 2017, заметно позже своих конкурентов. А спустя три года, "
#         f"когда огромное количество людей на планете приучились работать из дома из-за эпидемии "
#         f"коронавируса, команда Павла Дурова не растерялась и сделала качественные "
#         f"видеозвонки на WebRTC!\n\nP.S. а ещё ходят слухи про демонстрацию своего экрана :)",
#         parse_mode=types.ParseMode.HTML)


# @dp.message_handler(commands='start')
# async def cmd_start(message: types.Message):
#     """
#     Conversation's entry point
#     """
#     # Set state
#     await Form.name.set()

#     await message.reply("Hi there! What's your name?")


# # You can use state '*' if you need to handle all states
# @dp.message_handler(state='*', commands='cancel')
# @dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
# async def cancel_handler(message: types.Message, state: FSMContext):
#     """
#     Allow user to cancel any action
#     """
#     current_state = await state.get_state()
#     if current_state is None:
#         return

#     logging.info('Cancelling state %r', current_state)
#     # Cancel state and inform user about it
#     await state.finish()
#     # And remove keyboard (just in case)
#     await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


# @dp.message_handler(state=Form.name)
# async def process_name(message: types.Message, state: FSMContext):
#     """
#     Process user name
#     """
#     async with state.proxy() as data:
#         data['name'] = message.text

#     await message.reply("How old are you?")


# # Check age. Age gotta be digit
# @dp.message_handler(lambda message: not message.text.isdigit(), state=Form.age)
# async def process_age_invalid(message: types.Message):
#     """
#     If age is invalid
#     """
#     return await message.reply("Age gotta be a number.\nHow old are you? (digits only)")


# @dp.message_handler(lambda message: message.text.isdigit(), state=Form.age)
# async def process_age(message: types.Message, state: FSMContext):
#     # Update state and data
#     await Form.next()
#     await state.update_data(age=int(message.text))

#     # Configure ReplyKeyboardMarkup
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
#     markup.add("Male", "Female")
#     markup.add("Other")

#     await message.reply("What is your gender?", reply_markup=markup)


# @dp.message_handler(lambda message: message.text not in ["Male", "Female", "Other"], state=Form.gender)
# async def process_gender_invalid(message: types.Message):
#     """
#     In this example gender has to be one of: Male, Female, Other.
#     """
#     return await message.reply("Bad gender name. Choose your gender from the keyboard.")


# @dp.message_handler(state=Form.gender)
# async def process_gender(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['gender'] = message.text

#         # Remove keyboard
#         markup = types.ReplyKeyboardRemove()

#         # And send message
#         await bot.send_message(
#             message.chat.id,
#             md.text(
#                 md.text('Hi! Nice to meet you,', md.bold(data['name'])),
#                 md.text('Age:', md.code(data['age'])),
#                 md.text('Gender:', data['gender']),
#                 sep='\n',
#             ),
#             reply_markup=markup,
#             parse_mode=ParseMode.MARKDOWN,
#         )

#     # Finish conversation
#     await state.finish()


# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True)


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


class Game(StatesGroup):
    question = State()
    typesOfPosts = State()


async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(command="/profile", description="Мой профиль"),
        types.BotCommand(command="/search", description="Поиск мероприятия"),
        types.BotCommand(command="/tooday",
                         description="Мероприятия на сегодня"),
        types.BotCommand(command="/yesterday",
                         description="Мероприятия на завтра"),
        types.BotCommand(command="/game",
                         description="Игра «Угадай комика»"),
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

        await message.answer(title, reply_markup=markup)

    @bot.message_handler()
    async def send_text(message: types.Message, state: FSMContext):
        if message.text.lower() == 'мой профиль':
            cities = requests.get(
                'http://127.0.0.1:8000/api/user/get/' + str(message.chat.id)).json()

            textAbout = "<b>Ваш профиль:</b>\n\nВаш уникальный номер: <u>{0}</u>\nВаш город: <u>{1}</u>\nВаше количество очков: <u>{2}</u>\n\nКоличество сыграных разов\nв  «Угадай комика»: <u>{3}</u>\n".format(
                cities["token"], cities["location"]["name"], cities["points"], cities["questions"])
            markup = types.ReplyKeyboardMarkup(True, True)
            changeLocation = types.KeyboardButton('Поменять город')
            markup.add(changeLocation)
            await message.answer(textAbout, parse_mode=types.ParseMode.HTML, reply_markup=markup)

        if message.text.lower() == 'поменять город':
            cities = requests.get('http://127.0.0.1:8000/api/city/get/').json()
            markup = types.ReplyKeyboardMarkup(True, True)
            for i in range(0, len(cities)):
                markup.add(types.KeyboardButton(cities[i]['name']))
            markup.add(types.KeyboardButton('Другое'))

            title = 'Выбери город'
            await message.answer(title, reply_markup=markup)

        cities = requests.get('http://127.0.0.1:8000/api/city/get/').json()
        for i in range(0, len(cities)):
            if message.text.lower() == cities[i]['name']:
                create = requests.get(
                    'http://127.0.0.1:8000/api/user/reg/{0}/{1}'.format(message.chat.id, message.text))

                markup = types.ReplyKeyboardMarkup(True, True)
                search = types.KeyboardButton('Поиск мероприятия')
                game = types.KeyboardButton('Игра «Угадай комика»')
                setting = types.KeyboardButton('Мой профиль')
                markup.add(search, game, setting)

                await message.answer('Привет, чего ты хочешь ?', reply_markup=markup)

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
            await message.answer('К сожалению я пока ищу только в {} но это ненадолго. Напиши из какого ты города и я уведомлю, когда смогу тебе помогать.'.format(
                cityText), reply_markup=markup)

        if message.text.lower() == 'игра «угадай комика»':
            markup = types.ReplyKeyboardMarkup(True, True)
            photo = types.KeyboardButton('Угадай комика по фотке')
            joke = types.KeyboardButton('Угадай комика по шутке')

            markup.add(photo, joke)
            await message.answer('Выберите как вы хотите как вы хотите искать', reply_markup=markup)

        if message.text.lower() == 'угадай комика по шутке':
            startGame = requests.get(
                'http://127.0.0.1:8000/api/action/create/{0}/0/'.format(message.chat.id)).json()
            markup = types.ReplyKeyboardMarkup(True, True)
            back = types.KeyboardButton('На главную')
            markup.add(back)
            await message.answer(startGame["question"]["question"], reply_markup=markup)
            await Game.question.set()

        if message.text.lower() == 'поиск мероприятия':
            human = requests.get('http://127.0.0.1:8000/api/types/get/').json()
            markup = types.ReplyKeyboardMarkup(True, True)
            for i in range(0, len(human)):
                markup.add(types.KeyboardButton(human[i]['name']))
            await message.answer('Выберите какой тип мероприятий', reply_markup=markup)

        human = requests.get('http://127.0.0.1:8000/api/types/get/').json()
        for i in range(0, len(human)):
            if message.text.lower() == human[i]['name']:
                await Game.typesOfPosts.set()
                state.update_data(typesOfPosts=message.text)
                markup = types.ReplyKeyboardMarkup(True, True)
                tooday = types.KeyboardButton('Сегодня')
                toomorrow = types.KeyboardButton('Завтра')
                inWeek = types.KeyboardButton('На этой неделе')
                top = types.KeyboardButton('Топ на месяц')
                location = types.KeyboardButton('Поиск по геолокации')
                markup.add(tooday, toomorrow, inWeek, top, location)
                await message.answer('Выберите как вы хотите как вы хотите искать', reply_markup=markup)

    @bot.message_handler(state=Game.question)
    async def send_text(message: types.Message, state: FSMContext):
        if not message.text == 'На главную':
            getHuman = requests.get(
                'http://127.0.0.1:8000/api/action/get/{0}'.format(message.chat.id)).json()
            if message.text == getHuman["question"]["human"]["name"]:
                requests.get('http://127.0.0.1:8000/api/user/add/points/{0}/{1}'.format(
                    message.chat.id, getHuman["question"]["points"]))

                await message.answer('Праавильно, на ваш профиль зачислено {0} очков'.format(
                    getHuman["question"]["points"]))

                startGame = requests.get(
                    'http://127.0.0.1:8000/api/action/create/{0}/0/'.format(message.chat.id)).json()
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
            search = types.KeyboardButton('Поиск мероприятия')
            game = types.KeyboardButton('Игра «Угадай комика»')
            setting = types.KeyboardButton('Мой профиль')
            title = 'Привет, чего ты хочешь ?'
            markup.add(search, game, setting)
            await message.answer(title, reply_markup=markup)

    @bot.message_handler(state=Game.typesOfPosts)
    async def send_text(message: types.Message, state: FSMContext):
        current_state = await state.get_state()
        await message.answer(current_state['typesOfPosts'])

    await set_commands(botInit)
    await bot.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
