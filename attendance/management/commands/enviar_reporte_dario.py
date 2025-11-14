from django.core.management.base import BaseCommand
from django.utils import timezone
from attendance.utils import generar_reporte_diario

class Command(BaseCommand):
    help = 'Envía el reporte diario de asistencia después de las 12:00 PM'

    def handle(self, *args, **options):
        ahora = timezone.now()

        if ahora.hour >= 12:
            self.stdout.write('Generando reporte diario...')
            try:
                generar_reporte_diario()
                self.stdout.write(self.style.SUCCESS('Reporte diario enviado exitosamente'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error al enviar reporte: {e}'))
        else:
            self.stdout.write(self.style.WARNING('Aún no es hora de enviar el reporte (después de las 12:00 PM)'))


# attendance/management/commands/enviar_reporte_quincenal.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from attendance.utils import generar_reporte_quincenal

class Command(BaseCommand):
    help = 'Envía el reporte quincenal (días 13 y 28)'

    def handle(self, *args, **options):
        hoy = timezone.now().date()

        if hoy.day == 13 or hoy.day == 28:
            self.stdout.write(f'Generando reporte quincenal para el día {hoy.day}...')
            try:
                generar_reporte_quincenal(hoy.day)
                self.stdout.write(self.style.SUCCESS('Reporte quincenal enviado exitosamente'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error al enviar reporte: {e}'))
        else:
            self.stdout.write(self.style.WARNING(f'Hoy no es día de reporte quincenal (día {hoy.day})'))


# attendance/management/commands/generar_reporte_tiempo_extra.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from attendance.utils import generar_reporte_tiempo_extra_mensual

class Command(BaseCommand):
    help = 'Genera el reporte mensual de tiempo extra'

    def handle(self, *args, **options):
        self.stdout.write('Generando reporte mensual de tiempo extra...')
        try:
            generar_reporte_tiempo_extra_mensual()
            self.stdout.write(self.style.SUCCESS('Reporte de tiempo extra generado exitosamente'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al generar reporte: {e}'))


"""
CONFIGURACIÓN DE CRON JOBS EN EL SERVIDOR

Para automatizar estos comandos, agrega lo siguiente al crontab:

# Reporte diario a las 12:05 PM todos los días
5 12 * * * cd /ruta/proyecto && /ruta/venv/bin/python manage.py enviar_reporte_diario

# Reporte quincenal los días 13 y 28 a las 6:00 PM
0 18 13,28 * * cd /ruta/proyecto && /ruta/venv/bin/python manage.py enviar_reporte_quincenal

# Reporte mensual de tiempo extra el primer día de cada mes a las 8:00 AM
0 8 1 * * cd /ruta/proyecto && /ruta/venv/bin/python manage.py generar_reporte_tiempo_extra

Ejecutar crontab -e para editar el crontab
"""