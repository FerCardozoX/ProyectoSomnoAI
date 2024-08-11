from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.conf import settings
import uuid
from SomnoAIApp.models import *

# Create your views here.

@csrf_exempt
@api_view(['GET'])
def getUsuarios(request):
    Usuarios = Usuario.objects.all().values()
    return JsonResponse(list(Usuarios), status=200, safe=False)

# Crear un usuario
@csrf_exempt
@api_view(['POST'])
def postCrearUsuario(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    fecha_nacimiento = request.data.get('fecha_nacimiento')
    genero = request.data.get('genero')
    altura = request.data.get('altura')
    peso = request.data.get('peso')
    condiciones_medicas = request.data.get('condiciones_medicas')

    if not all([username, email, password]):
        return JsonResponse({"error": "Campos Vacíos"}, status=400)

    if Usuario.objects.filter(email=email).exists():
        return JsonResponse({"error": "El Usuario ya existe"}, status=400)

    token = uuid.uuid4().hex
    usuario = Usuario(
        username=username,
        email=email,
        password=password,
        fecha_nacimiento=fecha_nacimiento,
        genero=genero,
        altura=altura,
        peso=peso,
        condiciones_medicas=condiciones_medicas,
        token_verificacion=token
    )
    usuario.save()

    verification_link = request.build_absolute_uri(f'/verificar-email/{token}/')
    send_mail(
        'Verifica tu correo electrónico',
        f'Por favor, verifica tu correo electrónico visitando el siguiente enlace: {verification_link}',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )

    return JsonResponse({"message": "Usuario Creado con Éxito. Por favor, verifica tu correo electrónico."}, status=201)

# Editar un usuario
@csrf_exempt
@api_view(['PUT'])
def putEditarUsuario(request, user_id):
    try:
        usuario = Usuario.objects.get(id=user_id)
    except Usuario.DoesNotExist:
        return JsonResponse({"error": "Usuario no encontrado"}, status=404)

    username = request.data.get('username')
    email = request.data.get('email')
    fecha_nacimiento = request.data.get('fecha_nacimiento')
    genero = request.data.get('genero')
    altura = request.data.get('altura')
    peso = request.data.get('peso')
    condiciones_medicas = request.data.get('condiciones_medicas')

    if not username:
        return JsonResponse({"error": "Campo 'username' es requerido"}, status=400)

    usuario.username = username
    usuario.email = email
    usuario.fecha_nacimiento = fecha_nacimiento
    usuario.genero = genero
    usuario.altura = altura
    usuario.peso = peso
    usuario.condiciones_medicas = condiciones_medicas
    usuario.save()

    return JsonResponse({"message": "Usuario Actualizado con Éxito"}, status=200)

# Eliminar un usuario
@csrf_exempt
@api_view(['DELETE'])
def deleteEliminarUsuario(request, user_id):
    try:
        usuario = Usuario.objects.get(id=user_id)
    except Usuario.DoesNotExist:
        return JsonResponse({"error": "Usuario no encontrado"}, status=404)

    usuario.delete()

    return JsonResponse({"message": "Usuario Eliminado con Éxito"}, status=204)

# Listar todos los usuarios
@csrf_exempt
@api_view(['GET'])
def getListarUsuarios(request):
    usuarios = Usuario.objects.all().values()
    return JsonResponse({"usuarios": list(usuarios)}, safe=False, status=200)

# Verificar el correo electrónico
@csrf_exempt
@api_view(['GET'])
def getVerificarEmail(request, token):
    try:
        usuario = Usuario.objects.get(token_verificacion=token)
        usuario.email_verificado = True
        usuario.token_verificacion = ''
        usuario.save()
        return JsonResponse({"message": "Correo electrónico verificado exitosamente."}, status=200)
    except Usuario.DoesNotExist:
        return JsonResponse({"error": "Token de verificación inválido."}, status=400)
