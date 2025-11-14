# attendance/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Tablet de recepción
    path('checkin/', views.checkin_view, name='checkin'),

    # Registro de visitantes (público)
    path('visitante/registro/', views.VisitanteCreateView.as_view(), name='visitante_registro'),
    path('visitante/exito/', views.visitante_exito, name='visitante_exito'),

    # Dashboard y reportes (requiere autenticación)
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('reporte/mensual/', views.reporte_mensual_view, name='reporte_mensual'),
    path('reporte/mensual/<int:mes>/<int:anio>/', views.reporte_mensual_view, name='reporte_mensual_detalle'),
]

# proyecto/urls.py (principal)
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('attendance.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""