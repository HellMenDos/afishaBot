# Generated by Django 3.1.4 on 2021-08-03 12:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_auto_20210802_0744'),
    ]

    operations = [
        migrations.AddField(
            model_name='push',
            name='city',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING,
                                    related_name='city', to='index.city', verbose_name='Город отправки'),
        ),
    ]
