# Sistema de Control de Asistencia - Django 5.2
## Guía Completa de Instalación y Configuración

### 📋 Requisitos Previos

- Python 3.11+
- PostgreSQL 14+ (o SQLite para desarrollo)
- Redis (para Celery)
- Git

### 🚀 Instalación Paso a Paso

#### 1. Clonar o crear el proyecto

```bash
# Crear directorio del proyecto
mkdir asistencia_proyecto
cd asistencia_proyecto

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

#### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

#### 3. Crear el proyecto Django

```bash
# Si es nuevo proyecto
django-admin startproject proyecto .
python manage.py startapp attendance

# Si ya existe, solo crear la app
python manage.py startapp attendance
```

#### 4. Configurar Base de Datos

**PostgreSQL (Recomendado para producción):**

```bash
# Crear base de datos
sudo -u postgres psql
CREATE DATABASE asistencia_db;
CREATE USER asistencia_user WITH PASSWORD 'tu_password_seguro';
GRANT ALL PRIVILEGES ON DATABASE asistencia_db TO asistencia_user;
\q
```

**En settings.py:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'asistencia_db',
        'USER': 'asistencia_user',
        'PASSWORD': 'tu_password_seguro',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

#### 5. Configurar Email

**Gmail (ejemplo):**

1. Ir a tu cuenta de Google → Seguridad
2. Activar verificación en 2 pasos
3. Crear una contraseña de aplicación
4. Actualizar en settings.py:

```python
EMAIL_HOST_USER = 'tu-email@gmail.com'
EMAIL_HOST_PASSWORD = 'tu_app_password_generado'
DEFAULT_FROM_EMAIL = 'tu-email@gmail.com'
```

#### 6. Ejecutar Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 7. Crear Superusuario

```bash
python manage.py createsuperuser
```

#### 8. Configurar Datos Iniciales

```bash
python manage.py shell
```

```python
from attendance.models import Departamento, ConfiguracionSistema

# Crear departamentos
Departamento.objects.create(nombre="Recursos Humanos", email="rh@empresa.com")
Departamento.objects.create(nombre="Ventas", email="ventas@empresa.com")
Departamento.objects.create(nombre="Tecnología", email="ti@empresa.com")

# Configurar sistema
ConfiguracionSistema.objects.create(
    hora_entrada="09:00:00",
    minutos_tolerancia=15,
    email_gerente="gerente@empresa.com",
    ruta_red_reportes="/ruta/a/tu/unidad/red/reportes"
)
```

#### 9. Crear Empleados

Desde el admin de Django (http://localhost:8000/admin):

1. Crear usuarios en Auth → Users
2. Crear empleados en Attendance → Empleados
3. Asignar usuario, código de empleado y departamento
4. El código QR se genera automáticamente

### 🔧 Configuración de Tareas Programadas

#### Opción A: Celery (Recomendado)

```bash
# Instalar Redis
sudo apt-get install redis-server
sudo systemctl start redis

# En una terminal, iniciar el worker
celery -A proyecto worker -l info

# En otra terminal, iniciar el beat scheduler
celery -A proyecto beat -l info

# O ambos en uno (desarrollo)
celery -A proyecto worker -B -l info
```

#### Opción B: Cron Jobs

```bash
crontab -e
```

Agregar:
```cron
# Reporte diario a las 12:05 PM
5 12 * * * cd /ruta/proyecto && /ruta/venv/bin/python manage.py enviar_reporte_diario

# Reporte quincenal días 13 y 28 a las 6:00 PM
0 18 13,28 * * cd /ruta/proyecto && /ruta/venv/bin/python manage.py enviar_reporte_quincenal

# Reporte tiempo extra primer día del mes a las 8:00 AM
0 8 1 * * cd /ruta/proyecto && /ruta/venv/bin/python manage.py generar_reporte_tiempo_extra
```

### 🖥️ Ejecutar el Servidor

```bash
# Desarrollo
python manage.py runserver 0.0.0.0:8000

# Colectar archivos estáticos
python manage.py collectstatic
```

### 📱 Configuración de la Tablet

1. Acceder a: `http://ip-servidor:8000/checkin/`
2. Configurar el navegador en modo kiosko/fullscreen
3. Conectar lector QR USB o usar cámara web
4. El campo QR tiene auto-focus para facilitar el escaneo

### 🌐 URLs del Sistema

- **Tablet Check-in:** `/checkin/`
- **Formulario Visitantes:** `/visitante/registro/`
- **Dashboard Gerencia:** `/dashboard/`
- **Reportes Mensuales:** `/reporte/mensual/`
- **Admin Django:** `/admin/`

### 📊 Estructura de Archivos

```
proyecto/
├── manage.py
├── requirements.txt
├── proyecto/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py
│   └── wsgi.py
├── attendance/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   ├── utils.py
│   ├── tasks.py
│   ├── management/
│   │   └── commands/
│   │       ├── enviar_reporte_diario.py
│   │       ├── enviar_reporte_quincenal.py
│   │       └── generar_reporte_tiempo_extra.py
│   └── templates/
│       └── attendance/
│           ├── checkin.html
│           ├── visitante_form.html
│           ├── visitante_exito.html
│           ├── dashboard.html
│           └── reporte_mensual.html
└── media/
    ├── qr_codes/
    └── qr_visitantes/
```

### 🔐 Seguridad en Producción

```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['tu-dominio.com', 'www.tu-dominio.com', 'ip-servidor']
CSRF_TRUSTED_ORIGINS = ['https://tu-dominio.com']

# Usar variables de entorno
from decouple import config
SECRET_KEY = config('SECRET_KEY')
EMAIL_HOST_PASSWORD = config('EMAIL_PASSWORD')
```

### 📝 Notas Importantes

1. **Códigos QR:** Se generan automáticamente al crear empleados y visitantes
2. **Tolerancia:** Configurada en 15 minutos desde la hora de entrada
3. **Reportes:** Se envían automáticamente según configuración
4. **Tiempo Extra:** Debe habilitarse por empleado en el admin
5. **Ruta de Red:** Configurar una ruta accesible para guardar reportes mensuales

### 🐛 Troubleshooting

**Error al generar QR:**
```bash
pip install --upgrade Pillow qrcode
```

**Error de permisos en ruta de red:**
```bash
# Verificar permisos de escritura
touch /ruta/red/reportes/test.txt
```

**Celery no ejecuta tareas:**
```bash
# Verificar Redis
redis-cli ping
# Debe responder PONG

# Reiniciar servicios
celery -A proyecto purge
celery -A proyecto worker -B -l info
```

### 📞 Soporte

Para dudas o problemas:
1. Revisar logs de Django
2. Verificar configuración de email
3. Comprobar conexión a base de datos
4. Validar permisos de archivos

### 🎯 Funcionalidades Implementadas

✅ Check-in/out en tablet con QR
✅ Entrada y salida de comida
✅ Tolerancia de 15 minutos
✅ Registro de visitantes con QR
✅ Reporte diario automático (12:00 PM)
✅ Reportes quincenales (días 13 y 28)
✅ Control de tiempo extra
✅ Reporte mensual en red
✅ Dashboard con estadísticas
✅ Detección de retardos consecutivos
✅ Todos los templates con Tailwind CSS