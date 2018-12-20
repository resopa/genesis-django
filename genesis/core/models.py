from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

class Genesis(models.Model):
	nombre = models.CharField(max_length=30, default='GENESIS')
	descripcion = RichTextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.nombre

class TutorialEncabezado(models.Model):
	topico = models.CharField(max_length=30)
	correlativo = models.IntegerField(default=1)
	descripcion = RichTextField()
	diagrama = models.ImageField(upload_to='tutorial',blank=True,null=True)

	def __str__(self):
		return self.topico

class TutorialDetalle(models.Model):
	topico = models.CharField(max_length=30)
	correlativo = models.IntegerField(default=1)
	descripcion = RichTextField()
	diagrama = models.ImageField(upload_to='tutorial',blank=True,null=True)
	tutorialencabezado = models.ForeignKey(TutorialEncabezado, on_delete=models.CASCADE)

	def __str__(self):
		return self.topico
