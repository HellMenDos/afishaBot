# Generated by Django 3.1.4 on 2021-07-24 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0005_auto_20210724_1201'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='link',
            field=models.CharField(default='', max_length=500, verbose_name='Ссылка на покупку'),
        ),
        migrations.AddField(
            model_name='posts',
            name='linkForChat',
            field=models.CharField(default='', max_length=500, verbose_name='Ссылка на чат'),
        ),
    ]
