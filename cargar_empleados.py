import os
import django
import pandas as pd
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'checador.settings')
django.setup()

from django.contrib.auth.models import User
from attendance.models import Empleado, Departamento

def cargar_empleados_desde_csv(archivo_csv):
    """
    Función para cargar empleados desde un archivo CSV al modelo de Django
    """
    # Leer el archivo CSV
    df = pd.read_csv(archivo_csv)

    # Contadores para estadísticas
    empleados_creados = 0
    empleados_actualizados = 0
    errores = []

    # Mapeo de departamentos del CSV a los nombres en la base de datos
    mapeo_departamentos = {
        'Dirección / Gerencia General': 'Dirección / Gerencia General',
        'Operaciones': 'Operaciones',
        'Servicio al Cliente': 'Servicio al Cliente',
        'Administración y Finanzas': 'Administración y Finanzas',
        'Compras y Logística / Cadena de Suministro': 'Compras y Logística',
        'Seguridad': 'Seguridad',
        'Mantenimiento y Taller': 'Mantenimiento y Taller',
        'Servicios Generales': 'Servicios Generales'
    }

    for index, row in df.iterrows():
        try:
            # Obtener datos del CSV
            numero = str(row['No']).strip()
            nombre_completo = str(row['Nombre']).strip()
            puesto = str(row['Puesto']).strip()
            departamento_csv = str(row['Departamento']).strip()

            # Saltar si es VACANTE
            if nombre_completo.upper() == 'VACANTE':
                print(f"Saltando empleado VACANTE - {puesto}")
                continue

            # Buscar o crear el departamento
            departamento_nombre = mapeo_departamentos.get(departamento_csv, departamento_csv)
            departamento, created = Departamento.objects.get_or_create(
                nombre=departamento_nombre,
                defaults={'email': f"{departamento_nombre.lower().replace(' ', '_').replace('/', '_')}@empresa.com"}
            )

            if created:
                print(f"Departamento creado: {departamento.nombre}")

            # Generar código de empleado
            codigo_empleado = f"EMP{numero.zfill(3)}"

            # Crear nombre de usuario (usar primera parte del nombre)
            partes_nombre = nombre_completo.split()
            if len(partes_nombre) >= 2:
                username = f"{partes_nombre[0].lower()}.{partes_nombre[1].lower()}"
            else:
                username = partes_nombre[0].lower()

            # Asegurarse de que el username sea único
            username_base = username
            contador = 1
            while User.objects.filter(username=username).exists():
                username = f"{username_base}{contador}"
                contador += 1

            # Crear email
            email = f"{username}@empresa.com"

            # Verificar si el empleado ya existe
            empleado_existente = Empleado.objects.filter(codigo_empleado=codigo_empleado).first()

            if empleado_existente:
                # Actualizar empleado existente
                empleado_existente.departamento = departamento
                empleado_existente.save()

                # Actualizar usuario
                usuario = empleado_existente.user
                usuario.first_name = ' '.join(partes_nombre[:-1]) if len(partes_nombre) > 1 else partes_nombre[0]
                usuario.last_name = partes_nombre[-1] if len(partes_nombre) > 1 else ''
                usuario.email = email
                usuario.save()

                empleados_actualizados += 1
                print(f"Empleado actualizado: {nombre_completo} - {codigo_empleado}")

            else:
                # Crear nuevo usuario
                usuario = User.objects.create_user(
                    username=username,
                    email=email,
                    password='temp12345',  # Contraseña temporal
                    first_name=' '.join(partes_nombre[:-1]) if len(partes_nombre) > 1 else partes_nombre[0],
                    last_name=partes_nombre[-1] if len(partes_nombre) > 1 else ''
                )

                # Crear empleado
                empleado = Empleado.objects.create(
                    user=usuario,
                    codigo_empleado=codigo_empleado,
                    departamento=departamento,
                    tiempo_extra_habilitado=False,
                    activo=True
                )

                empleados_creados += 1
                print(f"Empleado creado: {nombre_completo} - {codigo_empleado}")

        except Exception as e:
            error_msg = f"Error procesando fila {index + 1}: {nombre_completo} - {str(e)}"
            errores.append(error_msg)
            print(f"ERROR: {error_msg}")
            continue

    # Mostrar resumen
    print("\n" + "="*50)
    print("RESUMEN DE CARGA DE EMPLEADOS")
    print("="*50)
    print(f"Empleados creados: {empleados_creados}")
    print(f"Empleados actualizados: {empleados_actualizados}")
    print(f"Errores: {len(errores)}")

    if errores:
        print("\nErrores encontrados:")
        for error in errores:
            print(f"- {error}")

def crear_departamentos_iniciales():
    """
    Función para crear los departamentos base si no existen
    """
    departamentos_base = [
        {'nombre': 'Dirección / Gerencia General', 'email': 'gerencia_general@empresa.com'},
        {'nombre': 'Operaciones', 'email': 'operaciones@empresa.com'},
        {'nombre': 'Servicio al Cliente', 'email': 'servicio_cliente@empresa.com'},
        {'nombre': 'Administración y Finanzas', 'email': 'administracion@empresa.com'},
        {'nombre': 'Compras y Logística', 'email': 'compras@empresa.com'},
        {'nombre': 'Seguridad', 'email': 'seguridad@empresa.com'},
        {'nombre': 'Mantenimiento y Taller', 'email': 'mantenimiento@empresa.com'},
        {'nombre': 'Servicios Generales', 'email': 'servicios_generales@empresa.com'},
    ]

    for depto in departamentos_base:
        departamento, created = Departamento.objects.get_or_create(
            nombre=depto['nombre'],
            defaults={'email': depto['email']}
        )
        if created:
            print(f"Departamento creado: {departamento.nombre}")

if __name__ == "__main__":
    # Ruta al archivo CSV
    archivo_csv = "Kasu - Empleados.csv"  # Ajusta la ruta si es necesario

    try:
        print("Iniciando carga de empleados...")

        # Primero crear departamentos base
        print("Creando departamentos base...")
        crear_departamentos_iniciales()

        # Luego cargar empleados
        print("Cargando empleados desde CSV...")
        cargar_empleados_desde_csv(archivo_csv)

        print("\n¡Proceso completado!")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {archivo_csv}")
    except Exception as e:
        print(f"Error general: {str(e)}")