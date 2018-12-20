from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.sessions.models import Session

from .models import Modelo

JUSTIFICACION_CHOICES = (
   ('i', 'Izquierda'),
   ('d', 'Derecha'),
   ('c', 'Centro'),
	)

JUSTIFICACION_V_CHOICES = (
   ('s', 'Superior'),
   ('c', 'Centro'),
   ('i', 'Inferior'),
	)

MENU_COLOR_CHOICES = (
   ('primary', 'Primary'),
   ('secondary', 'Secondary'),
   ('success', 'Success'),
   ('danger', 'Danger'),
   ('warning', 'Warning'),
   ('info', 'Info'),
   ('dark', 'Dark'),
   ('light', 'Light'),
   ('white', 'White'),
   ('transparent', 'Transparent'),
	)

class ModeloForm(forms.ModelForm):
	class Meta:
		model = Modelo
		fields = ('nombre', 'descripcion','padre','nombreself','nombreborrar',
			'titulolista','colorfondotitulolista', 'fonttitulolista','colortitulolista',
			'justificaciontitulolista','mayusculastitulolista','bordeinferior',
			'fontcolumnas','colorcolumnas','mayusculascolumnas',
			'fonteditarborrar','coloreditarborrar','textoeditarborrar','colorlinknuevo',
			'textolinknuevo','fontlinknuevo','textotitulopagina',
			'fonttextotitulopagina','colortextotitulopagina',
			'controlesautomaticos','hijoscontiguos','textotitulolistahijos','fonttextotitulolistahijos',
			'colortextolistahijos','colorfondotitulolistahijos','fontcolumnaslistahijos',
			'colorcolumnaslistahijos','mayusculascolumnaslistahijos',
			'textoborrado','textobotonborrado','fonttextoborrado','colortextoborrado',
			'numerocolumnasizquierdaedicion','numerocolumnasderechaedicion',
			'numerocolumnasmodeloedicion', 'numerocolumnashijosedicion',
			'numerocolumnasizquierdanuevo','numerocolumnasderechanuevo',
			'numerocolumnasmodelonuevo', 'altotitulolista','justificacionverticaltitulolista',			
			'fontetiqueta','coloretiqueta', 'justificaciontitulolistahijos','mayusculastitulolistahijos',
			'textoopcionmenu','fondocolumnaslistahijos', 'altotitulolistahijos',
			'justificacionverticaltitulolistahijos','fonttextolista','colortextolista','colorfondotextolista',
			'colorfondocolumnas','altocolumnas','altocolumnaslistahijos','linkboton','colorbotonlinknuevo')
		widgets = {
			'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder': ''}),
			'descripcion': forms.Textarea(attrs={'class':'form-control', 'placeholder': ''}),
			'nombreself' : forms.TextInput(attrs={'class':'form-control', 'placeholder': ''}),
			'nombreborrar' : forms.TextInput(attrs={'class':'form-control', 'placeholder': ''}),
			'padre' : forms.TextInput(attrs={'class':'form-control', 'placeholder': ''}),
			# 'numerodivisiones' : forms.NumberInput(attrs={'class':'form-control'})
			'justificaciontitulolista': forms.Select(choices=JUSTIFICACION_CHOICES),
			'justificacionverticaltitulolista': forms.Select(choices=JUSTIFICACION_V_CHOICES),
			'justificacionverticaltitulolistahijos': forms.Select(choices=JUSTIFICACION_V_CHOICES),
			'justificaciontitulolistahijos': forms.Select(choices=JUSTIFICACION_CHOICES),
			'colorbotonlinknuevo': forms.Select(choices=MENU_COLOR_CHOICES),
		}
		labels = {
			'nombre':'', 'descripcion':'','padre': 'Modelo Padre','nombreself':'Para despliegue','nombreborrar': 'Para borrar'
		}
