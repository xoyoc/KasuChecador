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