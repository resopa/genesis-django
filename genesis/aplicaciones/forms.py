from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.sessions.models import Session

from .models import Aplicacion

class AplicacionForm(forms.ModelForm):
	class Meta:
		model = Aplicacion
		fields = ('nombre', 'descripcion','textoenmenu')
		widgets = {
			'nombre': forms.TextInput(attrs={'class':'form-control' }),
			'Descripcion': forms.Textarea(attrs={'class':'form-control'}),
			'textoenmenu': forms.TextInput(attrs={'class':'form-control'}),
		}
		labels = {
			'nombre':'', 'descripcion':''
		}

