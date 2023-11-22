from django.contrib.auth import authenticate
from django import forms 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from .models import Cita, Disponibilidad, Paciente, Medico, Secretaria

class PacienteRegistrationForm(UserCreationForm):
    rut = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'con puntos y guión'}))
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    telefono = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))


    class Meta:
        model = Paciente
        fields = ['rut', 'nombre', 'email', 'telefono', 'password1', 'password2']
        labels = {
            'email' : 'Correo',
            'telefono' : 'Teléfono',
            'password1' : 'Contraseña',
            'password2' : 'Confirmar contraseña',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for k, v in self.Meta.labels.items():
            self[k].label = v
    

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

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['fechaHora']

        widgets = {
            'fechaHora': DateTimePickerInput(),
        }


class DisponibilidadForm(forms.ModelForm):
    class Meta:
        model = Disponibilidad
        fields = ['fecha', 'horaInicio', 'horaFin', 'diaSemana']
