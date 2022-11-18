"""PasteleriaFinal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from PasteleriaApp import views
from django.contrib.auth.views import LoginView, logout_then_login
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name=""),
    path('accounts/login/', LoginView.as_view(template_name = 'login.html'), name="login"),
    path('register', views.register, name="register"),
    path('logout', logout_then_login, name="logout"),
    path('compras', login_required(views.compras), name="compras"),
    path('pastel', login_required(views.pastel), name="pastel"),
    path('historial/<int:user_id>', login_required(views.historial), name="historial"),
    path('comprar/<int:user_id>/', login_required(views.comprar), name="comprar"),
    path('agregar_producto', login_required(views.agregar_producto), name="agregar_producto"),
    path('eliminar_producto/<int:producto_id>/', login_required(views.eliminar_producto), name="eliminar_producto"),
    path('limpiar_carrito', login_required(views.limpiar_carrito), name="limpiar_carrito"),
]

urlpatterns += staticfiles_urlpatterns()