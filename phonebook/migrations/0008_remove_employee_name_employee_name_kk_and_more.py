# Generated by Django 5.1.4 on 2024-12-23 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phonebook', '0007_alter_cityphonenumber_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='name',
        ),
        migrations.AddField(
            model_name='employee',
            name='name_kk',
            field=models.CharField(default=2, max_length=300, verbose_name='ФИО на казахском'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employee',
            name='name_ru',
            field=models.CharField(default=1, max_length=300, verbose_name='ФИО на русском'),
            preserve_default=False,
        ),
    ]