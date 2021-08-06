from urllib import request
from django.db import models
from django.db.models.fields import CharField
from django.db.models.signals import post_save
from django.dispatch import receiver


class City(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название города')
    describe = models.TextField(verbose_name='Описание города')

    def __str__(self):
        return f'({self.name})'

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class TypeOfPosts(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название типа поста')
    describe = models.TextField(verbose_name='Описание типа')

    def __str__(self):
        return f'({self.name})'

    class Meta:
        verbose_name = 'Тип мероприятия (скрыто)'
        verbose_name_plural = 'Типы мероприятий (скрыто)'


class Human(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя человека')
    describe = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f'({self.name})'

    class Meta:
        verbose_name = 'Выступающий / Комик / Ведущий'
        verbose_name_plural = 'Выступающие / Комики / Ведущие'


class Posts(models.Model):

    COST_TYPE = (
        (0, 'Обычная плата'),
        (1, 'Депозит'),
        (2, 'Донат'),
    )

    title = models.CharField(max_length=100, verbose_name='Оглавление поста')
    describe = models.TextField(verbose_name='Описание поста')
    location = models.CharField(max_length=200, verbose_name='Местоположение')
    cost = models.IntegerField(default=0, blank=True,
                               verbose_name='цена (р)')
    costType = models.IntegerField(
        default=0, verbose_name='Тип цены', choices=COST_TYPE)
    typeOfPost = models.ForeignKey(
        TypeOfPosts, on_delete=models.DO_NOTHING, verbose_name="Тип поста")
    human = models.ManyToManyField(
        Human, related_name='humans_post', verbose_name="Выступающий")
    theBest = models.BooleanField(
        default=False, verbose_name="Лучшее на месяц")
    timeStart = models.DateTimeField(verbose_name='Вход')
    timeEnd = models.DateTimeField(verbose_name='Начало')
    photo = models.ImageField(
        upload_to='post', blank=True, null=True, verbose_name='Фото поста')
    paid = models.BooleanField(default=False, verbose_name='Оплачено')
    linkForChat = models.CharField(
        max_length=500, default='', blank=True, verbose_name='Ссылка на чат')
    link = models.CharField(max_length=500, blank=True, default='',
                            verbose_name='Ссылка на покупку')
    linkRegistr = models.CharField(max_length=500, blank=True, default='',
                                   verbose_name='Ссылка на регистрацию')
    sended = models.BooleanField(default=False, verbose_name='Оповещено')

    def __str__(self):
        return f'{self.title}  {self.timeStart}'

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'


# @receiver(post_save, sender=Posts)
# def posts_update(sender, instance, created, **kwargs):
#     for i in range(0, len(instance.human.all())):
#         idolId = instance.human.all()[i].id
#         userToken = Idols.objects.filter(humans__in=[idolId]).first()
#     print(instance.human.all()[0].id)
#     print(len(instance.human_list.all()))

# @receiver(post_save, sender=Posts)
# def posts_update(sender, instance, created, **kwargs):
#     for i in range(0, len(instance.human.all())):
#         idolId = instance.human.all()[i].id
#         userToken = requests.get(
#             f'http://127.0.0.1:8000/api/get/token/idols/{idolId}').json()
#         method = "sendMessage"
#         token = "1921418522:AAGhuuELsBbOeby0OcjyjlGO5lqAbypl30c"
#         url = f"https://api.telegram.org/bot{token}/{method}"

#         markup = []
#         if instance.link:
#             markup.add(
#                 [{'text': 'Ссылка на покупку', 'url': instance.link}])
#         if instance.linkForChat:
#             markup.add(
#                 [{'text': 'Ссылка на чат', 'url': instance.linkForChat}])
#         if instance.linkRegistr:
#             markup.add(
#                 [{'text': 'Ссылка на регистрацию', 'url': instance.linkRegistr}])

#         data = {"chat_id": userToken['user'],
#                 "text": f"<b>{instance.title}</b> \n\n"
#                 f"{instance.describe} \n"
#                 f"Местоположение: {instance.location} \n\n"
#                 f"Начало:  <u>{str(instance.timeStart).split('T')[0]}</u>\n"
#                 f"Вход:  <u>{str(instance.timeEnd).split('T')[0]}</u>\n\n"
#                 f"Цена: {str(instance.cost) + ' р.' if instance.cost else 'Бесплатно'} \n",
#                 'parse_mode': types.ParseMode.HTML,
#                 'reply_markup': json.dumps({'inline_keyboard': [markup],
#                                             'resize_keyboard': True,
#                                             'one_time_keyboard': True,
#                                             'selective': True})
#                 }
#         data = requests.post(url, data=data)


class Game(models.Model):
    human = models.ForeignKey(
        Human, on_delete=models.DO_NOTHING, verbose_name="Человек которого надо угадать")
    photo = models.ImageField(
        upload_to='game', blank=True, null=True, verbose_name='Фото человека')
    question = models.TextField(blank=True, verbose_name='Вопрос')
    points = models.IntegerField(default=0, verbose_name='Количество баллов')

    def __str__(self):
        return f'{self.question}  {self.points}'

    class Meta:
        verbose_name = 'Игра (Угадай Комика)'
        verbose_name_plural = 'Игра (Угадай Комика)'
