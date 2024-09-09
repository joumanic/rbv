from django.urls import path
from . import views

urlpatterns = [
    path('api/radio-show/', views.RadioShowCreateView.as_view(), name='radio-show-create'),
]
