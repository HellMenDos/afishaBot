# Generated by Django 3.1.4 on 2021-07-26 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0008_auto_20210726_0929'),
        ('user', '0007_auto_20210726_1000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idols',
            name='human',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, related_name='humans', to='index.human', verbose_name='Кумир'),
        ),
    ]