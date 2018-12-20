from django import forms
from modelos.models import Modelo
from reglas.models import Regla

class ReglaForm(forms.ModelForm):
	class Meta:
		model = Regla

		fields = ('mensaje', 'codigo', )
		
		widgets = {
			'mensaje': forms.TextInput(attrs={'class':'form-control', 'placeholder': ''}),
			'codigo': forms.Textarea(attrs={'class':'form-control', 'placeholder': ''}),
		}
		labels = {
			'mensaje': '', 'codigo': ''
		}

