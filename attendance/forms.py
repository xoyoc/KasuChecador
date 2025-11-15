from django import forms
from .models import Visitante, Empleado

class CheckInForm(forms.Form):
    qr_code = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 text-lg border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Escanea tu código QR',
            'autofocus': True,
            'autocomplete': 'off'
        }),
        label=''
    )

class VisitanteForm(forms.ModelForm):
    class Meta:
        model = Visitante
        fields = ['nombre', 'email', 'empresa', 'telefono', 'departamento_visita', 'motivo', 'fecha_visita', 'hora_visita']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Nombre completo'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'correo@ejemplo.com'
            }),
            'empresa': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Nombre de la empresa (opcional)'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': '55-1234-5678'
            }),
            'departamento_visita': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'motivo': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Motivo de la visita',
                'rows': 3
            }),
            'fecha_visita': forms.DateInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'type': 'date'
            }),
            'hora_visita': forms.TimeInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'type': 'time'
            }),
        }
        labels = {
            'nombre': 'Nombre Completo',
            'email': 'Correo Electrónico',
            'empresa': 'Empresa',
            'telefono': 'Teléfono',
            'departamento_visita': 'Departamento a Visitar',
            'motivo': 'Motivo de la Visita',
            'fecha_visita': 'Fecha de Visita',
            'hora_visita': 'Hora de Visita',
        }