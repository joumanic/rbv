from django.db import models
import json

# Create your models here.

class RadioShow(models.Model):
    host_name = models.CharField(max_length=255)
    show_name = models.CharField(max_length=255)
    genre1 = models.CharField(max_length=100, default='')
    genre2 = models.CharField(max_length=100, default='')
    genre3 = models.CharField(max_length=100, default='')
    socials = models.TextField(blank=True, null=True)
    show_image = models.URLField(max_length=200, blank=True, null=True) 

    def set_socials(self, socials_list):
        self.socials = json.dumps(socials_list)  # Serialize list as JSON

    def get_socials(self):
        return json.loads(self.socials)  # Deserialize JSON into list

    def __str__(self):
        return self.show_name
