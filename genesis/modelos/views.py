from django.views.generic.list import ListView
from .models import Aplicacion
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse, reverse_lazy

from modelos.models import Modelo
from propiedades.models import Propiedad
from proyectos.models import Proyecto
from .forms import ModeloForm

class ModeloListaView(ListView):
    model = Modelo

class EditarModeloView(UpdateView):
    model = Modelo
    form_class = ModeloForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        modelo = self.object
        modelo.nombre = modelo.nombre.lower()
        # actualiza proyecto
        aplicacion = Aplicacion.objects.get(id = self.request.GET['aplicacion_id'])
        proyecto = Proyecto.objects.get(id=aplicacion.proyecto.id)
        modelo.aplicacion = aplicacion
        modelo.proyecto = proyecto        
        modelo.save()
        return reverse_lazy('aplicaciones:editar', args=[self.request.GET['aplicacion_id']]) + '?ok'

    def get_context_data(self,**kwargs):
        context = super(EditarModeloView, self).get_context_data(**kwargs)
        context['aplicacion_id'] = self.object.aplicacion.id
        aplicacion = Aplicacion.objects.get(id=self.object.aplicacion.id)
        context['proyecto_id'] = aplicacion.proyecto.id
        propiedades = Propiedad.objects.filter(modelo=self.object)
        print (self.request.GET['aplicacion_id'])
        context['listapropiedad'] = propiedades
        context['nombre'] = self.object.nombre
        context['numero'] = Propiedad.objects.filter(modelo=self.object).count()
        return context

from django.http import HttpResponseRedirect

class CrearModeloView(CreateView):
    model = Modelo
    form_class = ModeloForm

    def get_success_url(self):
        return reverse_lazy('aplicaciones:editar', args=[self.request.GET['aplicacion_id']]) + '?ok'

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        aplicacion = Aplicacion.objects.get(id = request.GET['aplicacion_id'])
        if form.is_valid():
            modelo = form.save(commit=False)
            modelo.nombre = modelo.nombre.lower()
            modelo.aplicacion = aplicacion
            aplicacion = Aplicacion.objects.get(id = request.GET['aplicacion_id'])
            proyecto = Proyecto.objects.get(id=aplicacion.proyecto.id)
            modelo.proyecto = proyecto
            #Valores vacios
            if modelo.textoopcionmenu == '':
                modelo.textoopcionmenu = modelo.nombre
            if modelo.titulolista == '':
                modelo.titulolista = 'Lista de ' + modelo.nombre
            if modelo.textotitulolistahijos == '':
                modelo.textotitulolistahijos = 'Lista de ' + modelo.nombre
            modelo.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class BorrarModeloView(DeleteView):
    model = Modelo

    def get_success_url(self):
        return reverse_lazy('aplicaciones:editar', args=[self.request.GET['aplicacion_id']]) + '?ok'

    def get_context_data(self,**kwargs):
        context = super(BorrarModeloView, self).get_context_data(**kwargs)
        obj = Modelo.objects.get(id=self.object.id)
        context['nombre'] = obj.nombre
        context['aplicacion_id'] = obj.aplicacion.id
        aplicacion = Aplicacion.objects.get(id=obj.aplicacion.id)
        context['proyecto_id'] = aplicacion.proyecto.id
        return context