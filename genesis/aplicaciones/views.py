from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy

from aplicaciones.models import Aplicacion
from modelos.models import Modelo
from proyectos.models import Proyecto
from .forms import AplicacionForm

class AplicacionListaView(ListView):
    model = Aplicacion

class EditarAplicacionView(UpdateView):
    model = Aplicacion
    form_class = AplicacionForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse_lazy('aplicaciones:editar', args=[self.object.id]) + '?ok'

    def get_context_data(self,**kwargs):
        context = super(EditarAplicacionView, self).get_context_data(**kwargs)
        modelos = Modelo.objects.filter(aplicacion = self.object)
        context['nombre'] = self.object.nombre
        context['listamodelo'] =  modelos
        context['proyecto_id'] = self.object.proyecto.id
        context['numero'] = Modelo.objects.filter(aplicacion=self.object).count()
        return context

from django.http import HttpResponseRedirect

class CrearAplicacionView(CreateView):
    model = Aplicacion
    form_class = AplicacionForm

    def get_success_url(self):
        return reverse_lazy('proyectos:editar', args=[self.request.GET['proyecto_id']]) + '?ok'

    def get_context_data(self,**kwargs):
        context = super(CrearAplicacionView, self).get_context_data(**kwargs)
        context['proyecto_id'] = self.request.GET['proyecto_id']
        return context

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        proyecto = Proyecto.objects.get(id = request.GET['proyecto_id'])
        if form.is_valid():
            aplicacion = form.save(commit=False)
            aplicacion.proyecto = proyecto
            aplicacion.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class BorrarAplicacionView(DeleteView):
    model = Aplicacion

    def get_success_url(self):
        return reverse_lazy('proyectos:editar', args=[self.request.GET['proyecto_id']]) + '?ok'

    def get_context_data(self,**kwargs):
        context = super(BorrarAplicacionView, self).get_context_data(**kwargs)
        obj = Aplicacion.objects.get(id=self.object.id)
        context['nombre'] = obj.nombre
        context['proyecto_id'] = obj.proyecto.id
        return context