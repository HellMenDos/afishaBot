from django.db import models
from index.models import City


class User(models.Model):
    token = models.CharField(max_length=100, verbose_name='Оглавление поста')
    location = models.ForeignKey(
        City, on_delete=models.DO_NOTHING, verbose_name="Город")
    points = models.IntegerField(default=0, verbose_name='Количество баллов ')
    top = models.IntegerField(
        default=0, verbose_name='Количество нажатий на топ месяца')
    tooday = models.IntegerField(
        default=0, verbose_name='Количество нажатий на сегодня')
    yesterday = models.IntegerField(
        default=0, verbose_name='Количество нажатий на вчера')
    questions = models.IntegerField(
        default=0, verbose_name='Количество отвеченных вопросов')

    def __str__(self):
        return f'{self.token}  {self.location}'

    class Meta:
        verbose_name = 'Пользователи бота'
        verbose_name_plural = 'Пользователи бота'
