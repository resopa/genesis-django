from django.db import models

class Crear(models.Model):
	proyectoid = models.IntegerField(default=0)
	aplicacionid = models.IntegerField(default=0)
	modeloid = models.IntegerField(default=0)
	propiedadid = models.IntegerField(default=0)
	reglaid = models.IntegerField(default=0)
	elemento = models.CharField(max_length=1)
	nombre = models.CharField(max_length=30)
	nombremayuscula = models.CharField(max_length=30,blank=True)
	padre = models.CharField(max_length=30,default='')
	tipo = models.CharField(max_length=1,default='')
	nombretipo = models.CharField(max_length=15,default='')
	largostring = models.SmallIntegerField(default=0)
	foranea = models.CharField(max_length=30,default='')
	inicial = models.CharField(max_length=30,default='')
	mensaje = models.TextField(default='')
	codigo = models.TextField(default='')
	etiqueta = models.CharField(max_length=100)
	nombreself = models.CharField(max_length=100)
	textobotones = models.CharField(max_length=100)
	primero = models.BooleanField(default='False')
	identa = models.IntegerField(default=0)
	restoidenta = models.IntegerField(default=0)

	def __str__(self):
		return self.elemento + ' ' + self.nombre