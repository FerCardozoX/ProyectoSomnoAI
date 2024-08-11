from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.conf import settings
import uuid
from SomnoAIApp.models import Usuario

# Obtener todos los usuarios
@csrf_exempt
@api_view(['GET'])
def getUsuarios(request):
    usuarios = Usuario.objects.all().values()
    return JsonResponse(list(usuarios), status=200, safe=False)

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
        return JsonResponse({"error": "Campos vacíos"}, status=400)

    if Usuario.objects.filter(email=email).exists():
        return JsonResponse({"error": "El usuario ya existe"}, status=400)

    token = uuid.uuid4().hex
    usuario = Usuario(
        username=username,
        email=email,
        password=password,
        fecha_nacimiento=fecha_nacimiento,
        genero=genero,
        altura=altura,
        peso=peso,
        condiciones_medicas=condiciones_medicas
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

    return JsonResponse({"message": "Usuario creado con éxito. Por favor, verifica tu correo electrónico."}, status=201)

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

    return JsonResponse({"message": "Usuario actualizado con éxito"}, status=200)

# Eliminar un usuario
@csrf_exempt
@api_view(['DELETE'])
def deleteEliminarUsuario(request, user_id):
    try:
        usuario = Usuario.objects.get(id=user_id)
    except Usuario.DoesNotExist:
        return JsonResponse({"error": "Usuario no encontrado"}, status=404)

    usuario.delete()

    return JsonResponse({"message": "Usuario eliminado con éxito"}, status=204)

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

# Iniciar sesión
@csrf_exempt
@api_view(['POST'])
def iniciar_sesion(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not all([email, password]):
        return JsonResponse({"error": "Correo electrónico y contraseña son requeridos."}, status=400)

    try:
        usuario = Usuario.objects.get(email=email)
        if usuario.verificar_password(password):
            # Aquí puedes manejar la sesión si usas Django con sesiones.
            return JsonResponse({"message": "Inicio de sesión exitoso."}, status=200)
        else:
            return JsonResponse({"error": "Correo electrónico o contraseña incorrectos."}, status=401)
    except Usuario.DoesNotExist:
        return JsonResponse({"error": "Usuario no encontrado."}, status=404)

# Solicitar cambio de contraseña
@csrf_exempt
@api_view(['POST'])
def solicitar_cambio_contraseña(request):
    email = request.data.get('email')

    if not email:
        return JsonResponse({"error": "Correo electrónico requerido."}, status=400)

    try:
        usuario = Usuario.objects.get(email=email)
    except Usuario.DoesNotExist:
        return JsonResponse({"error": "Usuario no encontrado."}, status=404)

    token = default_token_generator.make_token(usuario)
    uid = urlsafe_base64_encode(force_bytes(usuario.pk))

    # Enviar correo electrónico con el token
    send_mail(
        'Restablecimiento de contraseña',
        f'Usa este token para restablecer tu contraseña: {token}',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )

    return JsonResponse({"message": "Correo enviado con éxito.", "uid": uid, "token": token}, status=200)

# Verificar token
@csrf_exempt
@api_view(['POST'])
def verificar_token(request):
    uidb64 = request.data.get('uid')
    token = request.data.get('token')

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        usuario = Usuario.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
        return JsonResponse({"error": "Token inválido o usuario no encontrado."}, status=400)

    if default_token_generator.check_token(usuario, token):
        return JsonResponse({"message": "Token válido."}, status=200)
    else:
        return JsonResponse({"error": "Token inválido."}, status=400)

# Cambiar contraseña
@csrf_exempt
@api_view(['POST'])
def cambiar_contraseña(request):
    uidb64 = request.data.get('uid')
    token = request.data.get('token')
    nueva_contraseña = request.data.get('nueva_contraseña')

    if not nueva_contraseña:
        return JsonResponse({"error": "Nueva contraseña requerida."}, status=400)

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        usuario = Usuario.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
        return JsonResponse({"error": "Usuario no encontrado."}, status=404)

    if default_token_generator.check_token(usuario, token):
        usuario.set_password(nueva_contraseña)
        usuario.save()
        return JsonResponse({"message": "Contraseña actualizada con éxito."}, status=200)
    else:
        return JsonResponse({"error": "Token inválido."}, status=400)
