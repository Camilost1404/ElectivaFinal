from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegisterForm
from django.contrib import messages
from PasteleriaApp.models import Cobertura, Relleno, Sabor
from PasteleriaApp.carrito import Carrito
from django.db import connection
from datetime import date

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
                request, f'Usuario {username} creado con éxito')
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
        request, f'Pastel creado con éxito')

    return redirect('compras')


def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    carrito.eliminar(producto_id)
    messages.success(
        request, f'Pastel eliminado con éxito')
    return redirect('compras')


def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    messages.success(
        request, f'Productos eliminados con éxito')
    return redirect('compras')


def historial(request, user_id):

    with connection.cursor() as cursor:

        cursor.execute(
            f'CALL traer_pedidos({user_id})')

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

    return render(request, 'historial.html', {'data': data})


def comprar(request, user_id):

    with connection.cursor() as cursor:
        carrito = Carrito(request)

        if request.method == 'GET':
            tipo_entrega = request.GET['tipo_entrega']
        else:
            return redirect('pastel')

        total = float(carrito.session['total'])
        user = user_id
        fecha = date.today()

        cursor.execute(
            f'CALL pedido("{fecha}", "{tipo_entrega}", {total}, {user})')

        for key, value in carrito.session['carrito'].items():
            tamaño = int(value['tamaño'])
            aclaracion = value['aclaracion']
            cobertura = value['cobertura']
            sabor = value['sabor']
            relleno = value['relleno']
            precio = float(value['precio_pastel'])

            # print(type(value['tamaño']))
            cursor.execute(
                f'CALL guardar_producto({tamaño}, "{aclaracion}", "{cobertura}", "{relleno}", "{sabor}")')
            cursor.execute(f'CALL detalle_pedido({precio})')

        cursor.close()

        connection.commit()
        connection.close()

    messages.success(
        request, f'Compra realizada con éxito')
    carrito.limpiar()

    return redirect('compras')
