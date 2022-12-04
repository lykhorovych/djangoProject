from django.contrib import admin
from .models import Pizzeria, Snippet, Album, Track

# Register your models here.
admin.site.register(Pizzeria)
admin.site.register(Snippet)
admin.site.register(Album)
admin.site.register(Track)