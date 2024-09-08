from django.contrib import admin
from .models import RadioShow

@admin.register(RadioShow)
class RadioShowAdmin(admin.ModelAdmin):
    list_display = ('host_name', 'show_name', 'genre_1', 'genre_2', 'genre_3', 'show_image')
