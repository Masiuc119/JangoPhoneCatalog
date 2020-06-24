from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render, redirect

from .models import PhoneCatalog
# сообщения
from .models import Message
from datetime import datetime


# главная страница со списком загадок
def index(request):
    message = None
    if "message" in request.GET:
        message = request.GET["message"]
    # создание HTML-страницы по шаблону index.html
    # с заданными параметрами latest_riddles и message
    return render(
        request,
        "index.html",
        {
            "latest_phoneCatalog":
                PhoneCatalog.objects.order_by('-RegDate')[:5],
            "message": message,
            "latest_messages":
                Message.objects.order_by('-pub_date')[:5]

        }
    )


# Базовый класс для обработки страниц с формами.
from django.views.generic.edit import FormView
# Спасибо django за готовую форму регистрации.
from django.contrib.auth.forms import UserCreationForm

...
# базовый URL приложения, главной страницы -
# часто нужен при указании путей переадресации
app_url = "/PhoneCatalog/"


# наше представление для регистрации
class RegisterFormView(FormView):
    # будем строить на основе
    # встроенной в django формы регистрации
    form_class = UserCreationForm
    # Ссылка, на которую будет перенаправляться пользователь
    # в случае успешной регистрации.
    # В данном случае указана ссылка на
    # страницу входа для зарегистрированных пользователей.
    success_url = app_url + "login/"
    # Шаблон, который будет использоваться
    # при отображении представления.
    template_name = "reg/register.html"

    def form_valid(self, form):
        # Создаём пользователя,
        # если данные в форму были введены корректно.
        form.save()
        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)


# Спасибо django за готовую форму аутентификации.
from django.contrib.auth.forms import AuthenticationForm
# Функция для установки сессионного ключа.
# По нему django будет определять,
# выполнил ли вход пользователь.
from django.contrib.auth import login

...


# наше представление для входа
class LoginFormView(FormView):
    # будем строить на основе
    # встроенной в django формы входа
    form_class = AuthenticationForm
    # Аналогично регистрации,
    # только используем шаблон аутентификации.
    template_name = "reg/login.html"
    # В случае успеха перенаправим на главную.
    success_url = app_url

    def form_valid(self, form):
        # Получаем объект пользователя
        # на основе введённых в форму данных.
        self.user = form.get_user()
        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


# Для Log out с перенаправлением на главную
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import logout

...


# для выхода - миниатюрное представление без шаблона -
# после выхода перенаправим на главную
class LogoutView(View):
    def get(self, request):
        # Выполняем выход для пользователя,
        # запросившего данное представление.
        logout(request)
        # После чего перенаправляем пользователя на
        # главную страницу.
        return HttpResponseRedirect(app_url)


# Для смены пароля - форма
from django.contrib.auth.forms import PasswordChangeForm

...


# наше представление для смены пароля
class PasswordChangeView(FormView):
    # будем строить на основе
    # встроенной в django формы смены пароля
    form_class = PasswordChangeForm
    template_name = 'reg/password_change_form.html'
    # после смены пароля нужно снова входить
    success_url = app_url + 'login/'

    def get_form_kwargs(self):
        kwargs = super(PasswordChangeView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        if self.request.method == 'POST':
            kwargs['data'] = self.request.POST
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(PasswordChangeView, self).form_valid(form)


def post(request):
    msg = Message()
    msg.author = request.user
    msg.message = request.POST['message']
    msg.pub_date = datetime.now()
    msg.save()
    return HttpResponseRedirect(app_url)


# для ответа на асинхронный запрос в формате JSON
from django.http import JsonResponse
import json

...


def msg_list(request):
    # выбираем список сообщений
    res = list(
        Message.objects
            # отбираем 5 самых свежих
            .order_by('-pub_date')[:5]
            # выбираем необходимые поля
            .values('author__username',
                    'pub_date',
                    'message'
                    )
    )
    # конвертируем даты в строки - сами они не умеют
    for r in res:
        r['pub_date'] = \
            r['pub_date'].strftime(
                '%d.%m.%Y %H:%M:%S'
            )
    return JsonResponse(json.dumps(res), safe=False)


def admin(request):
    message = None
    if "message" in request.GET:
        message = request.GET["message"]
    # создание HTML-страницы по шаблону admin.html
    # с заданными параметрами latest_riddles и message
    return render(
        request,
        "admin.html",
        {
            "latest_phoneCatalog":
                PhoneCatalog.objects.order_by('RegDate')[:5],
            "message": message,
        }
    )


def post_phoneCatalog(request):
    # защита от добавления загадок неадминистраторами
    author = request.user
    if not (author.is_authenticated and author.is_staff):
        return HttpResponseRedirect(app_url + "admin")
    # добавление загадки
    phn = PhoneCatalog()
    phn.Name = request.POST['name']
    phn.Address = request.POST['address']
    phn.Phone = request.POST['phone']
    phn.RegDate = datetime.now()
    phn.save()
    # цикл по всем пользователям
    for i in User.objects.all():
        # проверка, что текущий пользователь подписан - указал e-mail
        if i.email != '':
            send_mail(
                # тема письма
                'Новая запись',
                # текст письма
                'На портале появилась новая запись:\n' +
                'http://localhost:8000/PhoneCatalog/' + '.',
                # отправитель
                'masiuc1.19.noreply@gmail.com',
                # список получателей из одного получателя
                [i.email],
                # отключаем замалчивание ошибок,
                # чтобы из видеть и исправлять
                False
            )

    return HttpResponseRedirect(app_url)


from django import forms
from django.utils.translation import gettext, gettext_lazy as _
# ...


# класс, описывающий логику формы:
# список заполняемых полей и их сохранение
class SubscribeForm(forms.Form):
    # поле для ввода e-mail
    email = forms.EmailField(
        label=_("E-mail"),
        required=True,
    )

    # конструктор для запоминания пользователя,
    # которому задается e-mail
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    # сохранение e-mail
    def save(self, commit=True):
        self.user.email = self.cleaned_data["email"]
        if commit:
            self.user.save()
        return self.user


# класс, описывающий взаимодействие логики
# со страницами веб-приложения
class SubscribeView(FormView):
    # используем класс с логикой
    form_class = SubscribeForm
    # используем собственный шаблон
    template_name = 'subscribe.html'
    # после подписки возвращаем на главную станицу
    success_url = app_url

    # передача пользователя для конструктора класса с логикой
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    # вызов логики сохранения введенных данных
    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)


# функция для удаления подписки (форма не нужна,
# поэтому без классов, просто функция)
def unsubscribe(request):
    request.user.email = ''
    request.user.save()
    return HttpResponseRedirect(app_url)
