from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.sessions.models import Session

from .models import Crear

class CrearForm(forms.ModelForm):
	class Meta:
		model = Crear
		fields = ('nombre',)
		widgets = {
			'nombre': forms.TextInput(attrs={'class':'form-control mt-3', 'placeholder': 'Nombre del Modelo'}),
		}
		labels = {
			'nombre':''
		}

