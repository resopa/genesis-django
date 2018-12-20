from django.db import models
from ckeditor.fields import RichTextField

from aplicaciones.models import Aplicacion
from proyectos.models import Proyecto

# Create your models here.

class Modelo(models.Model):
	nombre = models.CharField(max_length=30)
	descripcion = RichTextField()
	padre = models.CharField(max_length=30,default='nada')
	nombreself = models.CharField(max_length=100)
	nombreborrar = models.CharField(max_length=100)
	aplicacion = models.ForeignKey(Aplicacion, on_delete=models.CASCADE)
	proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)

	#menu
	textoopcionmenu = models.CharField(max_length=30, blank=True)

	# Lista de modelos
	titulolista = models.CharField(max_length=30,blank=True)
	colorfondotitulolista = models.CharField(max_length=20,default='black')
	fonttitulolista = models.CharField(max_length=100,default='Arial,15,bold')
	colortitulolista = models.CharField(max_length=20,default='black')
	justificaciontitulolista = models.CharField(max_length=1,default='c')
	mayusculastitulolista = models.BooleanField(default=True)
	altotitulolista = models.SmallIntegerField(default=100)
	justificacionverticaltitulolista = models.CharField(max_length=1,default='c')
	bordeinferior = models.BooleanField(default=True)

	fontcolumnas = models.CharField(max_length=100,default='Arial,15,bold')
	colorcolumnas = models.CharField(max_length=20,default='black')
	colorfondocolumnas = models.CharField(max_length=20,default='black')
	mayusculascolumnas = models.BooleanField(default=True)
	altocolumnas = models.SmallIntegerField(default=30)

	fonteditarborrar = models.CharField(max_length=100,default='Arial,15,bold')
	coloreditarborrar = models.CharField(max_length=20,default='black')
	textoeditarborrar = models.CharField(max_length=30,default='Editar,Borrar')

	fontlinknuevo = models.CharField(max_length=100,default='Arial,15,bold')
	colorlinknuevo = models.CharField(max_length=20,default='black')
	textolinknuevo = models.CharField(max_length=30,default='Nuevo registro')
	linkboton = models.BooleanField(default=True)
	colorbotonlinknuevo = models.CharField(max_length=20,default='black')

	fonttextolista = models.CharField(max_length=100,default='Arial,12,bold')
	colortextolista = models.CharField(max_length=20,default='black')
	colorfondotextolista = models.CharField(max_length=20,default='white')

	# Modelo nuevo

	textotitulopagina = models.CharField(max_length=30,default='Nuevo registro')
	colortextotitulopagina = models.CharField(max_length=20,default='black')
	fonttextotitulopagina = models.CharField(max_length=100,default='Arial,15,bold')
	controlesautomaticos = models.BooleanField(default=True)

	# Modelo modificado
	hijoscontiguos = models.BooleanField(default=True)

	textotitulolistahijos = models.CharField(max_length=30,blank=True)
	fonttextotitulolistahijos = models.CharField(max_length=100,default='Arial,15,bold')
	colortextolistahijos = models.CharField(max_length=20,default='black')
	colorfondotitulolistahijos = models.CharField(max_length=20,default='black')
	mayusculastitulolistahijos = models.BooleanField(default=True)
	justificaciontitulolistahijos = models.CharField(max_length=1,default='i')
	altotitulolistahijos = models.SmallIntegerField(default=100)
	justificacionverticaltitulolistahijos = models.CharField(max_length=1,default='c')
	
	fontcolumnaslistahijos = models.CharField(max_length=100,default='Arial,15,bold')
	colorcolumnaslistahijos = models.CharField(max_length=20,default='black')
	mayusculascolumnaslistahijos = models.BooleanField(default=True)
	fondocolumnaslistahijos = models.CharField(max_length=20,default='black')
	altocolumnaslistahijos = models.SmallIntegerField(default=30)

	numerocolumnasizquierdaedicion = models.SmallIntegerField(default=1)
	numerocolumnasderechaedicion = models.SmallIntegerField(default=1)
	numerocolumnasmodeloedicion = models.SmallIntegerField(default=1)
	numerocolumnashijosedicion = models.SmallIntegerField(default=1)

	numerocolumnasizquierdanuevo = models.SmallIntegerField(default=1)
	numerocolumnasderechanuevo = models.SmallIntegerField(default=1)
	numerocolumnasmodelonuevo = models.SmallIntegerField(default=1)

	fontetiqueta = models.CharField(max_length=100,default='Arial,15,bold')
	coloretiqueta = models.CharField(max_length=20,default='black')
	etiquetaarriba = models.BooleanField(default=True)


	# Borrado del modelo
	textoborrado = models.CharField(max_length=30,default='Desea borrar el registro')
	textobotonborrado = models.CharField(max_length=30,default='Borrar')
	fonttextoborrado = models.CharField(max_length=100,default='Arial,15,bold')
	colortextoborrado = models.CharField(max_length=20,default='black')

	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")
	
	def __str__(self):
		return self.nombre