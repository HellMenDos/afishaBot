# Generated by Django 3.1.4 on 2021-07-24 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0004_auto_20210724_0854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='question',
            field=models.TextField(blank=True, verbose_name='Вопрос'),
        ),
    ]
