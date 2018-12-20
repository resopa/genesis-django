from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from .models import Proyecto
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views import View
from django.urls import reverse, reverse_lazy
from .forms import ProyectoForm
from crear import views

from aplicaciones.models import Aplicacion
import os

#seguridad
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

# Create your views here.
# @method_decorator(staff_member_required,name='dispatch')
class ListarProyectoView(ListView):
    model = Proyecto

    def get_context_data(self, **kwargs):
        context = super(ListarProyectoView, self).get_context_data(**kwargs)
        cd = os.getcwd()
        print('Directorio actual ' + cd)
        # Crear directorio
        try:
            os.mkdir(cd + "/archivos")
        except:
            print('ya existe')
        # Listar directorios
        lista = os.listdir()
        print (lista)        

        # print(self.request.user)
        # # renombrar directorios
        # os.rename('archivos','files')

        # # remover directorio
        # os.rmdir('files')
        # lista = os.listdir()
        # print (lista)        

        # escribir un archivo
        fo = open(cd + '/archivos/foo.txt', "w")
        print ("Name of the file: ", fo.name)
        print ("Closed or not : ", fo.closed)
        print ("Opening mode : ", fo.mode)
        fo.write("esta es la prueba\n\tpara que se cumpla\n\tlo previsto")
        fo.close()

        #split
        texto = 'esta es, la linea'
        print (texto.split(','))

        # leer archivo
        fo = open(cd + '/archivos/foo.txt', "r+")
        stri = fo.readlines()   
        for c in stri:
            print ("cada linea : ", c)
        

        # fd = os.open(cd + '/archivos/prueba.txt',os.O_CREAT)
        # with os.fdopen(os.open(cd + '/archivos/prueba.txt',os.O_CREAT | os.O_RDWR ),'w') as fd:  
        #     fd.write("abcd")
        # fd.close() 

        # with os.open( cd + '/archivos/prueba.txt', os.O_RDWR|os.O_CREAT ) as fd:
        #     fd.write("This is test")
        # f.close()

        #lista de proyectos por usuario
        try:
            listaproyectos = Proyecto.objects.filter(usuario=self.request.user)
        except:
            listaproyectos = None

        context['listadir'] = lista
        context['listaproyectos'] = listaproyectos
        return context

class EditarProyectoView(UpdateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse_lazy('proyectos:editar', args=[self.object.id]) + '?ok'

    def get_context_data(self,**kwargs):
        context = super(EditarProyectoView, self).get_context_data(**kwargs)
        proyecto = (self.object)
        aplicaciones = Aplicacion.objects.filter(proyecto = proyecto)
        context['nombre'] = proyecto.nombre
        context['listaaplicacion'] =  aplicaciones
        context['proyecto_id'] = self.object.id
        context['avatar'] = proyecto.avatar
        context['avatartitulo'] = proyecto.avatartitulo
        context['numero'] = Aplicacion.objects.filter(proyecto=proyecto).count()
        return context

class CrearProyectoView(CreateView):
    model = Proyecto
    form_class = ProyectoForm

    def get_success_url(self):
        return reverse_lazy('proyectos:home')
        # return reverse_lazy('proyectos:editar', args=[self.object.id]) + '?ok'

    def dispatch(self, request, *args, **kwargs):
        print(request.user)
        return super(CrearProyectoView,self).dispatch(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        user = request.user
        # print(user)
        if form.is_valid():
            proyecto = form.save(commit=False)
            proyecto.usuario = user
            proyecto.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class BorrarProyectoView(DeleteView):
    model = Proyecto
    success_url = reverse_lazy('proyectos:home')

    def get_context_data(self,**kwargs):
        context = super(BorrarProyectoView, self).get_context_data(**kwargs)
        obj = Proyecto.objects.get(id=self.object.id)
        context['nombre'] = obj.nombre
        return context

from django.shortcuts import render
import shutil
class dumpView(View):

    template_name = 'proyectos/download.html'
    def get(self, request):
        shutil.make_archive('/home/alterego/Documents/proyectos/genesis/core/zipfiles/zipfile', 'zip', '/home/alterego/Documents/proyectos/genesis/core/static/core/img')
        # file = open("/home/alterego/Documents/proyectos/genesis/core/static/core/img/logo.png", "rwt")
        # response = HttpResponse(file.read(), content_type="application/pdf")
        # response['Content-Disposition'] = 'attachement; filename=%s' % file
        return render(request, 'proyectos/download.html')     

class ListaArbolView(DetailView):
    model = Proyecto
    template_name = "proyectos/arbol_proyectos.html"

    def get_context_data(self, **kwargs):
        context = super(ListaArbolView, self).get_context_data(**kwargs)
        proyecto = (self.object)
        listaproyecto = views.ListaCrear(proyecto.id)
        context['listaproyectos'] = listaproyecto
        return context        