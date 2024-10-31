from django.urls import path
from .views import *

urlpatterns = [
    path('getUsuarios/',getUsuarios , name='getUsuarios'),
    path('get_usuario/<int:usuario_id>/', get_usuario, name='get_usuario'),
    path('crearUsuario/',postCrearUsuario , name='postCrearUsuario'),
    path('Login/',iniciar_sesion , name='iniciarsesion'),
    path('geminiChat/',gemini_chat, name='gemini_chat'),
    path('predecirApnea/', predecir, name='predecir_apnea'),
    path('predecirAudio/', predecirAudio, name='predecir_audio'),
    path('editarUsuario/<int:usuario_id>/', putEditarUsuario, name='editar_usuario'),
    path('eliminarUsuario/<int:usuario_id>/', deleteEliminarUsuario, name='eliminar_usuario'),
    path('getEstadisticas/<int:usuario_id>/', get_estadisticas, name='get_estadisticas'),
    path('crearEstadistica/', post_estadisticas, name='crear_estadistica'),

]