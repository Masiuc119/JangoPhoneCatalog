# Generated by Django 3.0.5 on 2020-05-16 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PhoneCatalog', '0002_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='chat',
        ),
    ]