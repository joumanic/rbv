from django.urls import path, include
from . import views
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    path('api/', include('radio_buena_vida.urls')),
    path('admin/', admin.site.urls),  
    path('/', TemplateView.as_view(template_name='index.html')), 
]
