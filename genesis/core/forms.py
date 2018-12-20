from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.sessions.models import Session

from .models import TutorialEncabezado
from .models import TutorialDetalle

class TutorialEncabezadoForm(forms.ModelForm):
	class Meta:
		model = TutorialEncabezado
		fields = ('topico', 'descripcion', 'correlativo', 'diagrama')
		widgets = {
			'topico': forms.TextInput(attrs={'class':'form-control' }),
			'Descripcion': forms.Textarea(attrs={'class':'form-control'}),
			'diagrama': forms.ClearableFileInput(attrs={'class':'form-control-file'}),		}
		labels = {
			'topico':'', 'descripcion':''
		}

class TutorialDetalleForm(forms.ModelForm):
	class Meta:
		model = TutorialDetalle
		fields = ('topico', 'descripcion','correlativo','diagrama')
		widgets = {
			'topico': forms.TextInput(attrs={'class':'form-control' }),
			'Descripcion': forms.Textarea(attrs={'class':'form-control'}),
			'diagrama': forms.ClearableFileInput(attrs={'class':'form-control-file'}),		}
		
		labels = {
			'topico':'', 'descripcion':''
		}

