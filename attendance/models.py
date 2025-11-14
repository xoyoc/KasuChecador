from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
import qrcode
from io import BytesIO
from django.core.files import File
import uuid

class Departamento(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Departamentos"

class Empleado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    codigo_empleado = models.CharField(max_length=20, unique=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)
    qr_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tiempo_extra_habilitado = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.codigo_empleado}"

    def generar_qr(self):
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(str(self.qr_uuid))
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer, format='PNG')
        filename = f'qr_{self.codigo_empleado}.png'
        self.qr_code.save(filename, File(buffer), save=False)
        buffer.close()

    def save(self, *args, **kwargs):
        if not self.qr_code:
            self.generar_qr()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Empleados"

class TipoMovimiento(models.TextChoices):
    ENTRADA = 'ENTRADA', 'Entrada'
    SALIDA_COMIDA = 'SALIDA_COMIDA', 'Salida a Comida'
    ENTRADA_COMIDA = 'ENTRADA_COMIDA', 'Entrada de Comida'
    SALIDA = 'SALIDA', 'Salida'

class Asistencia(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)
    hora = models.TimeField(auto_now_add=True)
    tipo_movimiento = models.CharField(max_length=20, choices=TipoMovimiento.choices)
    retardo = models.BooleanField(default=False)
    minutos_retardo = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.empleado.user.get_full_name()} - {self.tipo_movimiento} - {self.fecha}"

    def calcular_retardo(self, hora_entrada_esperada="09:00:00"):
        """Calcula si hay retardo considerando 15 minutos de tolerancia"""
        if self.tipo_movimiento == TipoMovimiento.ENTRADA:
            hora_esperada = datetime.strptime(hora_entrada_esperada, "%H:%M:%S").time()
            tolerancia = timedelta(minutes=15)
            hora_limite = (datetime.combine(datetime.today(), hora_esperada) + tolerancia).time()

            if self.hora > hora_limite:
                self.retardo = True
                hora_esperada_dt = datetime.combine(datetime.today(), hora_esperada)
                hora_real_dt = datetime.combine(datetime.today(), self.hora)
                diferencia = hora_real_dt - hora_esperada_dt
                self.minutos_retardo = int(diferencia.total_seconds() / 60)
            else:
                self.retardo = False
                self.minutos_retardo = 0

    class Meta:
        verbose_name_plural = "Asistencias"
        ordering = ['-fecha', '-hora']

class TiempoExtra(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha = models.DateField()
    horas_extra = models.DecimalField(max_digits=5, decimal_places=2)
    descripcion = models.TextField(blank=True)
    aprobado = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.empleado.user.get_full_name()} - {self.fecha} - {self.horas_extra}hrs"

    class Meta:
        verbose_name_plural = "Tiempos Extra"
        ordering = ['-fecha']

class Visitante(models.Model):
    nombre = models.CharField(max_length=200)
    email = models.EmailField()
    empresa = models.CharField(max_length=200, blank=True)
    telefono = models.CharField(max_length=20)
    departamento_visita = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    motivo = models.TextField()
    fecha_visita = models.DateField()
    hora_visita = models.TimeField()
    qr_code = models.ImageField(upload_to='qr_visitantes/', blank=True)
    qr_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    confirmado = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.departamento_visita} - {self.fecha_visita}"

    def generar_qr(self):
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(f"VISITANTE:{str(self.qr_uuid)}")
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer, format='PNG')
        filename = f'qr_visitante_{self.id}.png'
        self.qr_code.save(filename, File(buffer), save=False)
        buffer.close()

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and not self.qr_code:
            self.generar_qr()
            super().save(update_fields=['qr_code'])

    class Meta:
        verbose_name_plural = "Visitantes"

class RegistroVisita(models.Model):
    visitante = models.ForeignKey(Visitante, on_delete=models.CASCADE)
    hora_entrada = models.DateTimeField(auto_now_add=True)
    hora_salida = models.DateTimeField(null=True, blank=True)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"{self.visitante.nombre} - {self.hora_entrada}"

    class Meta:
        verbose_name_plural = "Registros de Visitas"
        ordering = ['-hora_entrada']

class ConfiguracionSistema(models.Model):
    hora_entrada = models.TimeField(default="09:00:00")
    minutos_tolerancia = models.IntegerField(default=15)
    email_gerente = models.EmailField()
    ruta_red_reportes = models.CharField(max_length=500, help_text="Ruta de red para guardar reportes mensuales")

    def __str__(self):
        return "Configuración del Sistema"

    class Meta:
        verbose_name_plural = "Configuración del Sistema"