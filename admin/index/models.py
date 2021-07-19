from django.db import models
from django.db.models.fields import CharField


class City(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название города')
    describe = models.TextField(verbose_name='Описание города')

    def __str__(self):
        return f'({self.name})'

    class Meta:
        verbose_name = 'Название города'
        verbose_name_plural = 'Название городов'


class TypeOfPosts(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название типа поста')
    describe = models.TextField(verbose_name='Описание типа')

    def __str__(self):
        return f'({self.name})'

    class Meta:
        verbose_name = 'Тип поста'
        verbose_name_plural = 'Типы постов'


class Human(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя человека')
    describe = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f'({self.name})'

    class Meta:
        verbose_name = 'Выступающий'
        verbose_name_plural = 'Выступающие'


class Posts(models.Model):
    title = models.CharField(max_length=100, verbose_name='Оглавление поста')
    describe = models.TextField(verbose_name='Описание поста')
    location = models.CharField(max_length=200, verbose_name='Местоположение')
    cost = models.CharField(max_length=200, blank=True,
                            verbose_name='цена (р)')
    typeOfPost = models.ForeignKey(
        TypeOfPosts, on_delete=models.DO_NOTHING, verbose_name="Тип поста")
    human = models.ForeignKey(
        Human, on_delete=models.DO_NOTHING, verbose_name="Выступающий")
    theBest = models.BooleanField(
        default=False, verbose_name="Лучшее на месяц")
    timeStart = models.DateTimeField(verbose_name='Время начала')
    timeEnd = models.DateTimeField(verbose_name='Время конца')
    photo = models.ImageField(
        upload_to='post', blank=True, null=True, verbose_name='Фото поста')
    paid = models.BooleanField(default=False, verbose_name='Оплачено')

    def __str__(self):
        return f'{self.title}  {self.timeStart}'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Game(models.Model):
    human = models.ForeignKey(
        Human, on_delete=models.DO_NOTHING, verbose_name="Человек которого надо угадать")
    photo = models.ImageField(
        upload_to='game', blank=True, null=True, verbose_name='Фото человека')
    question = models.TextField(verbose_name='Вопрос')
    points = models.IntegerField(default=0, verbose_name='Количество баллов')

    def __str__(self):
        return f'{self.question}  {self.points}'

    class Meta:
        verbose_name = 'Игра (Угадай Комика)'
        verbose_name_plural = 'Игра (Угадай Комика)'
