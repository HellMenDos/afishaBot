from django.db import models
from index.models import City, Game, Human


class User(models.Model):
    token = models.CharField(max_length=100, verbose_name='Токен пользователя')
    location = models.ForeignKey(
        City, on_delete=models.DO_NOTHING, verbose_name="Город")
    points = models.IntegerField(default=0, verbose_name='Количество баллов ')
    date = models.DateTimeField(
        verbose_name='Время регистрации', auto_now=True, blank=True)

    def __str__(self):
        return f'{self.token}  {self.location}'

    class Meta:
        verbose_name = 'Пользователи бота'
        verbose_name_plural = 'Пользователи бота'


class Actions(models.Model):

    user = models.OneToOneField(
        User, on_delete=models.DO_NOTHING, verbose_name="Пользователь")
    question = models.ForeignKey(
        Game, default=0, on_delete=models.DO_NOTHING, verbose_name="вопрос")

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = 'Действие пользователей'
        verbose_name_plural = 'Действия пользователей'


class Idols(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                             related_name='user', verbose_name="Пользователь")
    humans = models.ManyToManyField(
        Human, related_name='humans', verbose_name="Кумиры")

    def __str__(self):
        return f'{self.user} {self.humans}'

    class Meta:
        verbose_name = 'Кумир'
        verbose_name_plural = 'Кумиры'


class Push(models.Model):
    title = models.CharField(max_length=100, verbose_name='Оглавление')
    describe = models.TextField(verbose_name="Описание")
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING,
                             related_name='city', default=0, verbose_name="Город отправки")
    photo = models.ImageField(
        upload_to='push', blank=True, null=True, verbose_name='Фото уведомления')

    def __str__(self):
        return f'{self.title} {self.describe}'

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'


class Stat(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                             related_name='user_stat', verbose_name="Пользователь")
    action = models.CharField(
        max_length=100, verbose_name="Действие пользователя")
    date = models.DateTimeField(
        verbose_name='Время действия', auto_now=True, blank=True)

    def __str__(self):
        return f'{self.user} {self.action}'

    class Meta:
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистика'
