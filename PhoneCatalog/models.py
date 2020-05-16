from django.db import models
# встроенная модель пользователя
# нужна для авторов сообщений
from django.contrib.auth.models import User
# тип "временнАя зона" для получения текущего времени
from django.utils import timezone


class PhoneCatalog(models.Model):
    Name = models.CharField(max_length=255)
    RegDate = models.DateTimeField('date published')
    Address = models.CharField(max_length=255)
    Phone = models.CharField(max_length=30)


class Message(models.Model):
    author = models.ForeignKey(
        User, verbose_name='Пользователь', on_delete=models.CASCADE)
    message = models.TextField('Сообщение')
    pub_date = models.DateTimeField(
        'Дата сообщения', default=timezone.now)
