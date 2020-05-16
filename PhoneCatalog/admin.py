from django.contrib import admin

from .models import PhoneCatalog
from .models import Message

admin.site.register(PhoneCatalog)
admin.site.register(Message)
