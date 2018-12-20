from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Proyecto
from django.core.exceptions import ValidationError
import urllib.request

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

class ProyectoForm(forms.ModelForm):

	class Meta:
		model = Proyecto
		fields = ('nombre','descripcion','autor','directorio' ,'avatar','altopixeles','anchopixeles',
			'numerocolumnas','justificacion',
			'justificaciontitulo','numerocolumnastitulo','textotitulo','fonttitulo','colortitulo',
			'colorfondomenu','fontmenu','colormenu','mayusculas','altomenu',
			'numerocolumnasizquierda','numerocolumnasderecha','numerocolumnascentro',
			'numerodivisionespie','columnasdivision','columnasizquierdaencabezado',
			'columnasderechaencabezado',
			'listafontsgoogle','textoopcioninicio','colorfondoencabezado','altoencabezado',
			'justificacionverticallogo', 'justificacionverticaltitulo', 'colorfondologo',
			'colorfondotitulo','avatartitulo', 'colorhovermenu','tienecolorhover',
			'altopixelestitulo','anchopixelestitulo','tituloizquierda','conseguridad')

		widgets = {
			'nombre': forms.TextInput(attrs={'class':'form-control'}),
			'descripcion': forms.Textarea(attrs={'class':'form-control'}),
			'autor': forms.TextInput(attrs={'class':'form-control'}),
			'avatar': forms.ClearableFileInput(attrs={'class':'form-control-file'}),
			'avatartitulo': forms.ClearableFileInput(attrs={'class':'form-control-file'}),
			'directorio': forms.TextInput(attrs={'class':'form-control'}),
			# 'altopixeles': forms.TextInput(attrs={'class':'form-control'}),
			# 'anchopixeles': forms.TextInput(attrs={'class':'form-control'}),
			# 'numerocolumnas': forms.TextInput(attrs={'class':'form-control'}),
			# 'justificacion': forms.Select(attrs={'class':'form-control'}, choices=JUSTIFICACION_CHOICES),
			'justificacion': forms.Select(choices=JUSTIFICACION_CHOICES),
			# 'justificaciontitulo': forms.Select(attrs={'class':'form-control'}, choices=JUSTIFICACION_CHOICES),
			'justificaciontitulo': forms.Select(choices=JUSTIFICACION_CHOICES),
			'justificacionverticaltitulo': forms.Select(choices=JUSTIFICACION_V_CHOICES),
			'justificacionverticallogo': forms.Select(choices=JUSTIFICACION_V_CHOICES),
			'colormenu': forms.Select(choices=MENU_COLOR_CHOICES),
			'colorfondomenu': forms.Select(choices=MENU_COLOR_CHOICES),
			# 'numerocolumnastitulo': forms.TextInput(attrs={'class':'form-control'}),
			# 'textotitulo': forms.TextInput(attrs={'class':'form-control'}),
			# 'fonttitulo': forms.TextInput(attrs={'class':'form-control'}),
			# 'colortitulo': forms.TextInput(attrs={'class':'form-control'}),
			# 'columnasdivision': forms.TextInput(attrs={'class':'form-control'}),
			# 'colormenu': forms.TextInput(attrs={'class':'form-control'}),
			# 'colorfondomenu': forms.TextInput(attrs={'class':'form-control'}),
			# 'fontmenu': forms.TextInput(attrs={'class':'form-control'}),
		}
		labels = {
			'nombre':'', 'descripcion':'', 'autor':'','directorio': 'Directorio','altopixeles':'','anchopixeles':'','numerocolumnas':'','justificacion':'',
		}

class CrearDirectoriosForm(forms.Form):

	nombre = forms.CharField(label="",required=True, widget = forms.TextInput(
		attrs={'class': 'form-control','placeholder':'Directorio'}
		), min_length=3,max_length=50)

	class Meta:
		fields = ('nombre',)

	def clean(self):
		# Se leen los campos del formulario despues de submit y antes de grabarlos
		nombre = self.cleaned_data['nombre']
		
		# return name #- esto solo si es  clean_fieldname

class EscribirArchivosForm(forms.Form):

	nombre = forms.CharField(label="",required=True, widget = forms.Textarea(
		attrs={'class': 'form-control','placeholder':'Directorio'}
		), min_length=0,max_length=500)

	class Meta:
		fields = ('nombre',)

	def clean(self):
		# Se leen los campos del formulario despues de submit y antes de grabarlos
		nombre = self.cleaned_data['nombre']
		
		# return name #- esto solo si es  clean_fieldname

