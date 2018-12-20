from django.views.generic.list import ListView
from .models import Modelo
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy

from propiedades.models import Propiedad
from reglas.models import Regla
from aplicaciones.models import Aplicacion
from modelos.models import Modelo
from .forms import PropiedadForm

class PropiedadListaView(ListView):
    model = Propiedad

class EditarPropiedadView(UpdateView):
    model = Propiedad
    form_class = PropiedadForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse_lazy('modelos:editar', args=[self.request.GET['modelo_id']]) + '?ok'

    def get_context_data(self,**kwargs):
        context = super(EditarPropiedadView, self).get_context_data(**kwargs)
        obj = Modelo.objects.get(id=self.object.modelo.id)
        context['modelo_id'] = obj.id
        aplicacion = Aplicacion.objects.get(id=obj.aplicacion.id)
        context['proyecto_id'] = aplicacion.proyecto.id
        context['aplicacion_id'] = aplicacion.id
        reglas = Regla.objects.filter(propiedad=self.object)
        context['listaregla'] = reglas
        context['nombre'] = self.object.nombre
        context['numero'] = Regla.objects.filter(propiedad=self.object).count()
        return context

from django.http import HttpResponseRedirect

class CrearPropiedadView(CreateView):
    model = Propiedad
    form_class = PropiedadForm

    def get_success_url(self):
        return reverse_lazy('modelos:editar', args=[self.request.GET['modelo_id']]) + '?ok'

    def get_context_data(self,**kwargs):
        context = super(CrearPropiedadView, self).get_context_data(**kwargs)
        obj = Modelo.objects.get(id=self.request.GET['modelo_id'])
        context['modelo_id'] = obj.id
        aplicacion = Aplicacion.objects.get(id=obj.aplicacion.id)
        context['aplicacion_id'] = aplicacion.id
        return context

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        modelo = Modelo.objects.get(id = request.GET['modelo_id'])
        if form.is_valid():
            propiedad = form.save(commit=False)
            propiedad.modelo = modelo
            #valores defauls
            if propiedad.etiqueta == '':
                propiedad.etiqueta = propiedad.nombre
            if propiedad.textocolumna == '':
                propiedad.textocolumna = propiedad.nombre
            propiedad.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class BorrarPropiedadView(DeleteView):
    model = Propiedad

    def get_success_url(self):
        return reverse_lazy('modelos:editar', args=[self.request.GET['modelo_id']]) + '?ok'

    def get_context_data(self,**kwargs):
        context = super(BorrarPropiedadView, self).get_context_data(**kwargs)
        obj = Propiedad.objects.get(id=self.object.id)
        context['nombre'] = obj.nombre
        context['modelo_id'] = obj.modelo.id
        modelo = Modelo.objects.get(id=obj.modelo.id)
        context['aplicacion_id'] = modelo.aplicacion.id
        return context