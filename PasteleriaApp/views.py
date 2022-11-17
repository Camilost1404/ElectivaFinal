from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegisterForm
from django.contrib import messages
from PasteleriaApp.models import Cobertura, Relleno, Sabor
from PasteleriaApp.carrito import Carrito
from django.db import connection

# Create your views here.


def inicio(request):

    return render(request, 'inicio.html')


def compras(request):

    return render(request, 'compras.html')


def pastel(request):

    coberturas = Cobertura.objects.all()
    rellenos = Relleno.objects.all()
    sabores = Sabor.objects.all()

    return render(request, 'pastel.html', {
        'coberturas': coberturas,
        'rellenos': rellenos,
        'sabores': sabores
    })


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


def agregar_producto(request):

    with connection.cursor() as cursor:

        if request.method == 'GET':
            tamaño = request.GET.get('pisos', False)
            relleno = request.GET.get('relleno', False)
            cobertura = request.GET.get('cobertura', False)
            sabor = request.GET.get('sabor', False)
            aclaracion = request.GET.get('aclaracion', False)
        else:
            return redirect('pastel')

        cursor.execute(
            f'CALL tomar_precios("{cobertura}", "{relleno}", "{sabor}")')

        columns = []

        for column in cursor.description:

            columns.append(column[0])

        # print(cursor.description)
        data = []

        for row in cursor.fetchall():

            data.append(dict(zip(columns, row)))

        cursor.close()

        connection.commit()
        connection.close()

    # print(int(data[0]['total']))

    total = int(data[0]['total']) * int(tamaño)

    # print(total)

    carrito = Carrito(request)

    producto = {
        'tamaño': tamaño,
        'relleno': relleno,
        'cobertura': cobertura,
        'sabor': sabor,
        'aclaracion': aclaracion,
        'precio_pastel': total
    }

    carrito.agregar(producto)

    # print(total_compra)
    messages.success(
        request, f'Pastel creado con exito')

    return redirect('compras')


def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    carrito.eliminar(producto_id)
    messages.success(
        request, f'Pastel eliminado con exito')
    return redirect('compras')


def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    messages.success(
        request, f'Productos eliminados con exito')
    return redirect('compras')


def historial(request):

    return render(request, 'historial.html')