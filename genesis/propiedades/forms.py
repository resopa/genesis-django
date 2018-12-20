from django import forms
from modelos.models import Modelo
from propiedades.models import Propiedad

YEAR_CHOICES =[]
b=1917
for a in range(0,120):
	YEAR_CHOICES.append(b+a)

TIPO_CHOICES = (
		('s','String'),
		('x','Text Field'),
		('h','RichText'),
		('m','Entero pequeno'),
		('i','Entero'),
		('l','Entero largo'),
		('d','Decimal'),
		('f','Foranea'),
		('t','Fecha'),
		('b','Boolean'),
		('r','Radio Button'),
		('p','Imagen'),
	)

JUSTIFICACION_CHOICES = (
   ('i', 'Izquierda'),
   ('d', 'Derecha'),
   ('c', 'Centro'),
	)

class PropiedadForm(forms.ModelForm):
	class Meta:
		model = Propiedad

		fields = ('nombre', 'descripcion', 'tipo',  'largostring', 'inicial', 'foranea', 
		'etiqueta', 'textobotones','enlista','numerocolumnas','formatofecha',
		'etiquetaarriba','textoplaceholder','justificaciontextocolumna',
		'textocolumna' ,)

		widgets = {
			'nombre': forms.TextInput(attrs={'class':'form-control','placeholder': ''}),
			'descripcion': forms.Textarea(attrs={'class':'form-control', 'placeholder': ''}),
			'tipo': forms.Select(choices=TIPO_CHOICES),
			'largostring': forms.NumberInput(attrs={'class':'form-control','placeholder': ''}),
			'inicial': forms.TextInput(attrs={'class':'form-control','placeholder': ''}),
			'foranea': forms.TextInput(attrs={'class':'form-control','placeholder': ''}),
			'textobotones': forms.TextInput(attrs={'class':'form-control','placeholder': ''}),
			'enlista' : forms.CheckboxInput(attrs={'disabled':False}),
			'formatofecha': forms.TextInput(attrs={'class':'form-control','placeholder': ''}),
			'numerocolumnas': forms.NumberInput(attrs={'class':'form-control','placeholder': ''}),
			'justificaciontextocolumna': forms.Select(choices=JUSTIFICACION_CHOICES),
		}
		labels = {
			'nombre': '', 'descripcion': '', 'tipo': '', 'largostring': 'Largo string','inicial': 'Inicial', 'foranea': 'Foranea','etiqueta':'Label','textobotones':'Texto de Botones','enlista':'En la lista','numerocolumnas':'Numero columnas','formatofecha': 'Formato de fecha'
		}

