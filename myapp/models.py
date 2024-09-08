from django.db import models

# Create your models here.

class RadioShow(models.Model):
    host_name = models.CharField(max_length=255)
    show_name = models.CharField(max_length=255)
    genre_1 = models.CharField(max_length=100)
    genre_2 = models.CharField(max_length=100, blank=True, null=True)
    genre_3 = models.CharField(max_length=100, blank=True, null=True)
    show_image = models.URLField(max_length=200, blank=True, null=True) 

    def __str__(self):
        return self.show_name
