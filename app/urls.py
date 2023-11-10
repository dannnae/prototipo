from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('cita', views.cita, name='cita'),
    path('agendar', views.agendar, name='agendar'),
]