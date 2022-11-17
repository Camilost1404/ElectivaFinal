from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Usuario')
    first_name = forms.CharField(label='Nombre')
    last_name = forms.CharField(label='Apellido')
    direccion = forms.CharField(label='Dirección')
    email = forms.EmailField()
    password1 = forms.CharField(
        label='Contraseña:', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirmar Contraseña:', widget=forms.PasswordInput)
    telefono = forms.IntegerField(label='Teléfono', min_value=0, widget=forms.TextInput)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'direccion', 'telefono']
        help_texts = {k: '' for k in fields}

    def clean_email(self):
        email = self.cleaned_data['email']

        if email.split('@')[1] not in ['gmail.com', 'hotmail.com']:
            raise forms.ValidationError('Coloca un Email Válido')
        return email

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']

        if len(str(telefono)) != 10:
            raise forms.ValidationError('Ingrese un número valido')
        return telefono