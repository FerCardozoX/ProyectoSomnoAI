from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Modelo de Usuario
class Usuarios(models.Model):
    usuario_id = models.AutoField(primary_key=True)  # Campo incremental y único
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
        super(Usuarios, self).save(*args, **kwargs)

    def verificar_password(self, password):
        return check_password(password, self.password)

    def calcular_imc(self):
        if self.altura and self.peso:
            return self.peso / (self.altura ** 2)
        return None

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.username})"


# Modelo de Estadisticas
class Estadisticas(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, to_field='usuario_id')
    fecha = models.DateField(auto_now_add=True)
    frecuencia_cardiaca = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    saturacion_oxigeno = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    movimientos = models.IntegerField(null=True, blank=True)
    ronquidos = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    respiracion = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    presion_arterial = models.CharField(max_length=15, null=True, blank=True)

    class Meta:
        verbose_name = "Estadística"
        verbose_name_plural = "Estadísticas"

    def __str__(self):
        return f"Estadísticas del {self.fecha} para {self.usuario.username}"


# Modelo de Observaciones
class Observaciones(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, to_field='usuario_id')
    fecha = models.DateField(auto_now_add=True)
    puntaje_sueno = models.DecimalField(max_digits=5, decimal_places=2)  # Puntaje de sueño
    observacion = models.TextField()
    apnea_porcentaje = models.IntegerField(null=True, blank=True)
    resultado_apnea = models.CharField(max_length=255, null=True, blank=True)  # "Positivo para apnea del sueño" o "Negativo"
    promedio_oxigeno = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    evaluacion_oxigeno = models.CharField(max_length=255, null=True, blank=True)  
    promedio_heart_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    evaluacion_heart_rate = models.CharField(max_length=255, null=True, blank=True)  
    promedio_breathing = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    evaluacion_breathing = models.CharField(max_length=255, null=True, blank=True)  #

    class Meta:
        verbose_name = "Observación"
        verbose_name_plural = "Observaciones"

    def __str__(self):
        return f"Observación del {self.fecha} para {self.usuario.username}"


# Modelo de Informe
class Informes(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, to_field='usuario_id')
    fecha = models.DateField(auto_now_add=True)
    contenido_informe = models.TextField()

    class Meta:
        verbose_name = "Informe"
        verbose_name_plural = "Informes"

    def __str__(self):
        return f"Informe del {self.fecha} para {self.usuario.username}"
