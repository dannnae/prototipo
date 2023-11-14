from django.contrib.auth import authenticate
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Paciente, Medico, Secretaria

class PacienteRegistrationForm(UserCreationForm):
    rut = forms.CharField(max_length=20)
    nombre = forms.CharField(max_length=100)
    email = forms.EmailField()
    telefono = forms.CharField(max_length=15)

    class Meta:
        model = Paciente
        fields = ['rut', 'nombre', 'email', 'telefono', 'password1', 'password2']

class PacienteLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'autofocus': True}))

    class Meta:
        model = Paciente


class MultiUsuarioLoginForm(AuthenticationForm):
    
    def clean(self):
        rut = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if rut is not None and password:
            users = {
                'patient': authenticate(
                    self.request, username=rut, password=password, UserModel=Paciente 
                ),
                'medic': authenticate(
                    self.request, username=rut, password=password, UserModel=Medico 
                ),
                'secretary': authenticate(
                    self.request, username=rut, password=password, UserModel=Secretaria 
                )
            }

            if all([True if user is None else False for user in users.values()]):
                raise self.get_invalid_login_error()
            else:
                for user in users.values():
                    if user is not None:
                        self.user_cache = user
                        self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    