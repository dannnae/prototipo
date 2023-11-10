from django.shortcuts import render

def login(request):
    return render(request, "login.html")

def cita(request):
    return render(request, "cita.html")

def agendar(request):
    return render(request, "agendar.html")