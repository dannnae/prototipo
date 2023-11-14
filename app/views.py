from django.shortcuts import redirect, render
from .forms import PacienteLoginForm, PacienteRegistrationForm, MultiUsuarioLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



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
            return redirect('index')
    else:
        form = PacienteRegistrationForm()

    return render(request, 'registro_paciente.html', {'form': form})

def cita(request):
    return render(request, "cita.html")

def agendar(request):
    return render(request, "agendar.html")

def paciente(request):
    return render(request, "paciente.html")