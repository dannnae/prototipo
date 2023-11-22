from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_to_home),
    path('login', views.login_paciente, name='login'),
    path('index', views.index, name='index'),
    path('registro_paciente', views.register_paciente, name='registro_paciente'),
    path('paciente_cuenta', views.CitaListView.as_view(), name='paciente_cuenta'),
    path('logout_paciente', views.logout_paciente, name='logout_paciente'),
    path('mostrar_medicos/', views.mostrar_medicos, name='mostrar_medicos'),

    path('crear-medico/', views.crear_medico, name='crear_medico'),
    path('crear-disponibilidad/<int:medico_id>/', views.crear_disponibilidad, name='crear_disponibilidad'),


    path('citas/', views.CitaListView.as_view(), name='cita_list'),
    path('citas/nueva/<int:medico_id>/', views.CitaCreateView.as_view(), name='cita_create'),
    path('citas/<int:pk>/editar/', views.CitaUpdateView.as_view(), name='cita_update'),
    path('citas/<int:pk>/eliminar/', views.CitaDeleteView.as_view(), name='cita_delete'),
    
]