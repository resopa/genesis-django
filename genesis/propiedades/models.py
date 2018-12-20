from django.db import models
from ckeditor.fields import RichTextField

from modelos.models import Modelo

# Create your models here.

class Propiedad(models.Model):
	nombre = models.CharField(max_length=30)
	descripcion = RichTextField()
	tipo = models.CharField(max_length=1)
	largostring = models.SmallIntegerField(default=0)
	foranea = models.CharField(max_length=30,default='nada')
	inicial = models.CharField(max_length=30,blank=True)
	modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE)
	etiqueta = models.CharField(max_length=100, blank=True)
	textobotones = models.CharField(max_length=100,blank=True)
	enlista = models.BooleanField(default=False)
	numerocolumnas = models.SmallIntegerField(default=1)
	formatofecha = models.CharField(max_length=30,default='',blank=True)

	# Parametrizacion

	textocolumna = models.CharField(max_length=100, blank=True)
	justificaciontextocolumna = models.CharField(max_length=1,default='i')

	etiquetaarriba = models.BooleanField(default=True)
	textoplaceholder = models.CharField(max_length=50,blank=True)

	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")
	
	def __str__(self):
		return self.nombre