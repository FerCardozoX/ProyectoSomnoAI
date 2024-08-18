from django.urls import path
from .views import *

urlpatterns = [
    path('getUsuarios/',getUsuarios , name='getUsuarios'),
    path('crearUsuario/',postCrearUsuario , name='postCrearUsuario'),
    path('Login/',iniciar_sesion , name='iniciarsesion'),
    path('enviarCodigoVerificacion/', enviarCodigoVerificacion, name='enviar_codigo_verificacion'),
    path('verificarCodigoYCrearUsuario/', verificarCodigoYCrearUsuario, name='verificar_codigo_y_crear_usuario'),
]