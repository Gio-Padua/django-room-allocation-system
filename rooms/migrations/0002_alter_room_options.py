# Generated by Django 5.1 on 2024-08-21 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='room',
            options={'verbose_name_plural': 'Rooms'},
        ),
    ]