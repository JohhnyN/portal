# Generated by Django 5.1.4 on 2024-12-17 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phonebook', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CityPhoneNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=20, verbose_name='Городской номер телефона')),
            ],
            options={
                'verbose_name': 'Городской номер телефона',
                'verbose_name_plural': 'Городские номера телефонов',
            },
        ),
    ]