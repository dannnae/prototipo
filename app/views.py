from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as auth_login, logout


def index(request):
    if request.user.is_authenticated:
        user_logged_in = True
    else:
        user_logged_in = False

    usuario = request.user

    context = {'user_logged_in': user_logged_in, 'usuario': usuario}
    return render(request, "index.html", context)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            request.session['user_logged_in'] = True
            return redirect('index') 
        
        else:
            error_message = 'Nombre de usuario o contraseña incorrectos'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')
    
def logout_view(request):
    logout(request)
    return redirect('index') 

def cita(request):
    return render(request, "cita.html")

def agendar(request):
    return render(request, "agendar.html")