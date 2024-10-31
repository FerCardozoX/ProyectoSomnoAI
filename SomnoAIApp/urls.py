from django.urls import path
from .views import *

urlpatterns = [
    path('getUsuarios/',getUsuarios , name='getUsuarios'),
    path('crearUsuario/',postCrearUsuario , name='postCrearUsuario'),
    path('Login/',iniciar_sesion , name='iniciarsesion'),
    path('geminiChat/',gemini_chat, name='gemini_chat'),
    path('predecirApnea/', predecir, name='predecir_apnea'),
    path('predecirAudio/', predecirAudio, name='predecir_audio'),
    path('CargarBase/', CargarBase, name='CargarBase'),
]