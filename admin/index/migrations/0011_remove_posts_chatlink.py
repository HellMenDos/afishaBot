# Generated by Django 3.1.4 on 2021-08-02 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0010_auto_20210802_1225'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='chatlink',
        ),
    ]