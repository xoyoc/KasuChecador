# create_departamentos.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tu_proyecto.settings')
django.setup()

from attendance.models import Departamento

departamentos_data = [
    {"nombre": "Dirección / Gerencia General", "email": "gerencia@empresa.com"},
    {"nombre": "Operaciones", "email": "operaciones@empresa.com"},
    {"nombre": "Servicio al Cliente", "email": "servicio.cliente@empresa.com"},
    {"nombre": "Administración y Finanzas", "email": "administracion@empresa.com"},
    {"nombre": "Compras y Logística / Cadena de Suministro", "email": "compras.logistica@empresa.com"},
    {"nombre": "Mantenimiento y Taller", "email": "mantenimiento@empresa.com"},
    {"nombre": "Seguridad", "email": "seguridad@empresa.com"},
    {"nombre": "Servicios Generales", "email": "servicios.generales@empresa.com"},
]

for dept_data in departamentos_data:
    departamento, created = Departamento.objects.get_or_create(
        nombre=dept_data["nombre"],
        defaults={"email": dept_data["email"]}
    )
    if created:
        print(f"Departamento creado: {departamento.nombre}")
    else:
        print(f"Departamento ya existía: {departamento.nombre}")