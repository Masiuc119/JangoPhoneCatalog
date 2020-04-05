from django.shortcuts import get_object_or_404, render, redirect

from .models import PhoneCatalog


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
            "message": message
        }
    )
