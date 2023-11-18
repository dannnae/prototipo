from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_paciente, name='login'),
    path('index', views.index, name='index'),
    path('registro_paciente', views.register_paciente, name='registro_paciente'),
    path('paciente_cuenta', views.CitaListView.as_view(), name='paciente_cuenta'),
    path('logout_paciente', views.logout_paciente, name='logout_paciente'),

    path('citas/nueva/', views.CitaCreateView.as_view(), name='cita_create'),
    path('citas/<int:pk>/editar/', views.CitaUpdateView.as_view(), name='cita_update'),
    path('citas/<int:pk>/eliminar/', views.CitaDeleteView.as_view(), name='cita_delete'),
]