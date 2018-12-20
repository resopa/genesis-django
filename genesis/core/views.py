from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView, RedirectView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.list import ListView

# from .forms import GenesisForm
from .models import Genesis
from .models import TutorialEncabezado, TutorialDetalle
from .forms import TutorialEncabezadoForm, TutorialDetalleForm

import os,shutil
import string

# @method_decorator(staff_member_required, name='dispatch')
class CorePageView(TemplateView):
    template_name = "core/home.html"

# class EditarGenesisView(UpdateView):
#     form_class = GenesisForm
#     template_name = 'core/que_es_genesis.html'

#     def get_success_url(self):
#         return reverse_lazy('core:home', args=[self.object.id]) + '?ok'

#     def get_object(self):
#         # Recuperar el objeto a editar
#         genesis,created =  Genesis.objects.get_or_create(nombre='GENESIS')
#         # parametro.delete()
#         return genesis    

class DespliegaGenesisView(TemplateView):
    template_name = 'core/que_es_genesis.html'
    modelo = Genesis

    def get_context_data(self, **kwargs):
        context = super(DespliegaGenesisView, self).get_context_data(**kwargs)
        # context = super().get_context_data(**kwargs)
        try:
            context['genesis_real'] = Genesis.objects.get(nombre='GENESIS').descripcion
        except:
            context['genesis_real'] = None

        print(context)
        return context        
    def dispatch(self, request, *args, **kwargs):
        print(request.user)
        return super(DespliegaGenesisView,self).dispatch(request,*args,**kwargs)

class TutorialGenesisView(TemplateView):
    template_name = "core/home.html"


class TutorialEncabezadoListaView(ListView):
    model = TutorialEncabezado
    def get_context_data(self,**kwargs):
        context = super(TutorialEncabezadoListaView, self).get_context_data(**kwargs)
        print(TutorialEncabezado.objects.all().count())
        context['lista'] = TutorialEncabezado.objects.all()
        return context      

class EditarTutorialEncabezadoView(UpdateView):
    model = TutorialEncabezado
    form_class = TutorialEncabezadoForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse_lazy('core:editar_tutorial_encabezado', args=[self.object.id]) + '?ok'

    def get_context_data(self,**kwargs):
        context = super(EditarTutorialEncabezadoView, self).get_context_data(**kwargs)
        tutorialencabezado = (self.object)
        tutorialdetalles = TutorialDetalle.objects.filter(tutorialencabezado = tutorialencabezado)
        context['listadetalle'] = tutorialdetalles
        context['nombre'] = tutorialencabezado.topico
        context['diagrama'] = tutorialencabezado.diagrama
        return context

from django.http import HttpResponseRedirect

class CrearTutorialEncabezadoView(CreateView):
    model = TutorialEncabezado
    form_class = TutorialEncabezadoForm

    def get_success_url(self):
        return reverse_lazy('core:tutorial')

class BorrarTutorialEncabezadoView(DeleteView):
    model = TutorialEncabezado

    def get_success_url(self):
        return reverse_lazy('core:tutorial')

    def get_context_data(self,**kwargs):
        context = super(BorrarTutorialEncabezadoView, self).get_context_data(**kwargs)
        obj = TutorialEncabezado.objects.get(id=self.object.id)
        context['nombre'] = obj.topico
        return context

class TutorialDetalleListaView(ListView):
    model = TutorialDetalle

class EditarTutorialDetalleView(UpdateView):
    model = TutorialDetalle
    form_class = TutorialDetalleForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse_lazy('core:editar_tutorial_encabezado', args=[self.request.GET['tutorialencabezado_id']]) + '?ok'

    def get_context_data(self,**kwargs):
        context = super(EditarTutorialDetalleView, self).get_context_data(**kwargs)
        context['nombre'] = self.object.topico
        context['diagrama'] = self.object.diagrama
        return context

from django.http import HttpResponseRedirect

class CrearTutorialDetalleView(CreateView):
    model = TutorialDetalle
    form_class = TutorialDetalleForm

    def get_success_url(self):
        return reverse_lazy('core:editar_tutorial_encabezado', args=[self.request.GET['tutorialencabezado_id']]) + '?ok'

    def get_context_data(self,**kwargs):
        context = super(CrearTutorialDetalleView, self).get_context_data(**kwargs)
        context['tutorialencabezado_id'] = self.request.GET['tutorialencabezado_id']
        return context

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        tutorialencabezado = TutorialEncabezado.objects.get(id = request.GET['tutorialencabezado_id'])
        if form.is_valid():
            tutorialdetalle = form.save(commit=False)
            tutorialdetalle.tutorialencabezado = tutorialencabezado
            tutorialdetalle.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class BorrarTutorialDetalleView(DeleteView):
    model = TutorialDetalle

    def get_success_url(self):
        return reverse_lazy('core:editar_tutorial_encabezado', args=[self.request.GET['tutorialencabezado_id']]) + '?ok'

    def get_context_data(self,**kwargs):
        context = super(BorrarTutorialDetalleView, self).get_context_data(**kwargs)
        obj = TutorialDetalle.objects.get(id=self.object.id)
        context['nombre'] = obj.topico
        context['tutorialencabezado_id'] = obj.tutorialencabezado.id
        return context        

class DespliegaTutorialView(TemplateView):
    template_name = 'core/despliega_tutorial.html'
    modelo = TutorialEncabezado

    def get_context_data(self, **kwargs):
        context = super(DespliegaTutorialView, self).get_context_data(**kwargs)
        lista =[]
        tel = TutorialEncabezado.objects.all()
        for te in tel:
            lista.append([te.topico.upper(),te.descripcion,str(te.correlativo) + '.',te.diagrama,'e',te.id])
            tdl = TutorialDetalle.objects.filter(tutorialencabezado = te)
            for td in tdl:
                lista.append([string.capwords(td.topico.lower()),td.descripcion,str(te.correlativo) + '.' + str(td.correlativo) + '.',td.diagrama,'d',td.id])
        context['lista'] = lista
        print(lista[0][1])
        return context      

class DesplegarPreciosView(TemplateView):
    template_name = "core/desplegar_precios.html"
    model = TutorialDetalle
    print('entro')

    def dispatch(self, *args, **kwargs):
        print('dispatch1113')
        print(self.request.POST.get('hosted_button_id', None))
        return super(DesplegarPreciosView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        print ('pst1')
        
        return HttpResponseRedirect('https://www.paypal.com/cgi-bin/webscr')
        # return self.get(request, *args, **kwargs)
    def patch(self, request, *args, **kwargs):
        print ('pst2')
        return self.get(request, *args, **kwargs)
    def put(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

class CompraExitosaView(TemplateView):
    template_name = 'core/compra_exitosa.html'

    def get_context_data(self, **kwargs):
        context = super(CompraExitosaView, self).get_context_data(**kwargs)
        context['version_id'] = self.request.GET['version_id']
        return context       
