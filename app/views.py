import json
from django.urls import reverse as django_reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from .forms import CitaForm, PacienteRegistrationForm, MultiUsuarioLoginForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Cita, Disponibilidad, Medico

def redirect_to_home(request):
    return redirect('index')

def index(request):
    if request.user.is_authenticated:
        user_logged_in = True
    else:
        user_logged_in = False

    usuario = request.user
        
    context = {'user_logged_in': user_logged_in, 'usuario': usuario}
    return render(request, "index.html", context)

def login_paciente(request):
    if request.method == 'POST':
        form = MultiUsuarioLoginForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
        
    else:
        form = MultiUsuarioLoginForm()

    return render(request, 'login.html', {'form': form})

def logout_paciente(request):
    logout(request)
    return redirect('index')

def register_paciente(request):
    if request.method == 'POST':
        form = PacienteRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = PacienteRegistrationForm()

    return render(request, 'registro_paciente.html', {'form': form})


class CitaListView(ListView):
    model = Cita
    template_name = 'paciente_cuenta.html' 

    def get_queryset(self):
        return Cita.objects.filter(paciente=self.request.user)
    
    def render_to_response(self, context, **response_kwargs):
        context['user_logged_in'] = self.request.user.is_authenticated
        context['usuario'] = self.request.user
        return super().render_to_response(context, **response_kwargs)

class CitaCreateView(CreateView):
    model = Cita
    form_class = CitaForm
    template_name = 'cita_form.html'
    success_url = reverse_lazy('paciente_cuenta')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        medico = Medico.objects.get(pk=self.kwargs.get('medico_id'))
        context['medico'] = medico

        dias = {
            1: 'Lunes',
            2: 'Martes',
            3: 'Miércoles',
            4: 'Jueves',
            5: 'Viernes',
            6: 'Sábado',
            0: 'Domingo',
        }
        disponibilidad = medico.disponibilidad_medico.all()
        disponibilidad_dias = disponibilidad.values_list('diaSemana', flat=True)
        context['disponibilidadDias'] = json.dumps([i for i, dia in dias.items() if dia not in disponibilidad_dias])

        return context

    def form_valid(self, form):
        form.instance.paciente = self.request.user
        form.instance.medico_id = self.kwargs.get('medico_id')
        return super().form_valid(form)


class CitaUpdateView(UpdateView):
    model = Cita
    fields = ['fechaHora', 'estado', 'medico', 'paciente']  
    template_name = 'cita_form.html' 
    success_url = reverse_lazy('cita_list')  


class CitaDeleteView(DeleteView):
    model = Cita
    template_name = 'cita_delete.html'  
    success_url = reverse_lazy('paciente_cuenta') 

#vista para crear medicos
def crear_medico(request):
    if request.method == 'POST':
        rut = request.POST['rut']
        nombre = request.POST['nombre']
        especialidad = request.POST['especialidad']

        nuevo_medico = Medico.objects.create(rut=rut, nombre=nombre, especialidad=especialidad)
        nuevo_medico.save()

        return HttpResponseRedirect(f'/crear-disponibilidad/{nuevo_medico.id}/')

    return render(request, 'crear_medico.html')

#CREAR DISPONIBILIDAD MEDICOS
def crear_disponibilidad(request, medico_id):
    medico = get_object_or_404(Medico, id=medico_id)

    if request.method == 'POST':
        fecha = request.POST['fecha']
        hora_inicio = request.POST['hora_inicio']
        hora_fin = request.POST['hora_fin']
        dia_semana = request.POST['dia_semana']

        nueva_disponibilidad = Disponibilidad.objects.create(medico=medico, fecha=fecha, horaInicio=hora_inicio, horaFin=hora_fin, diaSemana=dia_semana)
        nueva_disponibilidad.save()


        medico.disponibilidad = nueva_disponibilidad
        medico.save()

        return HttpResponseRedirect(django_reverse('index'))

    return render(request, 'crear_disponibilidad.html', {'medico': medico})

@login_required
def mostrar_medicos(request):
    medicos = Medico.objects.all()
    return render(request, 'mostrar_medicos.html', {'medicos': medicos})

