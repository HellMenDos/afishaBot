# Generated by Django 3.1.4 on 2021-08-02 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0008_auto_20210726_0929'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='costType',
            field=models.IntegerField(choices=[(0, 'Обычная плата'), (1, 'Депозит'), (2, 'Залог')], default=0, verbose_name='Тип цены'),
        ),
    ]
