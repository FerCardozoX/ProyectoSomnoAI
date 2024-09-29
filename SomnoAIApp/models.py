from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Modelo de Usuario
class Usuario(models.Model):
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(
        max_length=10,
        choices=[('M', 'Masculino'), ('F', 'Femenino')],
        null=True,
        blank=True
    )
    altura = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # En metros
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # En kilogramos
    obra_social = models.TextField(null=True, blank=True)
    email_verificado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = make_password(self.password)
        super(Usuario, self).save(*args, **kwargs)

    def verificar_password(self, password):
        return check_password(password, self.password)

    def calcular_imc(self):
        if self.altura and self.peso:
            return self.peso / (self.altura ** 2)
        return None

# Modelo de Sueño
class Sueno(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateField()
    horas_dormidas = models.DecimalField(max_digits=4, decimal_places=2)
    calidad_sueno = models.IntegerField()  # Valoración del 1 al 10
    movimientos_dormir = models.IntegerField()  # Cantidad de movimientos registrados
    pulsaciones_promedio = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    apneas = models.IntegerField(null=True, blank=True)

# Modelo de Estadística
class Estadistica(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateField()
    promedio_calidad_sueno = models.DecimalField(max_digits=4, decimal_places=2)
    promedio_horas_dormidas = models.DecimalField(max_digits=4, decimal_places=2)
    promedio_apneas = models.DecimalField(max_digits=5, decimal_places=2)
    promedio_movimientos_dormir = models.DecimalField(max_digits=5, decimal_places=2)

# Modelo de Contacto
class Contacto(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    centro_salud = models.CharField(max_length=255)
    fecha_contacto = models.DateField()
    mensaje = models.TextField()

# Modelo de Centro de Salud
class CentroSalud(models.Model):
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)

# Modelo de Perfil
class Perfil(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    foto_perfil = models.ImageField(upload_to='perfiles/', null=True, blank=True)

# Historial del Chat
class HistorialChat(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pregunta = models.TextField()  # Pregunta hecha por el usuario
    respuesta = models.TextField()  # Respuesta de Gemini
    fecha = models.DateTimeField(auto_now_add=True)