# Generated by Django 3.1.7 on 2021-08-04 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_auto_20210804_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stat',
            name='action',
            field=models.CharField(max_length=100, verbose_name='Действие пользователя'),
        ),
    ]