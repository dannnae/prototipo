from typing import Any
from django import http
from django.db import models
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from .forms import CitaForm, PacienteLoginForm, PacienteRegistrationForm, MultiUsuarioLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Cita



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
    success_url = reverse_lazy('cita_list')

    def form_valid(self, form):
        form.instance.paciente = self.request.user
        return super().form_valid(form)


class CitaUpdateView(UpdateView):
    model = Cita
    fields = ['fechaHora', 'estado', 'medico', 'paciente']  
    template_name = 'cita_form.html' 
    success_url = reverse_lazy('cita_list')  


class CitaDeleteView(DeleteView):
    model = Cita
    template_name = 'cita_confirm_delete.html'  
    success_url = reverse_lazy('cita_list')  
    