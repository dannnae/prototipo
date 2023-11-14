from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_paciente, name='login'),
    path('cita', views.cita, name='cita'),
    path('agendar', views.agendar, name='agendar'),
    path('index', views.index, name='index'),
    path('registro_paciente', views.register_paciente, name='registro_paciente'),
]