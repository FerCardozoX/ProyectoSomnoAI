import datetime
from datetime import datetime, timedelta
from django.utils import timezone
import json
from random import randint, uniform
import uuid
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.conf import settings
from SomnoAIApp.models import Usuarios, Observaciones, Estadisticas, Informes
from config.gmail_service import send_email
import google.generativeai as genai
from .IA.Testeo import main as ejecutar_testeo
from .IA.TesteoAudio import main as ejecutar_audio

# Obtener todos los usuarios
@csrf_exempt
@api_view(['GET'])
def getUsuarios(request):
    usuarios = Usuarios.objects.all().values()
    return JsonResponse(list(usuarios), status=200, safe=False)

# Obtener un usuario por usuario_id
@csrf_exempt
@api_view(['GET'])
def get_usuario(request, usuario_id):
    usuario = Usuarios.objects.filter(usuario_id=usuario_id).values()
    return JsonResponse(list(usuario), status=200, safe=False)

# Crear un usuario
@csrf_exempt
@api_view(['POST'])
def postCrearUsuario(request):
    nombre = request.data.get('nombre')
    apellido = request.data.get('apellido')
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    fecha_nacimiento = request.data.get('fecha_nacimiento')
    genero = request.data.get('genero') 
    altura = request.data.get('altura')
    peso = request.data.get('peso')
    obra_social = request.data.get('obra_social')

    if not all([username, email, password, nombre, apellido, fecha_nacimiento, genero, altura, peso]):
        return JsonResponse({"error": "Campos vacíos"}, status=400)

    if Usuarios.objects.filter(email=email).exists():
        return JsonResponse({"error": "El usuario ya existe"}, status=400)

    usuario = Usuarios(
        nombre=nombre,
        apellido=apellido,
        username=username,
        email=email,
        password=password,
        fecha_nacimiento=fecha_nacimiento,
        genero=genero,
        altura=altura,
        peso=peso,
        obra_social=obra_social
    )
    usuario.save()

    return JsonResponse({"message": "Usuario creado con éxito. Por favor, verifica tu correo electrónico."}, status=201)

# Editar un usuario
@csrf_exempt
@api_view(['PUT'])
def putEditarUsuario(request, usuario_id):
    try:
        usuario = Usuarios.objects.get(usuario_id=usuario_id)
    except Usuarios.DoesNotExist:
        return JsonResponse({"error": "Usuario no encontrado"}, status=404)

    usuario.username = request.data.get('username', usuario.username)
    usuario.email = request.data.get('email', usuario.email)
    usuario.fecha_nacimiento = request.data.get('fecha_nacimiento', usuario.fecha_nacimiento)
    usuario.genero = request.data.get('genero', usuario.genero)
    usuario.altura = request.data.get('altura', usuario.altura)
    usuario.peso = request.data.get('peso', usuario.peso)
    usuario.obra_social = request.data.get('obra_social', usuario.obra_social)
    usuario.save()

    return JsonResponse({"message": "Usuario actualizado con éxito"}, status=200)

# Eliminar un usuario
@csrf_exempt
@api_view(['DELETE'])
def deleteEliminarUsuario(request, usuario_id):
    try:
        usuario = Usuarios.objects.get(usuario_id=usuario_id)
    except Usuarios.DoesNotExist:
        return JsonResponse({"error": "Usuario no encontrado"}, status=404)

    usuario.delete()

    return JsonResponse({"message": "Usuario eliminado con éxito"}, status=204)

# Iniciar sesión
@csrf_exempt
@api_view(['POST'])
def iniciar_sesion(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not all([username, password]):
        return JsonResponse({"error": "Username y contraseña son requeridos."}, status=400)

    try:
        usuario = Usuarios.objects.get(username=username)
        if usuario.verificar_password(password):
            return JsonResponse({"message": "Inicio de sesión exitoso."}, status=200)
        else:
            return JsonResponse({"error": "Username o contraseña incorrectos."}, status=401)
    except Usuarios.DoesNotExist:
        return JsonResponse({"error": "Usuario no encontrado."}, status=404)

# Generación de respuestas con Gemini
genai.configure(api_key="your_api_key")

@csrf_exempt
def gemini_chat(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        question = data.get('question')
        
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(question)
            respuesta = response.text
            return JsonResponse({'answer': respuesta})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

# Predecir datos
@csrf_exempt
@api_view(['POST'])
def predecir(request):
    try:
        resultados = ejecutar_testeo()
        return JsonResponse(resultados, status=200)
    except Exception as e:
        return JsonResponse({"error": f"Ocurrió un error al ejecutar el procesamiento: {str(e)}"}, status=500)

@csrf_exempt
@api_view(['POST'])
def predecirAudio(request):
    try:
        ResultadoAudio = ejecutar_audio()
        return JsonResponse(ResultadoAudio, status=200)
    except Exception as e:
        return JsonResponse({"error": f"Ocurrió un error al ejecutar el procesamiento: {str(e)}"}, status=500)

# Obtener y crear estadísticas
@csrf_exempt
@api_view(['GET'])
def get_estadisticas(request, usuario_id):
    estadisticas = Estadisticas.objects.filter(usuario_id=usuario_id).values()
    return JsonResponse(list(estadisticas), status=200, safe=False)

@csrf_exempt
@api_view(['POST'])
def post_estadisticas(request):
    usuario_id = request.data.get('usuario_id')
    frecuencia_cardiaca = request.data.get('frecuencia_cardiaca')
    saturacion_oxigeno = request.data.get('saturacion_oxigeno')
    movimientos = request.data.get('movimientos')
    ronquidos = request.data.get('ronquidos')
    respiracion = request.data.get('respiracion')
    presion_arterial = request.data.get('presion_arterial')
    apneas = request.data.get('apneas')
    
    if not usuario_id:
        return JsonResponse({"error": "Usuario ID es requerido"}, status=400)

    Estadisticas.objects.create(
        usuario_id=usuario_id,
        frecuencia_cardiaca=frecuencia_cardiaca,
        saturacion_oxigeno=saturacion_oxigeno,
        movimientos=movimientos,
        ronquidos=ronquidos,
        respiracion=respiracion,
        presion_arterial=presion_arterial,
        apneas=apneas
    )
    return JsonResponse({"message": "Estadística creada con éxito"}, status=201)


@csrf_exempt
@api_view(['POST'])
def registrar_sueno(request):
    usuario_id = request.data.get('usuario_id')
    frecuencia_cardiaca = request.data.get('frecuencia_cardiaca')
    saturacion_oxigeno = request.data.get('saturacion_oxigeno')
    movimientos = request.data.get('movimientos')
    ronquidos = request.data.get('ronquidos')
    respiracion = request.data.get('respiracion')
    presion_arterial = request.data.get('presion_arterial')

    Estadisticas.objects.create(
        usuario_id=usuario_id,
        frecuencia_cardiaca=frecuencia_cardiaca,
        saturacion_oxigeno=saturacion_oxigeno,
        movimientos=movimientos,
        ronquidos=ronquidos,
        respiracion=respiracion,
        presion_arterial=presion_arterial,
    )

    return JsonResponse({"message": "Datos de sueño registrados exitosamente"}, status=201)

@csrf_exempt
@api_view(['POST'])
def CargarBase(request):
    usuarios = Usuarios.objects.all()
    
    # Rango de fechas del 21 al 31 de octubre
    for usuario in usuarios:
        for dia in range(21, 32):  # Días del 21 al 31 de octubre
            fecha_noche = datetime(2024, 10, dia)
            tiene_apnea = usuario.usuario_id in [4, 2]  # Identificar si el usuario tiene apnea

            # Crear un informe diario
            informe = Informes.objects.create(
                usuario=usuario,
                fecha=fecha_noche.date(),
                contenido_informe="Apnea detectada" if tiene_apnea else "Sueño dentro de parámetros normales con pequeñas mejoras sugeridas."
            )

            # Crear exactamente 5 mediciones en intervalos dentro de la noche
            horas_medicion = [22, 23, 0, 1, 2]  # Horas fijas para cada medición
            for hora in horas_medicion:
                hora_medicion = fecha_noche.replace(hour=hora, minute=0)
                frecuencia_cardiaca = randint(80, 110) if tiene_apnea else randint(60, 90)
                saturacion_oxigeno = randint(85, 95) if tiene_apnea else randint(95, 100)
                movimientos = randint(10, 30) if tiene_apnea else randint(5, 15)
                respiracion = uniform(12.0, 20.0) if not tiene_apnea else uniform(10.0, 14.0)
                presion_arterial = randint(140, 160) if tiene_apnea else randint(110, 130)

                # Crear el registro en Estadísticas
                Estadisticas.objects.create(
                    usuario=usuario,
                    fecha=hora_medicion,
                    frecuencia_cardiaca=frecuencia_cardiaca,
                    saturacion_oxigeno=saturacion_oxigeno,
                    movimientos=movimientos,
                    respiracion=respiracion,
                    presion_arterial=presion_arterial
                )

    return JsonResponse({'status': 'Datos generados correctamente'})