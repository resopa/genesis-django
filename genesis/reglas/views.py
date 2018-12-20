from django.views.generic.list import ListView
from .models import Regla
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy

from reglas.models import Regla
from propiedades.models import Propiedad
from aplicaciones.models import Aplicacion
from .forms import ReglaForm

class ReglaListaView(ListView):
    model = Regla

class EditarReglaView(UpdateView):
    model = Regla
    form_class = ReglaForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse_lazy('propiedades:editar', args=[self.request.GET['propiedad_id']]) + '?ok'

    def get_context_data(self,**kwargs):
        context = super(EditarReglaView, self).get_context_data(**kwargs)
        obj = Regla.objects.get(id=self.object.id)
        context['propiedad_id'] = obj.propiedad.id
        propiedad = Propiedad.objects.get(id=obj.propiedad.id)
        context['modelo_id'] = propiedad.modelo.id
        aplicacion = Aplicacion.objects.get(id=propiedad.modelo.aplicacion.id)
        context['proyecto_id'] = aplicacion.proyecto.id
        return context

from django.http import HttpResponseRedirect

class CrearReglaView(CreateView):
    model = Regla
    form_class = ReglaForm

    def get_success_url(self):
        return reverse_lazy('propiedades:editar', args=[self.request.GET['propiedad_id']]) + '?ok'

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        propiedad = Propiedad.objects.get(id = request.GET['propiedad_id'])
        if form.is_valid():
            regla = form.save(commit=False)
            regla.propiedad = propiedad
            regla.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class BorrarReglaView(DeleteView):
    model = Regla

    def get_success_url(self):
        return reverse_lazy('propiedades:editar', args=[self.request.GET['propiedad_id']]) + '?ok'

    def get_context_data(self,**kwargs):
        context = super(BorrarReglaView, self).get_context_data(**kwargs)
        obj = Regla.objects.get(id=self.object.id)
        context['nombre'] = obj.mensaje
        context['propiedad_id'] = obj.propiedad.id
        propiedad = Propiedad.objects.get(id=obj.propiedad.id)
        context['modelo_id'] = propiedad.modelo.id
        return context