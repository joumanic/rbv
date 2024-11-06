from django.contrib import admin
from .models import RadioShow

@admin.register(RadioShow)
class RadioShowAdmin(admin.ModelAdmin):
    list_display = ('host_name', 'show_name', 'genre1', 'genre2', 'genre3', 'show_image')
