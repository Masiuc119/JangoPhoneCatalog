from django.conf.urls import url

from . import views

app_name = 'PhoneCatalog'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.RegisterFormView.as_view()),
    url(r'^login/$', views.LoginFormView.as_view()),
    url(r'^logout/$', views.LogoutView.as_view()),
    url(r'^password-change/', views.PasswordChangeView.as_view()),
    # отправка сообщения
    url(r'^post/$', views.post, name='post/'),
    url(r'^msg_list/$', views.msg_list, name='msg_list'),

]
