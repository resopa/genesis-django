from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.

class Proyecto(models.Model):
	usuario = models.ForeignKey(User,on_delete=models.CASCADE)
	nombre = models.CharField(max_length=30)
	autor = models.CharField(max_length=30,blank=True)
	avatar = models.ImageField(upload_to='proyectos',blank=True,null=True)
	descripcion = RichTextField()
	directorio = models.CharField(max_length=150,blank=True)
	textoopcioninicio = models.CharField(max_length=50)
	altopixeles = models.SmallIntegerField(default=100)
	anchopixeles = models.SmallIntegerField(default=100)
	numerocolumnas = models.SmallIntegerField(default=3)
	justificacion = models.CharField(max_length=1,default='c')
	justificaciontitulo = models.CharField(max_length=1,default='c')
	numerocolumnastitulo = models.SmallIntegerField(default=9)
	textotitulo = models.CharField(max_length=50, blank=True)
	fonttitulo = models.CharField(max_length=100,default='Arial,15,bold')
	colortitulo = models.CharField(max_length=20,default='black')
	altopixelestitulo = models.SmallIntegerField(default=100)
	anchopixelestitulo = models.SmallIntegerField(default=100)
	colorfondomenu = models.CharField(max_length=20,default='black')
	fontmenu = models.CharField(max_length=100,default='Arial,15,bold')
	colormenu = models.CharField(max_length=20,default='black')
	colorhovermenu = models.CharField(max_length=20,default='black')
	tienecolorhover = models.BooleanField(default=False)
	mayusculas = models.BooleanField(default=True)
	altomenu = models.SmallIntegerField(default=100)
	numerocolumnasizquierda = models.SmallIntegerField(default=0)
	numerocolumnasderecha = models.SmallIntegerField(default=0)
	numerocolumnascentro = models.SmallIntegerField(default=12)
	numerodivisionespie = models.SmallIntegerField(default=12)
	columnasdivision = models.CharField(max_length=30)
	columnasderechaencabezado = models.SmallIntegerField(default=0)
	columnasizquierdaencabezado = models.SmallIntegerField(default=0)
	listafontsgoogle = models.CharField(max_length=200)

	colorfondoencabezado = models.CharField(max_length=20,default='black')
	colorfondologo = models.CharField(max_length=20,default='black')
	colorfondotitulo = models.CharField(max_length=20,default='black')
	altoencabezado = models.SmallIntegerField(default=100)
	justificacionverticallogo = models.CharField(max_length=1,default='c')
	justificacionverticaltitulo = models.CharField(max_length=1,default='c')
	avatartitulo = models.ImageField(upload_to='proyectos',blank=True,null=True)

	tituloizquierda = models.BooleanField(default=False)

	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	
	conseguridad = models.BooleanField(default=False)
	
	def __str__(self):
		return self.nombre