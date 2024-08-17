from django.urls import path
from .views import *

urlpatterns = [
    path('getUsuarios/',getUsuarios , name='getUsuarios'),
    path('crearUsuario/',postCrearUsuario , name='postCrearUsuario'),
    path('Login/',iniciar_sesion , name='iniciarsesion'),
]