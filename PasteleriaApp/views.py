from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegisterForm
from django.contrib import messages

# Create your views here.

def inicio(request):

    return render(request, 'inicio.html')

def compras(request):

    return render(request, 'compras.html')

def pastel(request):

    return render(request, 'pastel.html')

def register(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            messages.success(
                request, f'Usuario {username} creado con exito')
            usuario = authenticate(username=email, password=password)
            login(request, usuario)
            return redirect('')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})
