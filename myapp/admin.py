from django.contrib import admin
from .models import RadioShow

@admin.register(RadioShow)
class RadioShowAdmin(admin.ModelAdmin):
    list_display = ('email', 'host_name', 'show_name', 'genre1', 'genre2', 'genre3', 'socials', 'show_date','show_image', 'pre_record')
