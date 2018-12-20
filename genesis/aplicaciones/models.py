from django.db import models
from ckeditor.fields import RichTextField

from proyectos.models import Proyecto

# Create your models here.

class Aplicacion(models.Model):
	nombre = models.CharField(max_length=30)
	descripcion = RichTextField()
	proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
	#parametros
	textoenmenu = models.CharField(max_length=30)

	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.nombre