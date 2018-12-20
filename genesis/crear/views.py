from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from proyectos.models import Proyecto
from aplicaciones.models import Aplicacion
from modelos.models import Modelo
from propiedades.models import Propiedad
from reglas.models import Regla
from crear.models import Crear
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from .forms import CrearForm
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect

import os,shutil
import string

class CrearView(TemplateView):
    template_name = "crear/home.html"

    def get_context_data(self,**kwargs):
        context = super(CrearView, self).get_context_data(**kwargs)
        proyecto = Proyecto.objects.get(id=self.request.GET['proyecto_id'])
        context['nombre'] = proyecto.nombre
        context['descripcion'] = proyecto.descripcion
        context['id'] = proyecto.id

        return context

class CrearProyectoView(FormView):
    template_name = "crear/CrearProyecto.html"
    form_class = CrearForm
    model = Crear

    def get_success_url(self):
        return reverse_lazy('crear:proyecto') + '?proyecto_id='+ self.request.GET['proyecto_id']

    def get_context_data(self,**kwargs):
        context = super(CrearProyectoView, self).get_context_data(**kwargs)
        context['lista'] = ListaCrear(self.request.GET['proyecto_id'])
        context['proyecto_id'] = self.request.GET['proyecto_id']
        return context      

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        proyecto = Proyecto.objects.get(id = request.GET['proyecto_id'])

        CrearProyecto(proyecto)
        return HttpResponseRedirect(self.get_success_url())

class CrearAplicacionesView(FormView):
    template_name = "crear/CrearAplicaciones.html"
    form_class = CrearForm
    model = Crear

    def get_success_url(self):
        return reverse_lazy('crear:proyecto') + '?proyecto_id='+ self.request.GET['proyecto_id']

    def get_context_data(self,**kwargs):
        context = super(CrearAplicacionesView, self).get_context_data(**kwargs)
        context['lista'] = ListaCrear(self.request.GET['proyecto_id'])
        context['proyecto_id'] = self.request.GET['proyecto_id']
        return context      

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        proyecto = Proyecto.objects.get(id = request.GET['proyecto_id'])

        CrearAplicaciones(proyecto)
        return HttpResponseRedirect(self.get_success_url())

class CrearDirectoriosView(FormView):
    template_name = "crear/CrearDirectorios.html"
    form_class = CrearForm
    model = Crear

    def get_success_url(self):
        return reverse_lazy('crear:proyecto') + '?proyecto_id='+ self.request.GET['proyecto_id']

    def get_context_data(self,**kwargs):
        context = super(CrearDirectoriosView, self).get_context_data(**kwargs)
        context['proyecto_id'] = self.request.GET['proyecto_id']
        context['lista'] = ListaCrear(self.request.GET['proyecto_id'])
        return context      

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        proyecto = Proyecto.objects.get(id = request.GET['proyecto_id'])

        CrearDirectoriosProyecto(proyecto)
        CrearArchivosProyectos(proyecto)

        return HttpResponseRedirect(self.get_success_url())

class CrearModelosView(FormView):
    template_name = "crear/CrearModelos.html"
    form_class = CrearForm
    model = Crear

    def get_success_url(self):
        return reverse_lazy('crear:proyecto') + '?proyecto_id='+ self.request.GET['proyecto_id']

    def get_context_data(self,**kwargs):
        context = super(CrearModelosView, self).get_context_data(**kwargs)
        context['proyecto_id'] = self.request.GET['proyecto_id']
        context['lista'] = ListaCrear(self.request.GET['proyecto_id'])
        return context      

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        proyecto = Proyecto.objects.get(id = request.GET['proyecto_id'])

        for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):
            CrearModelos(proyecto,aplicacion)

        # crear la urls de core

        cd = os.getcwd() + '/core/static/core/text_files'
        fo = open(cd + '/core_urls.py', "r+")
        stri = fo.read()

        # cd = os.getcwd() + '/' + proyecto.nombre + '/core'
        cd = proyecto.directorio + '/' + proyecto.nombre + '/core'
        try:
            os.remove( cd + "/urls.py")
        except:
            print('no hay archivo ' +cd)

        fd = os.open(cd + '/urls.py',os.O_CREAT)
        with os.fdopen(os.open(cd + '/urls.py',os.O_CREAT | os.O_RDWR ),'w') as fd:  
            fd.write(stri)
        fd.close() 

        # crear el view para core

        cd = os.getcwd() + '/core/static/core/text_files'
        fo = open(cd + '/core_view.py', "r+")
        stri = fo.read()

        cd = proyecto.directorio + '/' + proyecto.nombre + '/core'
        try:
            os.remove( cd + "/views.py")
        except:
            print('no hay archivo ' + cd)

        fd = os.open(cd + '/views.py',os.O_CREAT)
        with os.fdopen(os.open(cd + '/views.py',os.O_CREAT | os.O_RDWR ),'w') as fd:  
            fd.write(stri)
        fd.close() 

        return HttpResponseRedirect(self.get_success_url())

class CrearVistasView(FormView):
    template_name = "crear/CrearVistas.html"
    form_class = CrearForm
    model = Crear

    def get_success_url(self):
        return reverse_lazy('crear:proyecto') + '?proyecto_id='+ self.request.GET['proyecto_id']

    def get_context_data(self,**kwargs):
        context = super(CrearVistasView, self).get_context_data(**kwargs)
        context['proyecto_id'] = self.request.GET['proyecto_id']
        context['lista'] = ListaCrear(self.request.GET['proyecto_id'])
        return context      

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        proyecto = Proyecto.objects.get(id = request.GET['proyecto_id'])

        for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):
            CrearVistas(proyecto,aplicacion)

        return HttpResponseRedirect(self.get_success_url())

class CrearFormsView(FormView):
    template_name = "crear/CrearForms.html"
    form_class = CrearForm
    model = Crear

    def get_success_url(self):
        return reverse_lazy('crear:proyecto') + '?proyecto_id='+ self.request.GET['proyecto_id']

    def get_context_data(self,**kwargs):
        context = super(CrearFormsView, self).get_context_data(**kwargs)
        context['proyecto_id'] = self.request.GET['proyecto_id']
        context['lista'] = ListaCrear(self.request.GET['proyecto_id'])
        return context      

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        proyecto = Proyecto.objects.get(id = request.GET['proyecto_id'])

        for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):
            CrearForms(proyecto,aplicacion)

        return HttpResponseRedirect(self.get_success_url())

class CrearUrlsView(FormView):
    template_name = "crear/CrearUrls.html"
    form_class = CrearForm
    model = Crear

    def get_success_url(self):
        return reverse_lazy('crear:proyecto') + '?proyecto_id='+ self.request.GET['proyecto_id']

    def get_context_data(self,**kwargs):
        context = super(CrearUrlsView, self).get_context_data(**kwargs)
        context['proyecto_id'] = self.request.GET['proyecto_id']
        context['lista'] = ListaCrear(self.request.GET['proyecto_id'])
        return context      

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        proyecto = Proyecto.objects.get(id = request.GET['proyecto_id'])

        strlfp = ''
        strlpp = ''
        for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):
            CrearUrls(proyecto,aplicacion)

            # Crear las urls del proyecto
            flgCrear = False
            for modelo in Modelo.objects.filter(aplicacion=aplicacion):
                if Propiedad.objects.filter(modelo=modelo).count() > 0:
                    flgCrear = True

            if flgCrear or aplicacion.nombre == 'core':
                # Preparar los patterns para urls del proyecto
                strlfp += 'from @aplicacion.urls import @aplicacion_patterns' + '\n'
                if aplicacion.nombre == 'core':
                    strlpp += '\tpath(' + "'" + "'" + ',include(@aplicacion_patterns)),' + '\n'
                else:    
                    strlpp += '\tpath(' + "'" + '@aplicacion/' + "'" + ',include(@aplicacion_patterns)),' + '\n'

                strlfp = strlfp.replace('@aplicacion', aplicacion.nombre)
                strlpp = strlpp.replace('@aplicacion', aplicacion.nombre)


        # leer archivo urls.py del proyecto
        cd = os.getcwd() + '/core/static/core/text_files'

        fo = open(cd + '/urls_proyecto.py', "r+")
        stri = fo.read()

        stri = stri.replace('@listafrompatterns', strlfp)
        stri = stri.replace('@listapathpatterns', strlpp)

        cd = proyecto.directorio + '/' + proyecto.nombre + '/' + proyecto.nombre

        try:
            os.remove( cd + "/urls.py")
        except:
            print('no hay archivo')

        fd = os.open(cd + '/urls.py',os.O_CREAT)
        with os.fdopen(os.open(cd + '/urls.py',os.O_CREAT | os.O_RDWR ),'w') as fd:  
            fd.write(stri)
        fd.close() 

        return HttpResponseRedirect(self.get_success_url())

class CrearTemplatesView(FormView):
    template_name = "crear/CrearTemplates.html"
    form_class = CrearForm
    model = Crear

    def get_success_url(self):
        return reverse_lazy('crear:proyecto') + '?proyecto_id='+ self.request.GET['proyecto_id']

    def get_context_data(self,**kwargs):
        context = super(CrearTemplatesView, self).get_context_data(**kwargs)
        context['proyecto_id'] = self.request.GET['proyecto_id']
        context['lista'] = ListaCrear(self.request.GET['proyecto_id'])
        return context      

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        proyecto = Proyecto.objects.get(id = request.GET['proyecto_id'])

        # for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):
        # CrearTemplates(proyecto)
        CrearTemplatesAlLado(proyecto)

        return HttpResponseRedirect(self.get_success_url())

def CrearTemplates(proyecto):
    cd = os.getcwd() + '/core/static/core/text_files'

    fo = open(cd + '/base.html', "r+")
    stri = fo.read()
    # el archivo Base.html

    # crear archivo base.html de core
    # cd = os.getcwd() + '/' + proyecto.nombre + '/core/templates/core'
    cd = proyecto.directorio + '/' + proyecto.nombre + '/core/templates/core'

    try:
            os.remove( cd + "/base.html")
    except:
        print('no hay archivo')

    try:

        #copiar el archivo de logo del proyecto a static/core/img
        try:
            img = proyecto.avatar.url.split('/')
            imagen = ''
            for i in img:
                imagen = i
            origen = os.getcwd() + '/media/proyectos/' + imagen
            destino = proyecto.directorio + '/' + proyecto.nombre + '/core/static/core/img/logo.png' 

            if os.path.exists(origen):
                with open(origen, 'rb') as forigen:
                    with open(destino, 'wb') as fdestino:
                        shutil.copyfileobj(forigen, fdestino)
        except:
            print('no se copio la imagen')

        # reemplazar el nombre del logo y el titulo del proyecto
        imagen= ''
        img = proyecto.avatar.url.split('/')
        for i in img:
            imagen = i
        stri = stri.replace('@logo', imagen)

        # columnas izquierda derecha encabezado
        stri = stri.replace('@columnasizquierdaencabezado', proyecto.columnasizquierdaencabezado)
        stri = stri.replace('@columnasderechaencabezado', proyecto.columnasderechaencabezado)

        # logo
        stri = stri.replace('@altologo', proyecto.altopixeles)
        stri = stri.replace('@anchologo', proyecto.anchopixeles)
        stri = stri.replace('@numerocolumnas', proyecto.numerocolumnas)

        strJusti=''
        if proyecto.justificacion == 'i':
            strJusti = 'text-left'
        if proyecto.justificacion == 'd':
            strJusti = 'text-right'
        if proyecto.justificacion == 'c':
            strJusti = 'text-center'

        stri = stri.replace('@justificacion', strJusti)

        # TITULO
        stri = stri.replace('@titulo', proyecto.textotitulo)

        # font titulo
        strFont = proyecto.fonttitulo.split(',')
        stri = stri.replace('@fonttitulo', strFont[0])
        stri = stri.replace('@sizetitulo', strFont[1])
        stri = stri.replace('@boldtitulo', strFont[2])
        stri = stri.replace('@colortitulo', proyecto.colortitulo)
        stri = stri.replace('@numerocolumnastitulo', proyecto.numerocolumnastitulo)

        if proyecto.justificaciontitulo == 'i':
            strJusti = 'text-left'
        if proyecto.justificaciontitulo == 'd':
            strJusti = 'text-right'
        if proyecto.justificaciontitulo == 'c':
            strJusti = 'text-center'
        stri = stri.replace('@justificaciontitulo', strJusti)



    except:
        print('No se reemplazo el logo')

    fd = os.open(cd + '/base.html',os.O_CREAT)
    with os.fdopen(os.open(cd + '/base.html',os.O_CREAT | os.O_RDWR ),'w') as fd:  
        fd.write(stri)
    fd.close() 

    #crear el archivo menu_core.html en includes

    cd = os.getcwd() + '/core/static/core/text_files'

    fo = open(cd + '/menu_core.html', "r+")
    stri = fo.read()

    stroa = ''
    for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):

        # Grabar el modelo si su aplicacion tiene modelos con propiedades
        flgCrear = False
        for modelo in Modelo.objects.filter(aplicacion=aplicacion):
            if Propiedad.objects.filter(modelo=modelo).count() > 0:
                flgCrear = True

        # ver si dentro de la aplicacion existe un modelo con padre='nada'
        flgPadre = False
        for modelo in Modelo.objects.filter(aplicacion=aplicacion):
            if modelo.padre == 'nada':
                flgPadre= True

        if flgCrear and flgPadre and aplicacion.nombre != 'core':
            stroa += '\t\t\t\t\t\t<ul class="navbar-nav ">' + '\n'
            stroa += '\t\t\t\t\t\t\t<li class="nav-item  px-lg-4" >' + '\n'
            stroa += '\t\t\t\t\t\t\t\t<a  style="color:@colormenu;font-family: @fontmenu; font-size: @sizemenupt" class="nav-link text-capitalize text-expanded text-white" href="{%  url ' + "'" + '@aplicacion:home' + "'" + '%}">@aplicacion</a>' + '\n'
            stroa += '\t\t\t\t\t\t\t</li>' + '\n'
            stroa += '\t\t\t\t\t\t</ul>' + '\n'

            stroa = stroa.replace('@aplicacion', aplicacion.nombre)

    stri = stri.replace('@aplicaciones', stroa)
    stri = stri.replace('@proyecto', proyecto.nombre)
    
    # crear archivo menu_core.html de core
    # cd = os.getcwd() + '/' + proyecto.nombre + '/core/templates/core/includes'
    cd = proyecto.directorio + '/' + proyecto.nombre + '/core/templates/core/includes'

    try:
            os.remove( cd + "/menu_core.html")
    except:
        print('no hay archivo')

    fd = os.open(cd + '/menu_core.html',os.O_CREAT)
    with os.fdopen(os.open(cd + '/menu_core.html',os.O_CREAT | os.O_RDWR ),'w') as fd:  
        fd.write(stri)
    fd.close() 

    # archivo home.html de core    
    cd = os.getcwd() + '/core/static/core/text_files'

    fo = open(cd + '/home_core.html', "r+")
    stri = fo.read()

    # crear archivo home.html de core
    # cd = os.getcwd() + '/' + proyecto.nombre + '/core/templates/core'
    cd = proyecto.directorio + '/' + proyecto.nombre + '/core/templates/core'

    try:
            os.remove( cd + "/home.html")
    except:
        print('no hay archivo')

    fd = os.open(cd + '/home.html',os.O_CREAT)
    with os.fdopen(os.open(cd + '/home.html',os.O_CREAT | os.O_RDWR ),'w') as fd:  
        fd.write(stri)
    fd.close() 

    # crear el home.html por aplicacion
    cd = os.getcwd() + '/core/static/core/text_files'

    fo = open(cd + '/home_aplicacion.html', "r+")
    stri = fo.read()


    for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):

        # Grabar el modelo si su aplicacion tiene modelos con propiedades
        flgCrear = False
        for modelo in Modelo.objects.filter(aplicacion=aplicacion):
            if Propiedad.objects.filter(modelo=modelo).count() > 0:
                flgCrear = True

        if flgCrear and aplicacion.nombre != 'core':
            cd = proyecto.directorio + '/' + proyecto.nombre + '/' + aplicacion.nombre + '/templates/' + '/' + aplicacion.nombre

            try:
                    os.remove( cd + "/home.html")
            except:
                print('no hay archivo')

            strt = stri.replace('@aplicacion', aplicacion.nombre)

            fd = os.open(cd + '/home.html',os.O_CREAT)
            with os.fdopen(os.open(cd + '/home.html',os.O_CREAT | os.O_RDWR ),'w') as fd:  
                fd.write(strt)
            fd.close() 

    # Crear el menu para cada aplicacion
    cd = os.getcwd() + '/core/static/core/text_files'

    fo = open(cd + '/menu_aplicacion.html', "r+")
    stri = fo.read()
    strt = ''

    for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):

        # Grabar el modelo si su aplicacion tiene modelos con propiedades
        flgCrear = False
        for modelo in Modelo.objects.filter(aplicacion=aplicacion):
            if Propiedad.objects.filter(modelo=modelo).count() > 0:
                flgCrear = True

        if flgCrear:                
            if aplicacion.nombre != 'core':
                strlm = ''
                strt = stri

                # Grabar el modelo si su aplicacion tiene modelos con propiedades
                for modelo in Modelo.objects.filter(aplicacion=aplicacion):
                    if Propiedad.objects.filter(modelo=modelo).count() > 0:
                        if modelo.padre == 'nada':
                            strlm += '\t\t\t\t\t\t<ul class="navbar-nav ">' + '\n'
                            strlm += '\t\t\t\t\t\t\t<li class="nav-item  px-lg-4" >' + '\n'
                            strlm += '\t\t\t\t\t\t\t\t<a class="nav-link text-uppercase text-expanded text-white" href="{%  url ' + "'" + '@aplicacion:listar_@modelom' + "'" + ' %}">@modelo</a>' + '\n'
                            strlm += '\t\t\t\t\t\t\t</li>' + '\n'
                            strlm += '\t\t\t\t\t\t</ul>' + '\n'
                            strlm = strlm.replace('@modelom', modelo.nombre.lower())
                            strlm = strlm.replace('@modelo', string.capwords(modelo.nombre))
                            strlm = strlm.replace('@aplicacion', aplicacion.nombre)
                
                strt = strt.replace('@listamodelos', strlm)
                strt = strt.replace('@aplicacion', aplicacion.nombre)
                
                # cd = os.getcwd() + '/' + proyecto.nombre + '/' + 'core/templates/core/includes'
                cd = proyecto.directorio + '/' + proyecto.nombre + '/' + 'core/templates/core/includes'

                try:
                    os.remove( cd + '/menu_' + aplicacion.nombre + '.html')
                except:
                    print('no hay archivo')

                fd = os.open(cd + '/menu_' + aplicacion.nombre + '.html',os.O_CREAT)
                with os.fdopen(os.open(cd + '/menu_' + aplicacion.nombre + '.html',os.O_CREAT | os.O_RDWR ),'w') as fd:  
                    fd.write(strt)
                fd.close() 

    # Crear el template listar para cada modelo
    cd = os.getcwd() + '/core/static/core/text_files'

    fo = open(cd + '/modelo_listar.html', "r+")
    stri = fo.read()
    strt = ''

    for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):

        # Grabar el modelo si su aplicacion tiene modelos con propiedades
        flgCrear = False
        for modelo in Modelo.objects.filter(aplicacion=aplicacion):
            if Propiedad.objects.filter(modelo=modelo).count() > 0:
                flgCrear = True

        if flgCrear:                
            if aplicacion.nombre != 'core':

                # Grabar el modelo si su aplicacion tiene modelos con propiedades
                for modelo in Modelo.objects.filter(aplicacion=aplicacion):
                    strlr = ''
                    strlt = ''
                    strt = stri

                    if modelo.padre == 'nada':
                        for propiedad in Propiedad.objects.filter(modelo=modelo):
                            if propiedad.enlista:
                                strlt += '\t\t<div class="col-@numerocolumnas">' + '\n'
                                strlt += '\t\t\t<b>@nombrepropiedadM</b>' + '\n'
                                strlt += '\t\t</div>' + '\n'

                                if propiedad.tipo != 'p':
                                    strlr += '\t\t\t<div class="col-@numerocolumnas">' + '\n'
                                    strlr += '\t\t\t\t{{objeto.@nombrepropiedad@formatofecha}}' + '\n'
                                    strlr += '\t\t\t</div>' + '\n'
                                else:
                                    strlr += '\t\t\t<div class="col-@numerocolumnas">' + '\n'
                                    strlr += '\t\t\t\t{% if objeto.@nombrepropiedad %}' + '\n'
                                    strlr += '\t\t\t\t\t<img src="{{objeto.@nombrepropiedad.url}}" width="20px" height="20px" alt="">' + '\n'
                                    strlr += '\t\t\t\t{% endif %}' + '\n'
                                    strlr += '\t\t\t</div>' + '\n'
                                    
                                strlr = strlr.replace('@formatofecha', propiedad.formatofecha)
                                strlt = strlt.replace('@numerocolumnas', str(propiedad.numerocolumnas))
                                strlr = strlr.replace('@numerocolumnas', str(propiedad.numerocolumnas))
                                strlt = strlt.replace('@nombrepropiedadM', propiedad.nombre.upper())
                                strlr = strlr.replace('@nombrepropiedad', propiedad.nombre)
                
                        strt = strt.replace('@listatitulos', strlt)
                        strt = strt.replace('@listaregistros', strlr)
                        strt = strt.replace('@aplicacion', aplicacion.nombre)
                        strt = strt.replace('@modelom', modelo.nombre.lower())
                        strt = strt.replace('@modeloM', modelo.nombre.upper())
                        strt = strt.replace('@modelo', string.capwords(modelo.nombre))
                        
                        # cd = os.getcwd() + '/' + proyecto.nombre + '/' + aplicacion.nombre + '/' + 'templates/' + aplicacion.nombre 
                        cd = proyecto.directorio + '/' + proyecto.nombre + '/' + aplicacion.nombre + '/' + 'templates/' + aplicacion.nombre 

                        try:
                            os.remove( cd + '/' + modelo.nombre + '_list.html')
                        except:
                            print('no hay archivo')

                        fd = os.open(cd + '/' + modelo.nombre + '_list.html',os.O_CREAT)
                        with os.fdopen(os.open(cd + '/' + modelo.nombre + '_list.html',os.O_CREAT | os.O_RDWR ),'w') as fd:  
                            fd.write(strt)
                        fd.close() 

    # Crear el template form para cada modelo
    cd = os.getcwd() + '/core/static/core/text_files'

    fo = open(cd + '/modelo_form.html', "r+")
    stri = fo.read()
    strt = ''

    for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):

        # Grabar el modelo si su aplicacion tiene modelos con propiedades
        flgCrear = False
        for modelo in Modelo.objects.filter(aplicacion=aplicacion):
            if Propiedad.objects.filter(modelo=modelo).count() > 0:
                flgCrear = True

        if flgCrear and aplicacion.nombre!= 'core':                

            for modelo in Modelo.objects.filter(aplicacion=aplicacion):
                strt = stri            
                strt = strt.replace('@aplicacion', aplicacion.nombre)
                strt = strt.replace('@modelom', modelo.nombre.lower())
                strt = strt.replace('@modeloM', modelo.nombre.upper())
                strt = strt.replace('@modelo', string.capwords(modelo.nombre))
                
                # codigo para la opcion referencia form
                stra = ''

                if modelo.padre == 'nada':
                    stra += 'NUEVO @modeloM' + '\n'
                else:    
                    modelo_padre = Modelo.objects.get(nombre=modelo.padre, proyecto=proyecto)
                    if modelo_padre.padre != 'nada': # el modelo es nieto
                        modelo_abuelo = Modelo.objects.get(nombre=modelo_padre.padre , proyecto=proyecto)

                        # stra += '<div class="row font_encabezado mb-3">' + '\n'
                        stra += '<div class="col">' + '\n'
                        stra += '<div class="" style="float: left;">NUEVO @modeloM&nbsp&nbsp</div>' + '\n'
                        stra += '<div class=""><a href="{% url ' + "'" + '@aplicacionpadrem:editar_@modelopadrem' + "'" + ' @modelopadrem_id %}?@modeloabuelom_id={{@modeloabuelom_id}}">(Volver)</a></div>' + '\n'
                        stra += '</div>' + '\n'
                        # stra += '</div>' + '\n'

                        # stra =  modelo.nombre.upper() + ': <b>{{nombre}}</b>&nbsp&nbsp<a href="{% url ' + "'" + '@aplicacionpadrem:editar_@modelopadrem' + "'" + ' @modelopadrem_id %}?@modeloabuelom_id={{@modeloabuelom_id}}">(Volver)</a>'
                        stra = stra.replace('@modeloabuelom', modelo_abuelo.nombre.lower())        
                    else: # el modelo es hijo
                        # stra += '<div class="row font_encabezado mb-3 ">' + '\n'
                        stra += '<div class="col">' + '\n'
                        stra += '<div class="" style="float: left">NUEVO @modeloM</div>' + '\n'
                        stra += '<div class="" >&nbsp&nbsp<a href="{% url ' + "'" + '@aplicacionpadrem:editar_@modelopadrem' + "'" + ' @modelopadrem_id %}">(Volver)</a></div>' + '\n'
                        stra += '</div>' + '\n'
                        # stra += '</div>' + '\n'

                        # stra = modelo.nombre + ': <b>{{nombre}}</b>&nbsp&nbsp<a href="{% url ' + "'" + '@aplicacionpadrem:editar_@modelopadrem' + "'" + ' @modelopadrem_id %}">(Volver)</a>'
                    stra = stra.replace('@aplicacionpadrem', Aplicacion.objects.get(id=modelo_padre.aplicacion.id).nombre.lower())        
                    stra = stra.replace('@modelopadrem', modelo_padre.nombre.lower())        

                stra = stra.replace('@modeloM', modelo.nombre.upper())        

                strt = strt.replace('@referenciaform', stra)

                # cd = os.getcwd() + '/' + proyecto.nombre + '/' + aplicacion.nombre + '/' + 'templates/' + aplicacion.nombre 
                cd = proyecto.directorio + '/' + proyecto.nombre + '/' + aplicacion.nombre + '/' + 'templates/' + aplicacion.nombre 

                try:
                    os.remove( cd + '/' + modelo.nombre + '_form.html')
                except:
                    print('no hay archivo')

                fd = os.open(cd + '/' + modelo.nombre + '_form.html',os.O_CREAT)
                with os.fdopen(os.open(cd + '/' + modelo.nombre + '_form.html',os.O_CREAT | os.O_RDWR ),'w') as fd:  
                    fd.write(strt)
                fd.close() 

    # Crear el template update para cada modelo
    cd = os.getcwd() + '/core/static/core/text_files'

    fo = open(cd + '/modelo_update.html', "r+")
    stri = fo.read()
    strt = ''

    for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):

        # Grabar el modelo si su aplicacion tiene modelos con propiedades
        flgCrear = False
        for modelo in Modelo.objects.filter(aplicacion=aplicacion):
            if Propiedad.objects.filter(modelo=modelo).count() > 0:
                flgCrear = True

        if flgCrear and aplicacion.nombre!= 'core':                

            for modelo in Modelo.objects.filter(aplicacion=aplicacion):

                strt = stri            
                strt = strt.replace('@aplicacion', aplicacion.nombre)
                strt = strt.replace('@modelom', modelo.nombre.lower())
                strt = strt.replace('@modeloM', modelo.nombre.upper())
                strt = strt.replace('@modelo', string.capwords(modelo.nombre))
                
                for propiedad in Propiedad.objects.filter(modelo=modelo):
                    if propiedad.enlista:
                        strt = strt.replace('@nombre', modelo.nombre + '.' + propiedad.nombre)
                        break

                # codigo para la referencia del form
                stra = ''

                if modelo.padre =='nada': # modelo padre
                    stra = '<div class="col">@modeloM: {{nombre}}</div>' + '\n'
                else:
                    modelo_padre = Modelo.objects.get(nombre=modelo.padre , proyecto=proyecto)
                    if modelo_padre.padre != 'nada': # el modelo es nieto
                        modelo_abuelo = Modelo.objects.get(nombre=modelo_padre.padre , proyecto=proyecto)
                        stra += '<div class="col">' + '\n'
                        stra += '<div class="" style="float: left">@modeloM:&nbsp&nbsp</div>' +'\n'
                        stra += '<div class="" style="float: left;"><b>{{nombre}}</b>&nbsp&nbsp</div>' + '\n'
                        stra += '<div class="" style="float: left;"><a href="{% url ' + "'" + '@aplicacionpadrem:editar_@modelopadrem' + "'" + ' @modelopadrem_id %}?@modeloabuelom_id={{@modeloabuelom_id}}">(Volver)</a></div>' + '\n'
                        stra += '</div>' + '\n'
                        # stra =  modelo.nombre.upper() + ': <b>{{nombre}}</b>&nbsp&nbsp<a href="{% url ' + "'" + '@aplicacionpadrem:editar_@modelopadrem' + "'" + ' @modelopadrem_id %}?@modeloabuelom_id={{@modeloabuelom_id}}">(Volver)</a>'
                        stra = stra.replace('@modeloabuelom', modelo_abuelo.nombre.lower())        
                    else: # el modelo es hijo
                        stra += '<div class="col text-center">' + '\n'
                        stra += '<div class="" style="float: left;">@modeloM:&nbsp&nbsp</div>&nbsp' + '\n'
                        stra += '<div class="" style="float: left"><b>{{nombre}}&nbsp&nbsp</b></div>' + '\n'
                        stra += '<div class="" style="float: left"><a href="{% url ' + "'" + '@aplicacionpadrem:editar_@modelopadrem' + "'" + ' @modelopadrem_id %}">(Volver)</a></div>' + '\n'
                        stra += '</div>' + '\n'

                            # stra = modelo.nombre + ': <b>{{nombre}}</b>&nbsp&nbsp<a href="{% url ' + "'" + '@aplicacionpadrem:editar_@modelopadrem' + "'" + ' @modelopadrem_id %}">(Volver)</a>'
                    stra = stra.replace('@aplicacionpadrem', Aplicacion.objects.get(id=modelo_padre.aplicacion.id).nombre.lower())        
                    stra = stra.replace('@modelopadrem', modelo_padre.nombre.lower())        

                stra = stra.replace('@modeloM', modelo.nombre.upper())        

                strt = strt.replace('@referenciaform', stra)


                #lista de modelos hijos
                strh = ''
                for modelohijo in Modelo.objects.filter(padre=modelo.nombre , proyecto=proyecto):
                    strlh = '\t\t\t<div class="row mt-3">' + '\n'
                    strlh += '\t\t\t\t<div class="col">' + '\n'
                    strlh += '\t\t\t\t\t<!-- hijos -->' + '\n'
                    strlh += '\t\t\t\t\t<div class="row font_lista borde_inferior font-weight-bold mt-3">' + '\n'
                    strlh += '@columnashijo' + '\n'
                    strlh += '\t\t\t\t\t</div>' + '\n'
                    strlh += '\t\t\t\t\t{% for objeto in lista@hijo %}' + '\n'
                    strlh += '\t\t\t\t\t\t<div class="row font_lista ">' + '\n'
                    strlh += '@listaregistroshijo'
                    strlh += '\t\t\t\t\t\t\t<div class="col-1 ml-0">' + '\n'
                    strlh += '\t\t\t\t\t\t\t\t@editahijo'
                    strlh += '\t\t\t\t\t\t\t</div>' + '\n'
                    strlh += '\t\t\t\t\t\t\t<div class="col-1">' + '\n'
                    strlh += '\t\t\t\t\t\t\t\t@borrahijo'
                    strlh += '\t\t\t\t\t\t\t</div>' + '\n'
                    strlh += '\t\t\t\t\t\t</div>' + '\n'
                    strlh += '\t\t\t\t\t{% endfor %}' + '\n'
                    strlh += '\t\t\t\t\t<div class="row mt-3 borde_superior font_lista">' + '\n'
                    strlh += '\t\t\t\t\t\t<div class="col font-weight-bold">' + '\n'
                    strlh += '\t\t\t\t\t\t\t<a href="{% url ' + "'" + '@aplicacionhijo:crear_@hijo' + "'" + '%}?@modelopadrem_id={{ @modelopadrem.id }}">Nuevo registro @hijo</a>' + '\n'
                    strlh += '\t\t\t\t\t\t</div>' + '\n'
                    strlh += '\t\t\t\t\t</div>' + '\n'
                    strlh += '\t\t\t\t</div>' + '\n'
                    strlh += '\t\t\t</div>' + '\n'
                    strlrh = ''
                    strlth = ''

                    # lista hijos
                    for propiedadhijo in Propiedad.objects.filter(modelo=modelohijo):
                        if propiedadhijo.enlista:
                            strlth += '\t\t\t\t\t\t<div class="col-3 ">' + '\n'
                            strlth += '\t\t\t\t\t\t\t' + propiedadhijo.nombre + '\n'
                            strlth += '\t\t\t\t\t\t</div>' + '\n'
                            strlrh += '\t\t\t\t\t\t\t<div class="col-3 ">' + '\n'
                            strlrh += '\t\t\t\t\t\t\t\t{{objeto.' + propiedadhijo.nombre + propiedadhijo.formatofecha + '}}' + '\n'
                            strlrh += '\t\t\t\t\t\t</div>' + '\n'

                    # editar y borrar hijos
                    streh = ''
                    strbh = ''
                    if modelohijo.padre != 'nada': # modelo hijo o nieto
                        modelo_padre = Modelo.objects.get(nombre=modelohijo.padre , proyecto=proyecto)
                        if modelo_padre.padre != 'nada': # modelo nieto
                            modelo_abuelo = Modelo.objects.get(nombre=modelo_padre.padre , proyecto=proyecto)
                            streh += '<a href="{% url ' + "'" + '@aplicacionhijo:editar_@hijo' + "'" + ' objeto.id %}?@modelopadrem_id={{ @modelopadrem_id }}&@modeloabuelom_id={{@modeloabuelom_id}}">Editar</a>' + '\n'
                            strbh += '<a href="{% url ' + "'" + '@aplicacionhijo:borrar_@hijo' + "'" + ' objeto.id %}?@modelopadrem_id={{ @modelopadrem_id }}&@modeloabuelom_id={{@modeloabuelom_id}}">Borrar</a>' + '\n'
                            streh = streh.replace('@modeloabuelom', modelo_abuelo.nombre.lower())
                            strbh = strbh.replace('@modeloabuelom', modelo_abuelo.nombre.lower())
                        else: # modelo hijo
                            streh += '<a href="{% url ' + "'" + '@aplicacionhijo:editar_@hijo' + "'" + ' objeto.id %}?@modelopadrem_id={{ @modelopadrem_id }}">Editar</a>' + '\n'
                            strbh += '<a href="{% url ' + "'" + '@aplicacionhijo:borrar_@hijo' + "'" + ' objeto.id %}?@modelopadrem_id={{ @modelopadrem_id }}">Borrar</a>' + '\n'
                        streh = streh.replace('@modelopadrem', modelo_padre.nombre.lower())
                        strbh = strbh.replace('@modelopadrem', modelo_padre.nombre.lower())
                    else: # modelo sin padre
                        streh += '<a href="{% url ' + "'" + '@aplicacionhijo:editar_@hijo' + "'" + ' objeto.id %}?@modelom_id={{ @modelom.id }}">Editar</a>' + '\n'
                        strbh += '<a href="{% url ' + "'" + '@aplicacionhijo:borrar_@hijo' + "'" + ' objeto.id %}?@modelom_id={{ @modelom.id }}">Borrar</a>' + '\n'
                        streh = streh.replace('@modelom', modelohijo.nombre.lower())
                        strbh = strbh.replace('@modelom', modelohijo.nombre.lower())
                        
                    strlh = strlh.replace('@editahijo', streh)
                    strlh = strlh.replace('@borrahijo', strbh)
                    strlh = strlh.replace('@modelopadrem', modelo.nombre.lower())
                    strlh = strlh.replace('@modelohijom', modelohijo.nombre.lower())
                    strlh = strlh.replace('@hijo', modelohijo.nombre)
                    strlh = strlh.replace('@aplicacionhijo', modelohijo.aplicacion.nombre.lower())
                    strlh = strlh.replace('@columnashijo', strlth)
                    strlh = strlh.replace('@listaregistroshijo', strlrh)

                    strh += strlh
                    
                strt = strt.replace('@listahijos', strh)
                
                # if modelo.padre != 'nada':

                # cd = os.getcwd() + '/' + proyecto.nombre + '/' + aplicacion.nombre + '/' + 'templates/' + aplicacion.nombre 
                cd = proyecto.directorio + '/' + proyecto.nombre + '/' + aplicacion.nombre + '/' + 'templates/' + aplicacion.nombre 

                try:
                    os.remove( cd + '/' + modelo.nombre + '_update_form.html')
                except:
                    print('no hay archivo')
                fd = os.open(cd + '/' + modelo.nombre + '_update_form.html',os.O_CREAT)
                with os.fdopen(os.open(cd + '/' + modelo.nombre + '_update_form.html',os.O_CREAT | os.O_RDWR ),'w') as fd:  
                    fd.write(strt)
                fd.close() 

    # Crear el template confirm delete para cada modelo
    cd = os.getcwd() + '/core/static/core/text_files'

    fo = open(cd + '/modelo_confirm_delete.html', "r+")
    stri = fo.read()
    strt = ''

    for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):

        # Grabar el modelo si su aplicacion tiene modelos con propiedades
        flgCrear = False
        for modelo in Modelo.objects.filter(aplicacion=aplicacion):
            if Propiedad.objects.filter(modelo=modelo).count() > 0:
                flgCrear = True

        if flgCrear and aplicacion.nombre!= 'core':                

            for modelo in Modelo.objects.filter(aplicacion=aplicacion):
                strt = stri            

                # definir la vista de retorno
                if modelo.padre =='nada':
                    strt = strt.replace('@vistadespues', 'listar_@modelom')
                else:
                    strt = strt.replace('@vistadespues', 'listar_@modelom')


                # cancelar el borrado
                strcb = ''
                if modelo.padre != 'nada': # modelo hijo o nieto
                    modelo_padre = Modelo.objects.get(nombre=modelo.padre , proyecto=proyecto)
                    if modelo_padre.padre != 'nada': # modelo nieto
                        modelo_abuelo = Modelo.objects.get(nombre=modelo_padre.padre , proyecto=proyecto)
                        strcb = '<a href="{% url ' + "'" + '@aplicacionpadre:editar_@modelopadrem' + "'" + ' @modelopadrem_id %}?@modeloabuelom_id={{@modeloabuelom_id}}">Cancelar</a>'
                        strcb = strcb.replace('@modeloabuelom', modelo_abuelo.nombre)
                    else: # modelo hijo
                        strcb = '<a href="{% url ' + "'" + '@aplicacionpadre:editar_@modelopadrem' + "'" + ' @modelopadrem_id %}">Cancelar</a>'
                    strcb = strcb.replace('@aplicacionpadre', Aplicacion.objects.get(id=modelo_padre.aplicacion.id).nombre)
                    strcb = strcb.replace('@modelopadrem', modelo_padre.nombre)
                else: # modelo sin padre
                    strcb = '<a href="{% url ' + "'" + '@aplicacion:listar_@modelom' + "'" + ' %}">Cancelar</a>'
                    strcb = strcb.replace('@aplicacion', Aplicacion.objects.get(id=modelo.aplicacion.id).nombre)

                strt = strt.replace('@cancelaborrado', strcb)
                strt = strt.replace('@aplicacion', aplicacion.nombre)
                strt = strt.replace('@modelom', modelo.nombre.lower())
                strt = strt.replace('@modeloM', modelo.nombre.upper())
                strt = strt.replace('@modelo', string.capwords(modelo.nombre))
                

                # cd = os.getcwd() + '/' + proyecto.nombre + '/' + aplicacion.nombre + '/' + 'templates/' + aplicacion.nombre 
                cd = proyecto.directorio + '/' + proyecto.nombre + '/' + aplicacion.nombre + '/' + 'templates/' + aplicacion.nombre 

                try:
                    os.remove( cd + '/' + modelo.nombre + '_confirm_delete.html')
                except:
                    print('no hay archivo')
                fd = os.open(cd + '/' + modelo.nombre + '_confirm_delete.html',os.O_CREAT)
                with os.fdopen(os.open(cd + '/' + modelo.nombre + '_confirm_delete.html',os.O_CREAT | os.O_RDWR ),'w') as fd:  
                    fd.write(strt)
                fd.close() 

def CreaSeguridadHtml(proyecto,nombre_archivo):

    cd = os.getcwd() + '/core/static/core/text_files/registration'

    #password_reset_confirm
    try:

        # leer archivo modelo.py de core/text_files
        fo = open(cd + '/' + nombre_archivo, "r+")
        stri = fo.read()

        cd = proyecto.directorio + '/' + proyecto.nombre + '/' + 'registration/templates/registration' 

        try:
            os.remove( cd + '/' + nombre_archivo)
        except:
            print('no hay archivo')

        fd = os.open(cd + '/' + nombre_archivo,os.O_CREAT)
        with os.fdopen(os.open(cd + '/' + nombre_archivo,os.O_CREAT | os.O_RDWR ),'w') as fd:  
            fd.write(stri)
        fd.close()    

    except:
        print('No existe la aplicacion registration')

def CrearUrls(proyecto,aplicacion):
    cd = os.getcwd() + '/core/static/core/text_files'

    # leer archivo urls.py de core/text_files
    fo = open(cd + '/urls_modelo.py', "r+")
    stri = fo.read()
    strmf = ''

    # Para cada modelo
    strt = ''
    strp = ''
    strlv = ''
    strlfp = ''
    strlpp = 'path('',include(core_patterns)),' + '\n'
    for modelo in Modelo.objects.filter(aplicacion=aplicacion):

        if Propiedad.objects.filter(modelo=modelo).count() > 0:
            if modelo.padre == 'nada':
                strlv += 'from .views import Listar@moduloView, Crear@moduloView, Editar@moduloView, Borrar@moduloView, Home@moduloView' + '\n'
            else:
                strlv += 'from .views import Crear@moduloView, Editar@moduloView, Borrar@moduloView' + '\n'

            strlv = strlv.replace('@modulo', string.capwords(modelo.nombre))

            if modelo.padre == 'nada':
                # strp += '\tpath(' + "''" + ', Home@moduloView.as_view(), name=' + "'" + 'home' + "'" + '),' + '\n'
                strp += '\tpath(' + "''" + ',Home' + '@modulo' + 'View, name=' + "'" + 'home' + "'" + '),' + "\n"
                strp += '\tpath(' + "'listar_" + '@modulom/' + "'" + ',Listar@moduloView.as_view(), name=' + "'" + 'listar_@modulom' + "'" + '),' + '\n'

            strp += '\tpath(' + "'" + 'editar_@modulom/<int:pk>/' + "'" + ',Editar@moduloView.as_view(), name=' + "'" + 'editar_@modulom' + "'" +'),' + '\n'
            strp += '\tpath(' + "'" + 'crear_@modulom/' + "'" + ',Crear@moduloView.as_view(), name=' + "'" + 'crear_@modulom' + "'" + '),' + '\n'
            strp += '\tpath(' + "'" + 'borrar_@modulom/<int:pk>/' + "'" + ',Borrar@moduloView.as_view(), name=' + "'" + 'borrar_@modulom' + "'" + '),' + '\n'

            strp = strp.replace('@modulom', modelo.nombre.lower())
            strp = strp.replace('@modulo', string.capwords(modelo.nombre))

            strt += strp + '\n'
            strp = ''

    if strt != '':
        stri = stri.replace('@aplicacion', aplicacion.nombre)
        stri = stri.replace('@listaurls', strt)
        stri = stri.replace('@listaviews', strlv)

    stri = stri.split('\n')
    strt= ''

    for strl in stri:
        strt += strl + '\n'

    # Grabar el modelo si su aplicacion tiene modelos con propiedades
    flgCrear = False
    for modelo in Modelo.objects.filter(aplicacion=aplicacion):
        if Propiedad.objects.filter(modelo=modelo).count() > 0:
            flgCrear = True

    if flgCrear:
        # Grabar el modelo
        cd = proyecto.directorio + '/' + proyecto.nombre + '/' + aplicacion.nombre 

        try:
            os.remove( cd + "/urls.py")
        except:
            print('no hay archivo')

        fd = os.open(cd + '/urls.py',os.O_CREAT)
        with os.fdopen(os.open(cd + '/urls.py',os.O_CREAT | os.O_RDWR ),'w') as fd:  
            fd.write(strt)
        fd.close() 

def CrearForms(proyecto,aplicacion):

    cd = os.getcwd() + '/core/static/core/text_files'

    # leer archivo modelo.py de core/text_files
    fo = open(cd + '/forms.py', "r+")
    stri = fo.read()

    # Para cada modelo
    strt = ''
    strim = ''
    strc = ''
    strform = ''
    strcm = ''

    for modelo in Modelo.objects.filter(aplicacion=aplicacion):

        if Propiedad.objects.filter(modelo=modelo).count() > 0:
            strim += 'from ' + Aplicacion.objects.get(id=modelo.aplicacion.id).nombre + ".models import " + string.capwords(modelo.nombre) + '\n'

        # recorrer propiedades
        strw = ''
        strl = ''
        strf = ''
        pi = ''
        strget = ''
        # variable para modelos foreaneos
        for propiedad in Propiedad.objects.filter(modelo=modelo):
            if propiedad.tipo == 's':
                strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.TextInput(attrs={' + "'" + 'class' + "'" + ':' + "'" + 'form-control ' + "'" + ', ' + "'" + 'placeholder' + "'" + ': ' + "'" + '@textoplaceholder' + "'" + '}),' + '\n'
            if propiedad.tipo == 'x':
                strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.Textarea(attrs={' + "'" + 'class' + "'" + ':' + "'" + 'form-control ' + "'" + ', ' + "'" + 'placeholder' + "'" + ': ' + "'" + '@textoplaceholder' + "'" + '}),' + '\n'
            if propiedad.tipo == 'm':
                strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.TextInput(attrs={' + "'" + 'class' + "'" + ':' + "'" + 'form-control ' + "'" + ', ' + "'" + 'placeholder' + "'" + ': ' + "'" + '@textoplaceholder' + "'" + '}),' + '\n'
            if propiedad.tipo == 'i':
                strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.TextInput(attrs={' + "'" + 'class' + "'" + ':' + "'" + 'form-control ' + "'" + ', ' + "'" + 'placeholder' + "'" + ': ' + "'" + '@textoplaceholder' + "'" + '}),' + '\n'
            if propiedad.tipo == 'l':
                strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.TextInput(attrs={' + "'" + 'class' + "'" + ':' + "'" + 'form-control ' + "'" + ', ' + "'" + 'placeholder' + "'" + ': ' + "'" + '@textoplaceholder' + "'" + '}),' + '\n'
            if propiedad.tipo == 'd':
                strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.TextInput(attrs={' + "'" + 'class' + "'" + ':' + "'" + 'form-control ' + "'" + ', ' + "'" + 'placeholder' + "'" + ': ' + "'" + '@textoplaceholder' + "'" + '}),' + '\n'
            if propiedad.tipo == 'f':
                modelo_foraneo = Modelo.objects.get(nombre=propiedad.foranea , proyecto=proyecto)
                strim += 'from ' + Aplicacion.objects.get(id=modelo_foraneo.aplicacion.id).nombre + '.models import ' + string.capwords(modelo_foraneo.nombre) + "\n"
                strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.Select(choices=' + string.capwords(modelo_foraneo.nombre) + '.objects.all()),' + '\n'
            if propiedad.tipo == 't':
                strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.DateInput(format="%m/%d/%Y"),' + '\n'
            if propiedad.tipo == 'b':
                strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.CheckboxInput(),' + '\n'
            if propiedad.tipo == 'p':
                strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.ClearableFileInput(attrs={' + "'" + 'class' + "'" + ':' + "'" + 'form-control-file ' + "'" + '}),' + '\n'
            if propiedad.tipo == 'r':
                lista_botones = propiedad.textobotones.split(';')
                strlb = ''
                for texto in lista_botones:
                    lista_partes = texto.split(',')
                    strlb += '(' + "'" + lista_partes[0] + "'," + "'" + lista_partes[1] + "')" + ',' + '\n'
                strc += propiedad.nombre + '_choices = (' + strlb + ')' + '\n'
                # strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.RadioSelect(attrs={' + "'" + 'class' + "'" + ': ' + "'" + 'form-control' + "'" + '},choices=' + propiedad.nombre + '_choices),' + '\n'
                strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.RadioSelect(choices=' + propiedad.nombre + '_choices),' + '\n'
            if propiedad.tipo == 'h':
                strw += "\t\t\t'" + propiedad.nombre + "'" + ': forms.Textarea(attrs={' + "'" + 'class' + "'" + ':' + "'" + 'form-control ' + "'" + ', ' + "'" + 'placeholder' + "'" + ': ' + "'" + '@textoplaceholder' + "'" + '}),' + '\n'

            strw = strw.replace('@etiqueta', propiedad.nombre)
            strw = strw.replace('@textoplaceholder', propiedad.textoplaceholder)

            strf += "'" + propiedad.nombre + "'" + ','
            strl += "'" + propiedad.nombre + "':" + "'" + propiedad.nombre + "'" + ','

            # reglas
            strcm = ''
            for regla in Regla.objects.filter(propiedad=propiedad):
                cc = ''
                for lc in regla.codigo.split('\n'):
                    cc += '\t\t' + lc + '\n'
                strcm += cc
                strcm += '\t\t\traise forms.ValidationError(' + "'" + regla.mensaje + "'" + ')' + '\n'

            if strcm != '':
                strget = '\t\t' + propiedad.nombre + ' = self.cleaned_data[' + "'" + propiedad.nombre + "'" + ']' + '\n'
                strget += strcm


        streg = ''
        if strget != '':
            streg += '\tdef clean(self):' + '\n'
            streg += strget


        if strw != '':
            strt = 'class @modeloForm(forms.ModelForm):' + '\n'
            strt += '\tclass Meta:' + '\n'
            strt += '\t\tmodel = @modelo' + '\n'
            strt += '\t\tfields = (@listafields)' + '\n'
            strt += '\t\twidgets = {' + '\n'
            strt += '@listawidgets' + '\n'
            strt += '\t\t}' + '\n'
            strt += '\t\tlabels = {' + '\n'
            strt += '\t\t@listalabels' + '\n'
            strt += '\t\t}' + '\n'
            strt += '@reglas' + '\n'

            strt = strt.replace('@listafields', strf)
            strt = strt.replace('@listalabels', strl)
            strt = strt.replace('@listawidgets', strw)
            strt = strt.replace('@reglas', streg)
            strt = strt.replace('@modelo', string.capwords(modelo.nombre))

            strform += strt + '\n'

            strf = ''
            strl = ''
            strw = ''    

    stri = stri.replace('@listachoices', strc)
    stri = stri.replace('@importmodelos', strim)
    stri = stri.replace('@forms', strform)

    stri = stri.split('\n')
    strt= ''

    for strl in stri:
        strt += strl + '\n'

    # Grabar el modelo si su aplicacion tiene modelos con propiedades
    flgCrear = False
    for modelo in Modelo.objects.filter(aplicacion=aplicacion):
        if Propiedad.objects.filter(modelo=modelo).count() > 0:
            flgCrear = True

    if flgCrear:
        # Grabar el modelo
        cd = proyecto.directorio + '/' + proyecto.nombre + '/' + aplicacion.nombre 

        try:
            os.remove( cd + "/forms.py")
        except:
            print('no hay archivo')

        fd = os.open(cd + '/forms.py',os.O_CREAT)
        with os.fdopen(os.open(cd + '/forms.py',os.O_CREAT | os.O_RDWR ),'w') as fd:  
            fd.write(strt)
        fd.close() 

def CrearVistas(proyecto,aplicacion):

    cd = os.getcwd() + '/core/static/core/text_files'

    # leer archivo modelo.py de core/text_files
    fo = open(cd + '/vistas.py', "r+")
    stri = fo.read()

    # Para cada modelo
    strmp = ''
    strmh = ''
    strim = ''
    strif = ''
    strlh = ''

    for modelo in Modelo.objects.filter(aplicacion=aplicacion):

        if Propiedad.objects.filter(modelo=modelo).count() > 0:
            # Lista de import de formularios
            strif += 'from .forms import ' + string.capwords(modelo.nombre) + 'Form' + '\n'
            #importa modelos
            strim += 'from ' +  Aplicacion.objects.get(id=modelo.aplicacion.id).nombre + '.models import ' + string.capwords(modelo.nombre) + '\n'  

            if modelo.padre != 'nada': 
                # modelo hijo

                strv = 'class Editar@modeloView(UpdateView):' + '\n'
                strv += '\tmodel = @modelo' + '\n'
                strv += '\tform_class = @modeloForm' + '\n'
                strv += '\ttemplate_name_suffix = ' + "'" + '_update_form' + "'"  + '\n'
                strv += '\n'                
                strv += '\tdef get_success_url(self):' + '\n'

                # success de la edicion del modelo hijo o nieto
                modelo_padre = Modelo.objects.get(nombre=modelo.padre , proyecto=proyecto)
                if modelo_padre.padre != 'nada': # modelo nieto
                    modelo_abuelo = Modelo.objects.get(nombre=modelo_padre.padre , proyecto=proyecto)
                    strv += '\t\treturn reverse_lazy(' + "'" + '@aplicacionpadre:editar_@modelopadrem' + "'" + ', args=[self.request.GET[' + "'" +'@modelopadrem_id' + "'" + ']]) + ' + "'" + '?correcto' + "'" + ' + ' + "'" + '&@modeloabuelom_id=' + "'" + ' + str(self.request.GET[' + "'" + '@modeloabuelom_id' + "'" + '])' + '\n'
                    strv = strv.replace('@modeloabuelom', modelo_abuelo.nombre.lower())
                    strv = strv.replace('@modeloabuelo', string.capwords(modelo_abuelo.nombre))
                else: # modelo hijo
                    strv += '\t\treturn reverse_lazy(' + "'" + '@aplicacionpadre:editar_@modelopadrem' + "'" + ', args=[self.request.GET[' + "'" + '@modelopadrem_id' + "'" + ']]) + ' + "'" + '?correcto' + "'"  + '\n'

                strv += '\n'                
                strv += '\tdef get_context_data(self,**kwargs):' + '\n'
                strv += '\t\tcontext = super(Editar@modeloView, self).get_context_data(**kwargs)' + '\n'
                strv += '\t\t@modelom = (self.object)' + '\n'
                strv += '\t\tcontext[' + "'" + '@modelom_id' + "'" + '] = self.object.id' + '\n'
                strv += '\t\tcontext[' + "'" + 'nombre' + "'" + '] = @modelom.@paraborrar' + '\n'
                strv += '@listahijos' + '\n'
                strv += '@idsuperior' + '\n'
                strv += '@numerohijos' + '\n'
                strv += '\t\treturn context' + '\n'

                # define si existe un numero de registros para los hijos
                strnh = ''
                for hijo in Modelo.objects.filter(padre=modelo.nombre , proyecto=proyecto):
                    strnh += '\t\tcontext[' + "'" + 'numero' + hijo.nombre + "'" + '] = ' + string.capwords(hijo.nombre) + '.objects.filter(@modelom=@modelom).count()' + '\n'

                strv = strv.replace('@numerohijos', strnh)

                strv += '\n'                
                strv += 'class Crear@modeloView(CreateView):' + '\n'
                strv += '\tmodel = @modelo' + '\n'
                strv += '\tform_class = @modeloForm' + '\n'
                strv += '\n'                
                strv += '\tdef get_success_url(self):' + '\n'
                strv += '\t\treturn reverse_lazy(' + "'" + '@aplicacionpadre:editar_@modelopadrem' + "'" + ', args=[self.request.GET[' + "'" + '@modelopadrem_id' + "'" + ']]) + ' + "'" + '?correcto' + "'" + '\n'
                strv += '\n'                
                strv += '\tdef post(self,request,*args,**kwargs):' + '\n'
                strv += '\t\tform = self.form_class(request.POST)' + '\n'
                strv += '\t\t@modelopadrem = @modelopadre.objects.get(id = request.GET[' + "'" + '@modelopadrem_id' + "'" + '])' + '\n'
                strv += '\t\tif form.is_valid():' + '\n'
                strv += '\t\t\t@modelom = form.save(commit=False)' + '\n'
                strv += '\t\t\t@modelom.@modelopadrem = @modelopadrem' + '\n'
                strv += '\t\t\t@modelom.save()' + '\n'
                strv += '\t\t\treturn HttpResponseRedirect(self.get_success_url())' + '\n'
                strv += '\t\telse:' + '\n'
                strv += '\t\t\treturn self.render_to_response(self.get_context_data(form=form))' + '\n'
                strv += '\n'    

                # codigo para get_context en Crear
                strv += '@getcontext'
                strgc = ''
                modelo_padre = Modelo.objects.get(nombre=modelo.padre , proyecto=proyecto)
                if modelo_padre.padre != 'nada':  # modelo nieto
                    modelo_abuelo = Modelo.objects.get(nombre=modelo_padre.padre , proyecto=proyecto)
                    strgc += '\tdef get_context_data(self,**kwargs):' + '\n'
                    strgc += '\t\tcontext = super(Crear@modeloView, self).get_context_data(**kwargs)' + '\n'
                    strgc += '\t\tobj = @modelopadre.objects.get(id=self.request.GET[' + "'" + '@modelopadrem_id' + "'" + '])' + '\n'
                    strgc += '\t\tcontext[' + "'" + '@modelopadrem_id' + "'" + '] = obj.id' + '\n'
                    strgc += '\t\t@modeloabuelom = @modeloabuelo.objects.get(id=obj.@modeloabuelom.id)' + '\n'
                    strgc += '\t\tcontext[' + "'" + '@modeloabuelom_id' + "'" + '] = @modeloabuelom.id' + '\n'
                    strgc += '\t\treturn context' + '\n'
                    strgc = strgc.replace('@modeloabuelom', modelo_abuelo.nombre.lower())
                    strgc = strgc.replace('@modeloabuelo', string.capwords(modelo_abuelo.nombre))
                    strim += 'from ' +  Aplicacion.objects.get(id=modelo_abuelo.aplicacion.id).nombre + '.models import ' + string.capwords(modelo_abuelo.nombre) + '\n'  
                else:
                    strgc += '\tdef get_context_data(self,**kwargs):' + '\n'
                    strgc += '\t\tcontext = super(Crear@modeloView, self).get_context_data(**kwargs)' + '\n'
                    strgc += '\t\tcontext[' + "'" + '@modelopadrem_id' + "'" + '] = self.request.GET[' + "'" + '@modelopadrem_id' + "'" + ']' + '\n'
                    strgc += '\t\treturn context' + '\n'


                strgc = strgc.replace('@modelopadrem', modelo_padre.nombre.lower())
                strgc = strgc.replace('@modelopadre', string.capwords(modelo_padre.nombre))

                strv = strv.replace('@getcontext', strgc)

                strim += 'from ' +  Aplicacion.objects.get(id=modelo_padre.aplicacion.id).nombre + '.models import ' + string.capwords(modelo_padre.nombre) + '\n'  
    
                strv += '\n'            
                strv += 'class Borrar@modeloView(DeleteView):' + '\n'
                strv += '\tmodel = @modelo' + '\n'
                strv += '\n'                
                strv += '\tdef get_success_url(self):' + '\n'
                strv += '\t\treturn reverse_lazy(' + "'" + '@aplicacionpadre:editar_@modelopadrem' + "'" + ', args=[self.request.GET[' + "'" + '@modelopadrem_id' + "'" + ']]) + ' + "'" + '?correcto' + "'" + '\n'
                strv += '\n'                
                strv += '\tdef get_context_data(self,**kwargs):' + '\n'
                strv += '\t\tcontext = super(Borrar@modeloView, self).get_context_data(**kwargs)' + '\n'
                strv += '\t\t@modelom = @modelo.objects.get(id=self.object.id)' + '\n'
                strv += '\t\tcontext[' + "'" + 'nombreborrar' + "'" + '] = @modelom.@paraborrar' + '\n'
                strv += '@idsuperior' + '\n'
                strv += '\t\treturn context' + '\n'

                # modelo padre
                # modelo_padre = Modelo.objects.get(nombre=modelo.padre , proyecto=proyecto)
                strv = strv.replace('@modelopadrem', modelo_padre.nombre.lower())
                strv = strv.replace('@modelopadre', string.capwords(modelo_padre.nombre))

                strv = strv.replace('@modelom', modelo.nombre.lower())
                strv = strv.replace('@modelo', string.capwords(modelo.nombre))
                strv = strv.replace('@paraself', modelo.nombre.lower() + '.' + modelo.nombreself)

                # aplicacion
                strv = strv.replace('@aplicacionpadre', Aplicacion.objects.get(id=modelo_padre.aplicacion.id).nombre)

                # lista hijos
                for model in Modelo.objects.filter(padre=modelo.nombre , proyecto=proyecto):
                    strlh += '\t\t' + model.nombre.lower() + ' = ' + string.capwords(model.nombre) + '.objects.filter(' + modelo.nombre.lower() + ' = ' + modelo.nombre.lower() + ')' + '\n'
                    strlh += '\t\t' + 'context[' + "'" + 'lista' + model.nombre.lower() + "'" + '] =  ' + model.nombre.lower()  + '\n'
                strv = strv.replace('@listahijos', strlh)
                strlh = ''    

                # define los id superiores
                stris = ''
                modelo_padre = Modelo.objects.get(nombre=modelo.padre , proyecto=proyecto)
                if modelo_padre.padre != 'nada':  # modelo nieto
                    modelo_abuelo = Modelo.objects.get(nombre=modelo_padre.padre , proyecto=proyecto)
                    stris = '\t\tcontext[' + "'" + '@modelopadrem_id' + "'" + '] = self.object.@modelopadrem.id' + '\n'
                    stris += '\t\t@modelopadrem = @modelopadre.objects.get(id=self.object.@modelopadrem.id)' + '\n'
                    stris += '\t\tcontext[' + "'" + '@modeloabuelom_id' + "'" + '] = @modelopadrem.@modeloabuelom.id' + '\n'
                    stris = stris.replace('@modeloabuelom', modelo_abuelo.nombre.lower())
                    stris = stris.replace('@modeloabuelo', string.capwords(modelo_abuelo.nombre))
                else: # modelo hijo
                    stris = '\t\tcontext[' + "'" + '@modelopadrem_id' + "'" + '] = self.object.@modelopadrem.id' + '\n'
                stris = stris.replace('@modelopadrem', modelo_padre.nombre.lower())
                stris = stris.replace('@modelopadre', string.capwords(modelo_padre.nombre))

                strv = strv.replace('@idsuperior', stris)
                strv = strv.replace('@paraborrar', modelo.nombreborrar)

                strmh += strv + '\n'
                strv = ''

                #importa modelos de padres y abuelos
                strim += 'from ' +  Aplicacion.objects.get(id=modelo_padre.aplicacion.id).nombre + '.models import ' + string.capwords(modelo_padre.nombre) + '\n'  

                if modelo_padre.padre != 'nada': # tiene abuelo
                    modelo_abuelo = Modelo.objects.get(nombre=modelo_padre.padre , proyecto=proyecto)
                    strim += 'from ' +  Aplicacion.objects.get(id=modelo_abuelo.aplicacion.id).nombre + '.models import ' + string.capwords(modelo_abuelo.nombre) + '\n'  

                #importa modelos de hijos
                for modelo_hijo in Modelo.objects.filter(padre=modelo.nombre , proyecto=proyecto):
                    strim += 'from ' +  Aplicacion.objects.get(id=modelo_hijo.aplicacion.id).nombre + '.models import ' + string.capwords(modelo_hijo.nombre) + '\n'  

            else: 
                # modelo padre
                strv = 'def Home@modeloView(request):' + '\n'
                strv += '\treturn render(request,' + "'" + '@aplicacion/home.html' + "'" + ')' + '\n'
                strv += '\n'                
                strv += 'class Listar@modeloView(ListView):' + '\n'
                strv += '\tmodel = @modelo' + '\n'
                strv += '\n'                
                strv += 'class Editar@modeloView(UpdateView):' + '\n'
                strv += '\tmodel = @modelo' + '\n'
                strv += '\tform_class = @modeloForm' + '\n'
                strv += '\ttemplate_name_suffix = ' + "'" + '_update_form' + "'"  + '\n'
                strv += '\n'                
                strv += '\tdef get_success_url(self):' + '\n'
                strv += '\t\treturn reverse_lazy(' + "'" + '@aplicacion:editar_@modelom' + "'" + ', args=[self.object.id]) + ' + "'" + '?correcto' + "'"  + '\n'
                strv += '\n'                
                strv += '\tdef get_context_data(self,**kwargs):' + '\n'
                strv += '\t\tcontext = super(Editar@modeloView, self).get_context_data(**kwargs)' + '\n'
                strv += '\t\t@modelom = (self.object)' + '\n'
                strv += '\t\tcontext[' + "'" + '@modelom_id' + "'" + '] = self.object.id' + '\n'
                strv += '@listahijos' + '\n'
                strv += '\t\tcontext[' + "'" + 'nombre' + "'" + '] = @modelom.@paraborrar' + '\n'

                # define si existe un numero de registros para los hijos
                print (modelo.nombre)
                print(Modelo.objects.filter(padre=modelo.nombre , proyecto=proyecto).count())
                for hijo in Modelo.objects.filter(padre=modelo.nombre, proyecto=proyecto ):
                    strv += '\t\tcontext[' + "'" + 'numero' + hijo.nombre + "'" + '] = ' + string.capwords(hijo.nombre) + '.objects.filter(@modelom=@modelom).count()' + '\n'

                strv += '\t\treturn context' + '\n'
                strv += '\n'                
                strv += 'class Crear@modeloView(CreateView):' + '\n'
                strv += '\tmodel = @modelo' + '\n'
                strv += '\tform_class = @modeloForm' + '\n'
                strv += '\tsuccess_url = reverse_lazy(' + "'" + '@aplicacion:listar_@modelom' + "'" + ')' + '\n'
                strv += '\n'                
                strv += 'class Borrar@modeloView(DeleteView):' + '\n'
                strv += '\tmodel = @modelo' + '\n'
                strv += '\tsuccess_url = reverse_lazy(' + "'" + '@aplicacion:listar_@modelom' + "'" + ')' + '\n'
                strv += '\n'                
                strv += '\tdef get_context_data(self,**kwargs):' + '\n'
                strv += '\t\tcontext = super(Borrar@modeloView, self).get_context_data(**kwargs)' + '\n'
                strv += '\t\t@modelom = @modelo.objects.get(id=self.object.id)' + '\n'
                strv += '\t\tcontext[' + "'" + 'nombreborrar' + "'" + '] = @modelom.@paraborrar' + '\n'
                strv += '\t\treturn context' + '\n'

                strv = strv.replace('@modelom', modelo.nombre.lower())
                strv = strv.replace('@aplicacion', aplicacion.nombre)
                strv = strv.replace('@modelo', string.capwords(modelo.nombre))
                strv = strv.replace('@paraself', modelo.nombre.lower() + '.' + modelo.nombreself)
                strv = strv.replace('@paraborrar', modelo.nombreborrar)

                #importa modelos de hijos
                for modelo_hijo in Modelo.objects.filter(padre=modelo.nombre , proyecto=proyecto):
                    strim += 'from ' +  Aplicacion.objects.get(id=modelo_hijo.aplicacion.id).nombre + '.models import ' + string.capwords(modelo_hijo.nombre) + '\n'  

                # lista hijos
                for model in Modelo.objects.filter(padre=modelo.nombre  , proyecto=proyecto):
                    strlh += '\t\t' + model.nombre.lower() + ' = ' + string.capwords(model.nombre) + '.objects.filter(' + modelo.nombre.lower() + ' = ' + modelo.nombre.lower() + ')' + '\n'
                    strlh += '\t\t' + 'context[' + "'" + 'lista' + model.nombre.lower() + "'" + '] =  ' + model.nombre.lower()  + '\n'
                strv = strv.replace('@listahijos', strlh)
                strlh = ''    

                strmp += strv + '\n'
                strv = ''

    # reemplazar modeloshijo y padre

    stri = stri.replace('@importmodelos', strim)
    stri = stri.replace('@importforms', strif)
    stri = stri.replace('@modelospadre', strmp)
    stri = stri.replace('@modeloshijo', strmh)

    stri = stri.split('\n')
    strt= ''
    for strl in stri:
        strt += strl + '\n'

    # Grabar el modelo si su aplicacion tiene modelos con propiedades
    flgCrear = False
    for modelo in Modelo.objects.filter(aplicacion=aplicacion):
        if Propiedad.objects.filter(modelo=modelo).count() > 0:
            flgCrear = True

    if flgCrear:
        # Grabar el modelo
        cd = proyecto.directorio + '/' + proyecto.nombre + '/' + aplicacion.nombre 

        try:
            os.remove( cd + "/views.py")
        except:
            print('no hay archivo')

        fd = os.open(cd + '/views.py',os.O_CREAT)
        with os.fdopen(os.open(cd + '/views.py',os.O_CREAT | os.O_RDWR ),'w') as fd:  
            fd.write(strt)
        fd.close() 

def CrearModelos(proyecto,aplicacion):
    cd = os.getcwd() + '/core/static/core/text_files'

    # leer archivo modelo.py de core/text_files
    fo = open(cd + '/modelo.py', "r+")
    stri = fo.read()
    strmf = ''

    # Para cada modelo
    strt = ''
    for modelo in Modelo.objects.filter(aplicacion=aplicacion):

        # recorrer propiedades
        strp = ''
        pi = ''

        # ver si el modelo tiene padre
        if modelo.padre != 'nada':
            modelo_padre = Modelo.objects.get(nombre=modelo.padre , proyecto=proyecto)
            if modelo_padre != None:
                if modelo_padre.aplicacion.id != aplicacion.id:
                    strmf += 'from ' + modelo_padre.aplicacion.nombre + '.models import ' +  string.capwords(modelo.padre) + '\n'  

        # variable para modelos foreaneos
        for propiedad in Propiedad.objects.filter(modelo=modelo):
            if propiedad.tipo == 's':
                if propiedad.inicial == '':
                    pi = "''"
                else:
                    pi = propiedad.inicial + "'"
                strp += '\t' + propiedad.nombre + ' = ' + 'models.CharField(max_length=' + str(propiedad.largostring) + ',default=' + pi + ')' + '\n'
            if propiedad.tipo == 'x':
                if propiedad.inicial == '':
                    pi = "''"
                else:
                    pi = propiedad.inicial + "'"
                strp += '\t' + propiedad.nombre + ' = ' + 'models.TextField(default=' + pi + ')' + '\n'
            if propiedad.tipo == 'm':
                if propiedad.inicial == '':
                    pi = '0'
                else:
                    pi = propiedad.inicial
                strp += '\t' + propiedad.nombre + ' =  models.SmallIntegerField(default = ' + pi  + ')' + '\n'
            if propiedad.tipo == 'i':
                if propiedad.inicial == '':
                    pi = '0'
                else:
                    pi = propiedad.inicial
                strp += '\t' + propiedad.nombre + ' =  models.IntegerField(default = ' + pi + ')' + '\n'
            if propiedad.tipo == 'l':
                if propiedad.inicial == '':
                    pi = '0'
                else:
                    pi = propiedad.inicial
                strp += '\t' + propiedad.nombre + ' =  models.BigIntegerField(default = ' + pi + ')' + '\n'
            if propiedad.tipo == 'd':
                if propiedad.inicial == '':
                    pi = '0'
                else:
                    pi = propiedad.inicial
                strp += '\t' + propiedad.nombre + ' =  models.DecimalField(default = ' + pi + ',decimal_places=3,max_digits=10)' + '\n'
            if propiedad.tipo == 'f':
                strp += '\t' + propiedad.nombre + ' =  models.ForeignKey(' +  string.capwords(propiedad.foranea) + ', on_delete=models.CASCADE' + ')' + '\n'
                # llenar la variable de modelos foraneos
                try:
                    modelo_foraneo = Modelo.objects.get(nombre=propiedad.foranea , proyecto=proyecto)
                    if modelo_foraneo != None:
                        aplicacion_foranea = Aplicacion.objects.get(id=modelo_foraneo.aplicacion.id)
                        if aplicacion_foranea.id != modelo.aplicacion.id:
                            strmf += 'from ' + aplicacion_foranea.nombre + '.models import ' +  string.capwords(propiedad.foranea) + '\n'  
                except:
                    print('noleyo')                     
            if propiedad.tipo == 't':
                if propiedad.inicial == '':
                    pi = 'timezone.now'
                else:
                    pi = propiedad.inicial + "'"
                strp += '\t' + propiedad.nombre + ' =  models.DateTimeField(default=' + pi + ')' + '\n'
            if propiedad.tipo == 'b':
                if propiedad.inicial == '':
                    pi = 'False'
                else:
                    pi = propiedad.inicial
                strp += '\t' + propiedad.nombre + ' =  models.BooleanField(default = ' + pi + ')' + '\n'
            if propiedad.tipo == 'r':
                if propiedad.inicial == '':
                    pi = "''"
                else:
                    pi = propiedad.inicial + "'"
                strp += '\t' + propiedad.nombre + ' = ' + 'models.CharField(max_length=' + str(propiedad.largostring) + ',default=' + pi + ')' + '\n'
            if propiedad.tipo == 'h':
                strp += '\t' + propiedad.nombre + ' = ' + 'RichTextField()' + '\n'
            if propiedad.tipo == 'p':
                strp += '\t' + propiedad.nombre + ' = models.ImageField(upload_to=' + "'" + modelo.nombre + "'" + ',blank=True,null=True)' + '\n'

        if strp != '':
            #ver si el modelo es dependiente
            if modelo.padre != 'nada':
                strp += '\t' + modelo.padre + ' =  models.ForeignKey(' +  string.capwords(modelo.padre) + ', on_delete=models.CASCADE' + ')' + '\n'

            strmodelo = 'class @nombremodelo(models.Model):' + '\n'
            strmodelo += '@propiedades' + '\n'
            strmodelo += '\n'
            strmodelo += '\tdef __str__(self):' + '\n'
            # strmodelo += '\t\treturn str(self.@paraself)' + '\n' 
            strmodelo += '\t\treturn @paraself' + '\n' 

            strmodelo = strmodelo.replace('@nombremodelo', string.capwords(modelo.nombre))

            strmodelo = strmodelo.replace('@propiedades', strp)
            strmodelo = strmodelo.replace('@paraself', modelo.nombreself)

            strp = ''

            strt += strmodelo + '\n'


    stri = stri.replace('@modelos', strt)
    stri = stri.replace('@foraneos',  strmf)


    stri = stri.split('\n')
    strt= ''
    for strl in stri:
        strt += strl + '\n'

    # Grabar el modelo si su aplicacion tiene modelos con propiedades
    flgCrear = False
    for modelo in Modelo.objects.filter(aplicacion=aplicacion):
        if Propiedad.objects.filter(modelo=modelo).count() > 0:
            flgCrear = True
    
    if flgCrear:            
        cd = proyecto.directorio + '/' + proyecto.nombre + '/' + aplicacion.nombre 

        try:
            os.remove( cd + "/models.py")
        except:
            print('no hay archivo')

        fd = os.open(cd + '/models.py',os.O_CREAT)
        with os.fdopen(os.open(cd + '/models.py',os.O_CREAT | os.O_RDWR ),'w') as fd:  
            fd.write(strt)
        fd.close() 

def CrearDirectoriosProyecto(proyecto):

    cd = proyecto.directorio

    # Remover el directorio
    try:
        shutil.rmtree(cd + '/' + proyecto.nombre)
    except:
        print ('no se removio')

    # Crear el directorio del proyecto
    try:
        os.mkdir(cd + '/' + proyecto.nombre)
    except:
        print('ya existe')

    # Crear el directorio de settings
    cd = cd + '/' + proyecto.nombre
    try:
        os.mkdir(cd + '/' + proyecto.nombre)
    except:
        print('ya existe')

    # Crear el directorio __pycache__ bajo el directorio de settings
    try:
        os.mkdir(cd + '/' + proyecto.nombre + '/__pycache__')
    except:
        print('ya existe')

def CrearArchivosProyectos(proyecto):

    cd = os.getcwd() + '/core/static/core/text_files'

    # leer archivo seetings de core/text_files
    fo = open(cd + '/settings.py', "r+")
    stri = fo.read()
    # reemplzar @proyecto
    stri = stri.replace('@proyecto', proyecto.nombre)

    #reemplazar @aplicaciones
    stra = ''
    for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):
        # verificar si la aplicacion tiene modelos y estos tienen propiedades
        flgCrear = False
        for modelo in Modelo.objects.filter(aplicacion=aplicacion):
            if Propiedad.objects.filter(modelo=modelo).count() > 0:
               flgCrear = True

        if flgCrear:
            stra += '    ' + "'" + aplicacion.nombre + "'" + ',' + '\n'
    
    stri = stri.replace('@aplicaciones', stra)

    # Grabar el archivo settings debajo del directorio settings
    cd = proyecto.directorio + '/' + proyecto.nombre + '/' + proyecto.nombre 
    fd = os.open(cd + '/settings.py',os.O_CREAT)
    with os.fdopen(os.open(cd + '/settings.py',os.O_CREAT | os.O_RDWR ),'w') as fd:  
        fd.write(stri)
    fd.close() 

    # Crear db.sqlite3 debajo del directorio settings

    cd = os.getcwd() + '/core/static/core/text_files'

    # leer archivo seetings de core/text_files
    fo = open(cd + '/db.sqlite3', "r+")
    stri = fo.read()
    # reemplzar @proyecto
    stri = stri.replace('@proyecto', proyecto.nombre)

    # Grabar el archivo db.sqlite3 debajo del directorio settings
    cd = proyecto.directorio + '/' + proyecto.nombre 
    fd = os.open(cd + '/db.sqlite3',os.O_CREAT)
    with os.fdopen(os.open(cd + '/db.sqlite3',os.O_CREAT | os.O_RDWR ),'w') as fd:  
        fd.write(stri)
    fd.close() 

    # Crear manage.py debajo del directorio proyecto

    cd = os.getcwd() + '/core/static/core/text_files'

    # leer archivo manage.py de core/text_files
    fo = open(cd + '/manage.py', "r+")
    stri = fo.read()
    # reemplzar @proyecto
    stri = stri.replace('@proyecto', proyecto.nombre)

    # Grabar el archivo manage.py debajo del directorio del proyecto
    cd = proyecto.directorio + '/' + proyecto.nombre  
    fd = os.open(cd + '/manage.py',os.O_CREAT)
    with os.fdopen(os.open(cd + '/manage.py',os.O_CREAT | os.O_RDWR ),'w') as fd:  
        fd.write(stri)
    fd.close() 

    # Crear urls.py debajo del directorio proyecto

    cd = os.getcwd() + '/core/static/core/text_files'

    # leer archivo urls de core/text_files
    fo = open(cd + '/urls.py', "r+")
    stri = fo.read()
    # reemplzar @proyecto
    stri = stri.replace('@proyecto', proyecto.nombre)

    # Grabar el archivo urls.py debajo del directorio del proyecto
    cd = proyecto.directorio + '/' + proyecto.nombre + '/' + proyecto.nombre 
    fd = os.open(cd + '/urls.py',os.O_CREAT)
    with os.fdopen(os.open(cd + '/urls.py',os.O_CREAT | os.O_RDWR ),'w') as fd:  
        fd.write(stri)
    fd.close() 

    # Crear wsgi.py debajo del directorio proyecto

    cd = os.getcwd() + '/core/static/core/text_files'

    # leer archivo wsgi de core/text_files
    fo = open(cd + '/wsgi.py', "r+")
    stri = fo.read()
    # reemplzar @proyecto
    stri = stri.replace('@proyecto', proyecto.nombre)

    # Grabar el archivo wsgi.py debajo del directorio del proyecto
    cd = proyecto.directorio + '/' + proyecto.nombre + '/' + proyecto.nombre 
    fd = os.open(cd + '/wsgi.py',os.O_CREAT)
    with os.fdopen(os.open(cd + '/wsgi.py',os.O_CREAT | os.O_RDWR ),'w') as fd:  
        fd.write(stri)
    fd.close() 

    # Crear __init__.py debajo del directorio proyecto

    cd = os.getcwd() + '/core/static/core/text_files'

    # leer archivo __init__ de core/text_files
    fo = open(cd + '/__init__.py', "r+")
    stri = fo.read()
    # reemplzar @proyecto
    stri = stri.replace('@proyecto', proyecto.nombre)

    # Grabar el archivo _init__.py debajo del directorio del proyecto
    cd = proyecto.directorio + '/' + proyecto.nombre + '/' + proyecto.nombre 
    fd = os.open(cd + '/__init__.py',os.O_CREAT)
    with os.fdopen(os.open(cd + '/__init__.py',os.O_CREAT | os.O_RDWR ),'w') as fd:  
        fd.write(stri)
    fd.close() 

def CrearAplicaciones(proyecto):
    # Crear directorios para aplicaciones
    cd = proyecto.directorio + '/' + proyecto.nombre
    # Crear un directorio por aplicacion

    # variable para lista de aplicaciones en settings.py
    
    for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):

        try:

            # verificar si la aplicacion tiene modelos y estos tienen propiedades
            flgCrear = False
            for modelo in Modelo.objects.filter(aplicacion=aplicacion):
                if Propiedad.objects.filter(modelo=modelo).count() > 0:
                    flgCrear = True

            if flgCrear or aplicacion.nombre == 'core' or aplicacion.nombre == 'registration':     
                try:               
                    os.mkdir(cd + '/' + aplicacion.nombre) 
                except:
                    print ('ya existe ' + aplicacion.nombre)

                # Crear directorio templates, migrations, __pycache debajo de cada aplicacion
                try:
                   os.mkdir(cd + '/' + aplicacion.nombre + '/' + 'templates') 
                   os.mkdir(cd + '/' + aplicacion.nombre + '/' + 'migrations') 

                   # Crear un directorio con el nombre de la aplicacion debajo de templates
                   try:
                        os.mkdir(cd + '/' + aplicacion.nombre + '/' + 'templates/' + aplicacion.nombre)
                   except:
                        print('ya existe templates ' + aplicacion.nombre)  

                   # si es la aplicacion core crear el directorio includes y el static
                   if aplicacion.nombre == 'core':
                        try:
                            os.mkdir(cd + '/' + aplicacion.nombre + '/templates/core/' + 'includes') 
                        except:
                            print('ya existe includes')

                        # crear static
                        try:
                            os.mkdir(cd + '/' + aplicacion.nombre + '/static') 
                        except:
                            print('ya existe static')

                        # crear core bajo static
                        try:
                            os.mkdir(cd + '/' + aplicacion.nombre + '/static/core') 
                        except:
                            print('ya existe static/core')


                        # crear css
                        try:
                            os.mkdir(cd + '/' + aplicacion.nombre + '/static/core' + '/' + 'css') 
                        except:
                            print('ya existe static css')

                        # crear img
                        try:
                            os.mkdir(cd + '/' + aplicacion.nombre + '/static/core' + '/' + 'img') 
                        except:
                            print('ya existe static img')

                        # crear js
                        try:
                            os.mkdir(cd + '/' + aplicacion.nombre + '/static/core' + '/' + 'js') 
                        except:
                            print('ya existe static js')

                except:
                    print ('ya existe templates migrations')

                # strla += "\t'" + aplicacion.nombre + "'," + '\n'

        except Exception as e:
            print (e)

    # formar la lista de aplicaciones para settings
    strla = ''
    for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):
        # formar la lista con los nombres de las aplicaciones
        flgCrear = False
        for modelo in Modelo.objects.filter(aplicacion=aplicacion):
            if Propiedad.objects.filter(modelo=modelo).count() > 0:
                flgCrear = True

        if flgCrear or aplicacion.nombre == 'core':   
            strla += "\t'" + aplicacion.nombre + "'," + '\n'

    # modificar archivo settings.py  del proyecto con la lista de los nombres de las aplicaciones
    cd = os.getcwd() + '/core/static/core/text_files'
    fo = open(cd + '/settings.py', "r+")
    stri = fo.read()
    
    stri = stri.replace('#@aplicaciones', strla)
    stri = stri.replace('@proyecto', proyecto.nombre)

    cd = proyecto.directorio + '/' + proyecto.nombre + '/' + proyecto.nombre 
    try:
        os.remove( cd + "/settings.py")
    except:
        print('no hay archivo')
    
    fd = os.open(cd + '/settings.py',os.O_CREAT)
    with os.fdopen(os.open(cd + '/settings.py',os.O_CREAT | os.O_RDWR ),'w') as fd:  
        fd.write(stri)
    fd.close() 

    # Crear archivos de aplicaciones
    cd = proyecto.directorio + '/' + proyecto.nombre
    for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):
        print(aplicacion.nombre)
        # verificar si la aplicacion tiene modelos y estos tienen propiedades
        flgCrear = False
        for modelo in Modelo.objects.filter(aplicacion=aplicacion):
            if Propiedad.objects.filter(modelo=modelo).count() > 0:
                flgCrear = True

        if flgCrear or aplicacion.nombre == 'core' or aplicacion.nombre == 'registration':
            cd = os.getcwd() + '/core/static/core/text_files'

            # leer archivo __init__.py de core/text_files
            fo = open(cd + '/__init__.py', "r+")
            stri = fo.read()
            # reemplzar @proyecto
            stri = stri.replace('@proyecto', proyecto.nombre)
            
            # Crear el archivo __init__.py debajo de migratioms
            cd = proyecto.directorio + '/' + proyecto.nombre + '/' + aplicacion.nombre + '/' + 'migrations'
            fd = os.open(cd + '/__init__.py',os.O_CREAT)
            with os.fdopen(os.open(cd + '/__init__.py',os.O_CREAT | os.O_RDWR ),'w') as fd:  
                fd.write(stri)
            fd.close() 

            # Crear el archivo __init__.py debajo de cada aplicacion
            cd = proyecto.directorio + '/' + proyecto.nombre + '/' + aplicacion.nombre 

            fd = os.open(cd + '/__init__.py',os.O_CREAT)
            with os.fdopen(os.open(cd + '/__init__.py',os.O_CREAT | os.O_RDWR ),'w') as fd:  
                fd.write(stri)
            fd.close() 

            # leer archivo admin.py de core/text_files
            cd = os.getcwd() + '/core/static/core/text_files'
            fo = open(cd + '/admin.py', "r+")
            stri = fo.read()
            # reemplzar @proyecto
            stri = stri.replace('@proyecto', proyecto.nombre)

            # Crear el archivo admin.py debajo de cada aplicacion
            cd = proyecto.directorio + '/' + proyecto.nombre + '/' + aplicacion.nombre 

            fd = os.open(cd + '/admin.py',os.O_CREAT)
            with os.fdopen(os.open(cd + '/admin.py',os.O_CREAT | os.O_RDWR ),'w') as fd:  
                fd.write(stri)
            fd.close() 

            # leer archivo apps.py de core/text_files
            cd = os.getcwd() + '/core/static/core/text_files'
            fo = open(cd + '/apps.py', "r+")
            stri = fo.read()
            # reemplzar @proyecto
            stri = stri.replace('@proyecto', proyecto.nombre)

            # Crear el archivo admin.py debajo de cada aplicacion
            cd = proyecto.directorio + '/' + proyecto.nombre + '/' + aplicacion.nombre 

            fd = os.open(cd + '/apps.py',os.O_CREAT)
            with os.fdopen(os.open(cd + '/apps.py',os.O_CREAT | os.O_RDWR ),'w') as fd:  
                fd.write(stri)
            fd.close() 

            # leer archivo models.py de core/text_files
            cd = os.getcwd() + '/core/static/core/text_files'
            fo = open(cd + '/models.py', "r+")
            stri = fo.read()
            # reemplzar @proyecto
            stri = stri.replace('@proyecto', proyecto.nombre)

            # Crear el archivo admin.py debajo de cada aplicacion
            cd = proyecto.directorio + '/' + proyecto.nombre + '/' + aplicacion.nombre 

            fd = os.open(cd + '/models.py',os.O_CREAT)
            with os.fdopen(os.open(cd + '/models.py',os.O_CREAT | os.O_RDWR ),'w') as fd:  
                fd.write(stri)
            fd.close() 

            # leer archivo tests.py de core/text_files
            cd = os.getcwd() + '/core/static/core/text_files'
            fo = open(cd + '/tests.py', "r+")
            stri = fo.read()
            # reemplzar @proyecto
            stri = stri.replace('@proyecto', proyecto.nombre)

            # Crear el archivo tests.py debajo de cada aplicacion
            cd = proyecto.directorio + '/' + proyecto.nombre + '/' + aplicacion.nombre 

            fd = os.open(cd + '/tests.py',os.O_CREAT)
            with os.fdopen(os.open(cd + '/tests.py',os.O_CREAT | os.O_RDWR ),'w') as fd:  
                fd.write(stri)
            fd.close() 

            # leer archivo views.py de core/text_files
            cd = os.getcwd() + '/core/static/core/text_files'
            fo = open(cd + '/views.py', "r+")
            stri = fo.read()
            # reemplzar @proyecto
            stri = stri.replace('@proyecto', proyecto.nombre)

            # Crear el archivo admin.py debajo de cada aplicacion
            cd = proyecto.directorio + '/' + proyecto.nombre + '/' + aplicacion.nombre 

            fd = os.open(cd + '/views.py',os.O_CREAT)
            with os.fdopen(os.open(cd + '/views.py',os.O_CREAT | os.O_RDWR ),'w') as fd:  
                fd.write(stri)
            fd.close() 

            # Crear el archivo forms.py debajo de cada aplicacion
            cd = proyecto.directorio + '/' + proyecto.nombre + '/' + aplicacion.nombre 

            fd = os.open(cd + '/forms.py',os.O_CREAT)
            with os.fdopen(os.open(cd + '/forms.py',os.O_CREAT | os.O_RDWR ),'w') as fd:  
                fd.write(stri)
            fd.close() 

            # Crear el archivo urls.py debajo de cada aplicacion
            cd = proyecto.directorio + '/' + proyecto.nombre + '/' + aplicacion.nombre 

            fd = os.open(cd + '/urls.py',os.O_CREAT)
            with os.fdopen(os.open(cd + '/urls.py',os.O_CREAT | os.O_RDWR ),'w') as fd:  
                fd.write(stri)
            fd.close() 

def CrearProyecto(proyecto):

    cd = proyecto.directorio

    # Crear el directorio del proyecto
    try:
        shutil.rmtree(cd + '/' + proyecto.nombre)
    except:
        print ('no se removio')

    try:
        os.mkdir(cd + '/' + proyecto.nombre)
    except:
        print('ya existe')

    # Crear el directorio media
    try:
        shutil.rmtree(cd + '/' + proyecto.nombre + '/' + 'media')
    except:
        print ('no se removio')

    try:
        os.mkdir(cd + '/' + proyecto.nombre + '/' + 'media')
    except:
        print('ya existe')

    # # Crear directorios para media por aplicacion
    # for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):
    #     try:
    #         shutil.rmtree(cd + '/' + proyecto.nombre + '/' + 'media' + '/' + aplicacion.nombre)
    #     except:
    #         print ('no se removio')

    #     try:
    #         os.mkdir(cd + '/' + proyecto.nombre + '/' + 'media' + '/' + aplicacion.nombre)
    #     except:
    #         print('ya existe')     

    # Crear el directorio del proyecto del proyecto
    cd = proyecto.directorio + '/' + proyecto.nombre 
    try:
        shutil.rmtree(cd + '/' + proyecto.nombre)
    except:
        print ('no se removio')

    try:
        os.mkdir(cd + '/' + proyecto.nombre)
    except:
        print('ya existe')

    # crear el archivo __init__.py debajo del proyecto,proyecto
    # leer archivo __init__.py  de core/text_files
    cd = os.getcwd() + '/core/static/core/text_files'
    fo = open(cd + '/__init__.py', "r+")
    stri = fo.read()

    # Grabar el archivo __init__.py debajo del directorio del proyecto
    cd = proyecto.directorio + '/' + proyecto.nombre + '/' + proyecto.nombre 

    try:
        os.remove( cd + "/__init__.py")
    except:
        print('no hay archivo')
    
    fd = os.open(cd + '/__init__.py',os.O_CREAT)
    with os.fdopen(os.open(cd + '/__init__.py',os.O_CREAT | os.O_RDWR ),'w') as fd:  
        fd.write(stri)
    fd.close() 

    # crear el archivo settings.py debajo del proyecto,proyecto
    # leer archivo settings.py  de core/text_files
    cd = os.getcwd() + '/core/static/core/text_files'
    fo = open(cd + '/settings.py', "r+")
    stri = fo.read()

    # reemplzar @proyecto
    stri = stri.replace('@proyecto', proyecto.nombre)

    # Grabar el archivo settings.py debajo del directorio del proyecto
    cd = proyecto.directorio + '/' + proyecto.nombre + '/' + proyecto.nombre 

    try:
        os.remove( cd + "/settings.py")
    except:
        print('no hay archivo')
    
    fd = os.open(cd + '/settings.py',os.O_CREAT)
    with os.fdopen(os.open(cd + '/settings.py',os.O_CREAT | os.O_RDWR ),'w') as fd:  
        fd.write(stri)
    fd.close() 

    # crear el archivo urls.py debajo del proyecto,proyecto
    # leer archivo urls.py  de core/text_files
    cd = os.getcwd() + '/core/static/core/text_files'
    fo = open(cd + '/urls.py', "r+")
    stri = fo.read()

    # Grabar el archivo urls.py debajo del directorio del proyecto
    cd = proyecto.directorio + '/' + proyecto.nombre + '/' + proyecto.nombre 

    try:
        os.remove( cd + "/urls.py")
    except:
        print('no hay archivo')
    
    fd = os.open(cd + '/urls.py',os.O_CREAT)
    with os.fdopen(os.open(cd + '/urls.py',os.O_CREAT | os.O_RDWR ),'w') as fd:  
        fd.write(stri)
    fd.close() 


    # crear el archivo wsgi.py debajo del proyecto,proyecto
    # leer archivo wsgi.py  de core/text_files
    cd = os.getcwd() + '/core/static/core/text_files'
    fo = open(cd + '/wsgi.py', "r+")
    stri = fo.read()

    # reemplzar @proyecto
    stri = stri.replace('@proyecto', proyecto.nombre)

    # Grabar el archivo wsgi.py debajo del directorio del proyecto
    cd = proyecto.directorio + '/' + proyecto.nombre + '/' + proyecto.nombre 

    try:
        os.remove( cd + "/wsgi.py")
    except:
        print('no hay archivo')
    
    fd = os.open(cd + '/wsgi.py',os.O_CREAT)
    with os.fdopen(os.open(cd + '/wsgi.py',os.O_CREAT | os.O_RDWR ),'w') as fd:  
        fd.write(stri)
    fd.close() 

    # crear el archivo manage.py debajo del proyecto
    # leer archivo manage.py  de core/text_files
    cd = os.getcwd() + '/core/static/core/text_files'
    fo = open(cd + '/manage.py', "r+")
    stri = fo.read()

    # reemplzar @proyecto
    stri = stri.replace('@proyecto', proyecto.nombre)

    # Grabar el archivo manage.py debajo del directorio del proyecto
    cd = proyecto.directorio + '/' + proyecto.nombre  

    try:
        os.remove( cd + "/manage.py")
    except:
        print('no hay archivo')
    
    fd = os.open(cd + '/manage.py',os.O_CREAT)
    with os.fdopen(os.open(cd + '/manage.py',os.O_CREAT | os.O_RDWR ),'w') as fd:  
        fd.write(stri)
    fd.close() 

    # copiar el archivo del proyecto a img de static

def ListaCrear(id):
    Crear.objects.all().delete()
    proyecto = Proyecto.objects.get(id=id)

    listacrear = Crear()
    listacrear.elemento = 'p'
    listacrear.nombre = proyecto.nombre
    listacrear.proyectoid = proyecto.id
    listacrear.save()

    # crear aplicaciones
    pa=1
    for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):
        listacrear = Crear()
        listacrear.elemento='a'
        listacrear.nombre = aplicacion.nombre
        if pa == 1:
            pa=0
            listacrear.primero = True
        listacrear.proyectoid = proyecto.id
        listacrear.aplicacionid = aplicacion.id
        listacrear.save()

        # crear modelos
        pm=1
        for modelo in Modelo.objects.filter(aplicacion=aplicacion):
            listacrear = Crear()
            listacrear.elemento ='m'
            listacrear.nombre = modelo.nombre
            listacrear.nombremayuscula = string.capwords(modelo.nombre)
            listacrear.padre = modelo.padre
            listacrear.nombreself = modelo.nombreself
            if pm == 1:
                pm=0
                listacrear.primero = True
            listacrear.proyectoid = proyecto.id
            listacrear.aplicacionid = aplicacion.id
            listacrear.modeloid = modelo.id

            # verificar la identacion del modelo
            modeloi = modelo
            identa = 110
            while modeloi.padre != 'nada':
                identa += 55
                modeloi = Modelo.objects.get(nombre=modeloi.padre , proyecto=proyecto)
            listacrear.identa = identa
            listacrear.restoidenta = 12 - identa
            listacrear.save()

            # crear propiedades
            pd=1    
            for propiedad in Propiedad.objects.filter(modelo=modelo):
                listacrear = Crear()
                listacrear.elemento ='d'
                listacrear.nombre = propiedad.nombre
                if propiedad.tipo == 's':
                    listacrear.nombretipo = 'Char'
                if propiedad.tipo == 'x':
                    listacrear.nombretipo = 'Text'
                if propiedad.tipo == 'm':
                    listacrear.nombretipo = 'SmallInteger'
                if propiedad.tipo == 'i':
                    listacrear.nombretipo = 'Integer'
                if propiedad.tipo == 'l':
                    listacrear.nombretipo = 'LongInteger'
                if propiedad.tipo == 'd':
                    listacrear.nombretipo = 'Decimal'
                if propiedad.tipo == 'f':
                    listacrear.nombretipo = 'Foreign'
                if propiedad.tipo == 't':
                    listacrear.nombretipo = 'Date'
                if propiedad.tipo == 'b':
                    listacrear.nombretipo = 'Boolean'
                if propiedad.tipo == 'r':
                    listacrear.nombretipo = 'Radio'
                if propiedad.tipo == 'p':
                    listacrear.nombretipo = 'Imagen'
                listacrear.tipo = propiedad.tipo
                listacrear.largostring = propiedad.largostring
                listacrear.foranea = propiedad.foranea
                listacrear.inicial = propiedad.inicial
                listacrear.etiqueta = propiedad.nombre
                listacrear.textobotones = propiedad.textobotones
                if pd == 1:
                    pd=0
                    listacrear.primero = True
                listacrear.proyectoid = proyecto.id
                listacrear.aplicacionid = aplicacion.id
                listacrear.modeloid = modelo.id
                listacrear.propiedadid = propiedad.id
                listacrear.identa = identa + 55
                listacrear.restoidenta = 12 - (identa + 1)
                listacrear.save()

                # crear reglas
                pr=1    
                for regla in Regla.objects.filter(propiedad=propiedad):
                    listacrear = Crear()
                    listacrear.elemento ='r'
                    listacrear.mensaje = regla.mensaje
                    listacrear.codigo = regla.codigo
                    if pr == 1:
                        pr=0
                        listacrear.primero = True
                    listacrear.proyectoid = proyecto.id
                    listacrear.aplicacionid = aplicacion.id
                    listacrear.modeloid = modelo.id
                    listacrear.propiedadid = propiedad.id
                    listacrear.reglaid = regla.id
                    listacrear.identa = identa + 110
                    listacrear.restoidenta = 12 - (identa + 2)
                    listacrear.save()

    lista = Crear.objects.all()
    return lista


    # Los hijos se despliegan al lado del padre

# Los hijos se despliegan al lado del padre


def CrearTemplatesAlLado(proyecto):

    # variable para desglosar el font
    strFont = ''

    # prepara el archivo base.htm para titulo izquierda o derecha

    cd = os.getcwd() + '/core/static/core/text_files'

    fo = open(cd + '/base.html', "r+")
    stri = fo.read()

    strti =  '\t\t\t<div class="col-@numerocolumnaslogo @justificacionlogo @justificacionverticallogo color_fondo_logo">' + '\n'
    strti += '\t\t\t\t@avatarlogo' + '\n'
    strti += '\t\t\t</div>' + '\n'
    strtd =  '\t\t\t<div class="col-@numerocolumnastitulo font_titulo @justificaciontitulo @justificacionverticaltitulo color_fondo_titulo">' + '\n'
    strtd += '\t\t\t\t@avatartitulo' + '\n'
    strtd += '\t\t\t\t@titulo' + '\n'
    strtd += '\t\t\t</div>' + '\n'

    # titulo izquierda
    if proyecto.tituloizquierda:
        stri = stri.replace('@tituloizquierda', strtd + strti)
    else:
        stri = stri.replace('@tituloizquierda', strti + strtd)

    # crear archivo base.html de core
    cd = proyecto.directorio + '/' + proyecto.nombre + '/core/templates/core'

    try:
            os.remove( cd + "/base.html")
    except:
        print('no hay archivo')

    try:
        fd = os.open(cd + '/base.html',os.O_CREAT)
        with os.fdopen(os.open(cd + '/base.html',os.O_CREAT | os.O_RDWR ),'w') as fd:  
            fd.write(stri)
        fd.close() 
    except:
        print('no se creo base.html')

    # completa el archivo base.html

    # cd = os.getcwd() + '/core/static/core/text_files'
    
    cd = proyecto.directorio + '/' + proyecto.nombre + '/core/templates/core'
    
    fo = open(cd + '/base.html', "r+")
    stri = fo.read()
    # el archivo Base.html

    print (stri)
    # crear archivo base.html de core
    # cd = os.getcwd() + '/' + proyecto.nombre + '/core/templates/core'
    cd = proyecto.directorio + '/' + proyecto.nombre + '/core/templates/core'

    try:
            os.remove( cd + "/base.html")
    except:
        print('no hay archivo')

    try:

        #copiar el archivo de logo del proyecto a static/core/img
        destino = proyecto.directorio + '/' + proyecto.nombre + '/core/static/core/img/logo.png'
        print(proyecto.avatar)
        if proyecto.avatar: 
            CopiaImagenes(destino,'proyectos',proyecto.avatar.url)
        #copiar el archivo de avatar del titulo del proyecto a static/core/img
        destino = proyecto.directorio + '/' + proyecto.nombre + '/core/static/core/img/titulo.png' 
        if proyecto.avatartitulo:
            CopiaImagenes(destino,'proyectos',proyecto.avatartitulo.url)

        # columnas izquierda derecha encabezado
        stri = stri.replace('@columnasizquierdaencabezado', str(proyecto.columnasizquierdaencabezado))
        stri = stri.replace('@columnasderechaencabezado', str(proyecto.columnasderechaencabezado))

        #alto encabezado
        stri = stri.replace('@altoencabezado', str(proyecto.altoencabezado))

        #color fondo encabezado
        stri = stri.replace('@colorfondoencabezado', proyecto.colorfondoencabezado)

        # logo
        stri = stri.replace('@altologo', str(proyecto.altopixeles))
        stri = stri.replace('@anchologo', str(proyecto.anchopixeles))
        stri = stri.replace('@numerocolumnaslogo', str(proyecto.numerocolumnas))
        stri = stri.replace('@colorfondologo', proyecto.colorfondologo)

        #justificacion vertical logo
        strJusti=''
        if proyecto.justificacionverticallogo == 's':
            strJusti = 'align-self-start'
        if proyecto.justificacionverticallogo == 'c':
            strJusti = 'align-self-center'
        if proyecto.justificacionverticallogo == 'i':
            strJusti = 'align-self-end'        
        stri = stri.replace('@justificacionverticallogo', strJusti)

        strJusti=''
        if proyecto.justificacion == 'i':
            strJusti = 'text-left'
        if proyecto.justificacion == 'd':
            strJusti = 'text-right'
        if proyecto.justificacion == 'c':
            strJusti = 'text-center'

        stri = stri.replace('@justificacionlogo', strJusti)
        # TITULO
        stri = stri.replace('@titulo', proyecto.textotitulo)

        #avatar logo

        if proyecto.avatar:
            stri = stri.replace('@avatarlogo', '<img class="alto_ancho_imagen_logo" src="{% static ' + "'" + 'core/img/logo.png' + "'" + '" %}">')
        else:
            stri = stri.replace('@avatarlogo', '')

        # font titulo
        strFont = proyecto.fonttitulo.split(',')
        stri = stri.replace('@fonttitulo', strFont[0])
        stri = stri.replace('@sizetitulo', strFont[1])
        stri = stri.replace('@boldtitulo', strFont[2])
        stri = stri.replace('@colortitulo', proyecto.colortitulo)
        stri = stri.replace('@numerocolumnastitulo', str(proyecto.numerocolumnastitulo))
        stri = stri.replace('@colorfondotitulo', proyecto.colorfondotitulo)

        if proyecto.justificaciontitulo == 'i':
            strJusti = 'text-left'
        if proyecto.justificaciontitulo == 'd':
            strJusti = 'text-right'
        if proyecto.justificaciontitulo == 'c':
            strJusti = 'text-center'
        stri = stri.replace('@justificaciontitulo', strJusti)

        #justificacion vertical titulo
        strJusti=''
        if proyecto.justificacionverticaltitulo == 's':
            strJusti = 'align-self-start'
        if proyecto.justificacionverticaltitulo == 'c':
            strJusti = 'align-self-center'
        if proyecto.justificacionverticaltitulo == 'i':
            strJusti = 'align-self-end'        
        stri = stri.replace('@justificacionverticaltitulo', strJusti)

        stri = stri.replace('@justificacionverticaltitulo', proyecto.justificacionverticaltitulo)

        # # reemplazar el nombre del logo y el titulo del proyecto
        # try:
        #     imagen= ''
        #     img = proyecto.avatar.url.split('/')
        #     for i in img:
        #         imagen = i
        #     stri = stri.replace('@logo', imagen)
        # except:
        #     stri = stri.replace('@logo', '')

        stri = stri.replace('@titulo', proyecto.textotitulo)

        #avatar titulo
        if proyecto.avatartitulo:
            stri = stri.replace('@avatartitulo', '<img class="alto_ancho_imagen_titulo" src="{% static ' + "'" + 'core/img/titulo.png' + "'" + '" %}">')
        else:
            stri = stri.replace('@avatartitulo', '')

        #alto ancho avatar titulo
        stri = stri.replace('@altotitulo', str(proyecto.altopixelestitulo))
        stri = stri.replace('@anchotitulo', str(proyecto.anchopixelestitulo))

        # Menu core
        stri = stri.replace('@colorfondomenu', proyecto.colorfondomenu)
        strFont = proyecto.fontmenu.split(',')
        stri = stri.replace('@fontmenucore', strFont[0])
        stri = stri.replace('@sizefontmenucorept', strFont[1])
        stri = stri.replace('@boldfontmenucore', strFont[2])
        stri = stri.replace('@colorfontmenucore', proyecto.colormenu)
        stri = stri.replace('@altomenu', str(proyecto.altomenu))

        # FONTS DE GOOGLE
        strFontsGoogle = ''
        strFont = proyecto.listafontsgoogle.split(';')
        for strf in strFont:
            strFontsGoogle += '\t<link href="https://fonts.googleapis.com/css?family=@font" rel="stylesheet">' + '\n'
            strFontsGoogle = strFontsGoogle.replace('@font', strf)
        stri = stri.replace('@fontsgoogle', strFontsGoogle)

        # CUERPO
        stri = stri.replace('@columnasizquierdacuerpo', str(proyecto.numerocolumnasizquierda))
        stri = stri.replace('@columnascentrocuerpo', str(proyecto.numerocolumnascentro))
        stri = stri.replace('@columnasderechacuerpo', str(proyecto.numerocolumnasderecha))

    except:
        print('No se reemplazo el logo')

    fd = os.open(cd + '/base.html',os.O_CREAT)
    with os.fdopen(os.open(cd + '/base.html',os.O_CREAT | os.O_RDWR ),'w') as fd:  
        fd.write(stri)
    fd.close() 

    #crear el archivo menu_core.html en includes

    cd = os.getcwd() + '/core/static/core/text_files'

    fo = open(cd + '/menu_core.html', "r+")
    stri = fo.read()

    stroa = ''
    for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):

        # Grabar el modelo si su aplicacion tiene modelos con propiedades
        flgCrear = False
        for modelo in Modelo.objects.filter(aplicacion=aplicacion):
            if Propiedad.objects.filter(modelo=modelo).count() > 0:
                flgCrear = True

        # ver si dentro de la aplicacion existe un modelo con padre='nada'
        flgPadre = False
        for modelo in Modelo.objects.filter(aplicacion=aplicacion):
            if modelo.padre == 'nada':
                flgPadre= True

        if flgCrear and flgPadre and aplicacion.nombre != 'core':
            # stroa += '\t\t\t\t\t\t<ul class="navbar-nav ">' + '\n'
            stroa += '\t\t\t\t\t\t\t<li class="nav-item  px-lg-4" >' + '\n'
            stroa += '\t\t\t\t\t\t\t\t<a class="nav-link font_opcion_menu_core text-@coloropcionmenu"  href="{%  url ' + "'" + '@aplicacion:home' + "'" + '%}">@textoenmenu</a>' + '\n'
            stroa += '\t\t\t\t\t\t\t</li>' + '\n'
            # stroa += '\t\t\t\t\t\t</ul>' + '\n'

            stroa = stroa.replace('@aplicacion', aplicacion.nombre)
            if proyecto.mayusculas:
                stroa = stroa.replace('@textoenmenu', aplicacion.textoenmenu.upper())
            else:    
                stroa = stroa.replace('@textoenmenu', aplicacion.textoenmenu)

            #color opcion menu
            stroa = stroa.replace('@coloropcionmenu', proyecto.colormenu)


    stri = stri.replace('@aplicaciones', stroa)
    if proyecto.mayusculas:
        stri = stri.replace('@proyecto', proyecto.nombre.upper())
    else:
        stri = stri.replace('@proyecto', proyecto.nombre)

    #color fondo menu
    stri = stri.replace('@colorfondomenu', proyecto.colorfondomenu)

    #bold hover
    strFont = proyecto.fontmenu.split(',')
    if strFont[2] == 'bold':
        stri = stri.replace('@boldhover', 'normal')
    else:
        stri = stri.replace('@boldhover', 'bold')

    #tiene color hover
    if proyecto.tienecolorhover:
        stri = stri.replace('@colorhover', 'background-color:' + proyecto.colorhovermenu + ';')
    else:
        stri = stri.replace('@colorhover', '')
                    

    # crear archivo menu_core.html de core
    # cd = os.getcwd() + '/' + proyecto.nombre + '/core/templates/core/includes'
    cd = proyecto.directorio + '/' + proyecto.nombre + '/core/templates/core/includes'

    try:
            os.remove( cd + "/menu_core.html")
    except:
        print('no hay archivo')

    fd = os.open(cd + '/menu_core.html',os.O_CREAT)
    with os.fdopen(os.open(cd + '/menu_core.html',os.O_CREAT | os.O_RDWR ),'w') as fd:  
        fd.write(stri)
    fd.close() 

    # archivo home.html de core    
    cd = os.getcwd() + '/core/static/core/text_files'

    fo = open(cd + '/home_core.html', "r+")
    stri = fo.read()

    # crear archivo home.html de core
    # cd = os.getcwd() + '/' + proyecto.nombre + '/core/templates/core'
    cd = proyecto.directorio + '/' + proyecto.nombre + '/core/templates/core'

    try:
            os.remove( cd + "/home.html")
    except:
        print('no hay archivo')

    fd = os.open(cd + '/home.html',os.O_CREAT)
    with os.fdopen(os.open(cd + '/home.html',os.O_CREAT | os.O_RDWR ),'w') as fd:  
        fd.write(stri)
    fd.close() 

    # crear el home.html por aplicacion
    cd = os.getcwd() + '/core/static/core/text_files'

    fo = open(cd + '/home_aplicacion.html', "r+")
    stri = fo.read()


    for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):

        # Grabar el modelo si su aplicacion tiene modelos con propiedades
        flgCrear = False
        for modelo in Modelo.objects.filter(aplicacion=aplicacion):
            if Propiedad.objects.filter(modelo=modelo).count() > 0:
                flgCrear = True

        if flgCrear and aplicacion.nombre != 'core':
            cd = proyecto.directorio + '/' + proyecto.nombre + '/' + aplicacion.nombre + '/templates/' + '/' + aplicacion.nombre

            try:
                    os.remove( cd + "/home.html")
            except:
                print('no hay archivo')

            strt = stri.replace('@aplicacion', aplicacion.nombre)

            fd = os.open(cd + '/home.html',os.O_CREAT)
            with os.fdopen(os.open(cd + '/home.html',os.O_CREAT | os.O_RDWR ),'w') as fd:  
                fd.write(strt)
            fd.close() 

    # Crear el menu para cada aplicacion
    cd = os.getcwd() + '/core/static/core/text_files'

    fo = open(cd + '/menu_aplicacion.html', "r+")
    stri = fo.read()
    strt = ''

    for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):

        # Grabar el modelo si su aplicacion tiene modelos con propiedades
        flgCrear = False
        for modelo in Modelo.objects.filter(aplicacion=aplicacion):
            if Propiedad.objects.filter(modelo=modelo).count() > 0:
                flgCrear = True

        if flgCrear:                
            if aplicacion.nombre != 'core':
                strlm = ''
                strt = stri

                # Grabar el modelo si su aplicacion tiene modelos con propiedades
                for modelo in Modelo.objects.filter(aplicacion=aplicacion):
                    if Propiedad.objects.filter(modelo=modelo).count() > 0:
                        if modelo.padre == 'nada':
                            # strlm += '\t\t\t\t\t\t<ul class="navbar-nav ">' + '\n'
                            strlm += '\t\t\t\t\t\t\t<li class="nav-item  px-lg-4" >' + '\n'
                            strlm += '\t\t\t\t\t\t\t\t<a class="nav-link font_opcion_menu_core text-@coloropcionmenu" href="{%  url ' + "'" + '@aplicacion:listar_@modelom' + "'" + ' %}">@textoopcionmenu</a>' + '\n'
                            strlm += '\t\t\t\t\t\t\t</li>' + '\n'
                            # strlm += '\t\t\t\t\t\t</ul>' + '\n'
                            strlm = strlm.replace('@modelom', modelo.nombre.lower())
                            strlm = strlm.replace('@modelo', string.capwords(modelo.nombre))
                            strlm = strlm.replace('@aplicacion', aplicacion.nombre)
                
                            #texto opcion del menu
                            if proyecto.mayusculas:
                                strlm = strlm.replace('@textoopcionmenu', modelo.textoopcionmenu.upper())
                            else:
                                strlm = strlm.replace('@textoopcionmenu', modelo.textoopcionmenu)

                            #color opcion del menu
                            strlm = strlm.replace('@coloropcionmenu', proyecto.colormenu)

                strt = strt.replace('@listamodelos', strlm)
                strt = strt.replace('@aplicacion', aplicacion.nombre)

                #color fondo del menu
                strt = strt.replace('@colorfondomenu', proyecto.colorfondomenu)

                # color de la opcion del menu    
                strt = strt.replace('@coloropcionmenu', proyecto.colormenu)

                #bold hover
                strFont = proyecto.fontmenu.split(',')
                if strFont[2] == 'bold':
                    strt = strt.replace('@boldhover', 'normal')
                else:
                    strt = strt.replace('@boldhover', 'bold')

                #tiene color hover
                if proyecto.tienecolorhover:
                    strt = strt.replace('@colorhover', 'background-color:' + proyecto.colorhovermenu + ';')
                else:
                    strt = strt.replace('@colorhover', '')
                    


                #texto opcion del menu
                if proyecto.mayusculas:
                    strt = strt.replace('@inicio', proyecto.textoopcioninicio.upper())
                else:
                    strt = strt.replace('@inicio', proyecto.textoopcioninicio)
                
                # cd = os.getcwd() + '/' + proyecto.nombre + '/' + 'core/templates/core/includes'
                cd = proyecto.directorio + '/' + proyecto.nombre + '/' + 'core/templates/core/includes'

                try:
                    os.remove( cd + '/menu_' + aplicacion.nombre + '.html')
                except:
                    print('no hay archivo')

                fd = os.open(cd + '/menu_' + aplicacion.nombre + '.html',os.O_CREAT)
                with os.fdopen(os.open(cd + '/menu_' + aplicacion.nombre + '.html',os.O_CREAT | os.O_RDWR ),'w') as fd:  
                    fd.write(strt)
                fd.close() 

    # Crear el template listar para cada modelo
    cd = os.getcwd() + '/core/static/core/text_files'

    fo = open(cd + '/modelo_listar.html', "r+")
    stri = fo.read()
    strt = ''

    for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):

        # Grabar el modelo si su aplicacion tiene modelos con propiedades
        flgCrear = False
        for modelo in Modelo.objects.filter(aplicacion=aplicacion):
            if Propiedad.objects.filter(modelo=modelo).count() > 0:
                flgCrear = True

        if flgCrear:                
            if aplicacion.nombre != 'core':

                # Grabar el modelo si su aplicacion tiene modelos con propiedades
                for modelo in Modelo.objects.filter(aplicacion=aplicacion):
                    strlr = ''
                    strlt = ''
                    strt = stri

                    if modelo.padre == 'nada':
                        for propiedad in Propiedad.objects.filter(modelo=modelo):
                            if propiedad.enlista:
                                strlt += '\t\t<div class="col-@numerocolumnas @justificacioncolumnas align-self-center">' + '\n'
                                strlt += '\t\t\t<b>@nombrecolumnapropiedad</b>' + '\n'
                                strlt += '\t\t</div>' + '\n'

                                if propiedad.tipo != 'p':
                                    strlr += '\t\t\t<div class="col-@numerocolumnas @justificacioncolumnas mt-1">' + '\n'
                                    strlr += '\t\t\t\t{{objeto.@nombrepropiedad@formatofecha}}' + '\n'
                                    strlr += '\t\t\t</div>' + '\n'
                                else:
                                    strlr += '\t\t\t<div class="col-@numerocolumnas @justificacioncolumnas mt-1">' + '\n'
                                    strlr += '\t\t\t\t{% if objeto.@nombrepropiedad %}' + '\n'
                                    strlr += '\t\t\t\t\t<img src="{{objeto.@nombrepropiedad.url}}" width="20px" height="20px" alt="">' + '\n'
                                    strlr += '\t\t\t\t{% endif %}' + '\n'
                                    strlr += '\t\t\t</div>' + '\n'
                                    
                                strlr = strlr.replace('@formatofecha', propiedad.formatofecha)
                                strlt = strlt.replace('@numerocolumnas', str(propiedad.numerocolumnas))
                                strlr = strlr.replace('@numerocolumnas', str(propiedad.numerocolumnas))
                                strlr = strlr.replace('@nombrepropiedad', propiedad.nombre)

                                # Mayusculas columna
                                if modelo.mayusculascolumnas:
                                    strlt = strlt.replace('@nombrecolumnapropiedad', propiedad.textocolumna.upper())
                                else:
                                    strlt = strlt.replace('@nombrecolumnapropiedad', propiedad.textocolumna)

                                #justificacion columnas
                                if propiedad.justificaciontextocolumna == 'i':
                                    strJusti = 'text-left'
                                if propiedad.justificaciontextocolumna == 'd':
                                    strJusti = 'text-right'
                                if propiedad.justificaciontextocolumna == 'c':
                                    strJusti = 'text-center'
                                strlt = strlt.replace('@justificacioncolumnas', strJusti)
                                strlr = strlr.replace('@justificacioncolumnas', strJusti)

                        #titulo lista
                        strFont = modelo.fonttitulolista.split(',')
                        strt = strt.replace('@fonttitulolista', strFont[0])
                        strt = strt.replace('@sizetitulolista', strFont[1])
                        strt = strt.replace('@boldtitulolista', strFont[2])
                        strt = strt.replace('@colortitulolista', modelo.colortitulolista)
                        strt = strt.replace('@colorfondotitulolista', modelo.colorfondotitulolista)
                        strt = strt.replace('@altotitulolista', str(modelo.altotitulolista))
                
                        #color fondo columnas lista
                        strt = strt.replace('@colorfondocolumnaslista', modelo.colorfondocolumnas)

                        #alto columnas lista
                        strt = strt.replace('@altocolumnaslista', str(modelo.altocolumnas))

                        #texto lista
                        strFont = modelo.fonttextolista.split(',')
                        strt = strt.replace('@fonttextolista', strFont[0])
                        strt = strt.replace('@sizetextolista', strFont[1])
                        strt = strt.replace('@boldtextolista', strFont[2])
                        strt = strt.replace('@colortextolista', modelo.colortextolista)
                        strt = strt.replace('@colorfondotextolista', modelo.colorfondotextolista)

                        strt = strt.replace('@listatitulos', strlt)
                        strt = strt.replace('@listaregistros', strlr)
                        strt = strt.replace('@aplicacion', aplicacion.nombre)
                        strt = strt.replace('@modelom', modelo.nombre.lower())
                        strt = strt.replace('@modeloM', modelo.nombre.upper())
                        strt = strt.replace('@modelo', string.capwords(modelo.nombre))

                        # TITULO LISTA
                        if modelo.mayusculastitulolista:
                            strt = strt.replace('@titulolista', modelo.titulolista.upper())
                        else:
                            strt = strt.replace('@titulolista', modelo.titulolista)

                        strFont = modelo.fonttitulolista.split(',')
                        strt = strt.replace('@fonttitulolista', strFont[0])
                        strt = strt.replace('@sizetitulolista', strFont[1])
                        strt = strt.replace('@boldtitulolista', strFont[2])
                        strt = strt.replace('@colortitulolista', modelo.colortitulolista)
                        strt = strt.replace('@colorfondotitulolista', modelo.colorfondotitulolista)

                        #justificacion horizontal
                        if modelo.justificaciontitulolista == 'i':
                            strJusti = 'text-left'
                        if modelo.justificaciontitulolista == 'd':
                            strJusti = 'text-right'
                        if modelo.justificaciontitulolista == 'c':
                            strJusti = 'text-center'
                        strt = strt.replace('@justificaciontitulolista', strJusti)

                        #justificacion vertical
                        if modelo.justificacionverticaltitulolista == 's':
                            strJusti = 'align-self-start'
                        if modelo.justificacionverticaltitulolista == 'c':
                            strJusti = 'align-self-center'
                        if modelo.justificacionverticaltitulolista == 'i':
                            strJusti = 'align-self-end'
                        strt = strt.replace('@justificacionverticaltitulolista', strJusti)

                        if modelo.bordeinferior:
                            strt = strt.replace('@bordeinferiorlista', 'lightgray')
                        else:
                            strt = strt.replace('@bordeinferiorlista', 'transparent')

                        # columnas
                        print(modelo.nombre)
                        print(modelo.fontcolumnas)
                        strFont = modelo.fontcolumnas.split(',')
                        strt = strt.replace('@fontcolumnaslista', strFont[0])
                        strt = strt.replace('@sizecolumnaslista', strFont[1])
                        strt = strt.replace('@boldcolumnaslista', strFont[2])
                        strt = strt.replace('@colorcolumnaslista', modelo.colorcolumnas)

                        #editar borrar
                        strFont = modelo.fonteditarborrar.split(',')
                        strt = strt.replace('@fonteditarmodelo', strFont[0])
                        strt = strt.replace('@sizeeditarmodelo', strFont[1])
                        strt = strt.replace('@boldeditarmodelo', strFont[2])
                        strt = strt.replace('@coloreditarmodelo', modelo.coloreditarborrar)

                        strteb = modelo.textoeditarborrar.split(',')
                        strt = strt.replace('@textoeditar', strteb[0])
                        strt = strt.replace('@textoborrar', strteb[1])

                        #link nuevo
                        strFont = modelo.fontlinknuevo.split(',')
                        strt = strt.replace('@fontlinknuevomodelomodelo', strFont[0])
                        strt = strt.replace('@sizelinknuevomodelo', strFont[1])
                        strt = strt.replace('@boldlinknuevomodelo', strFont[2])
                        strt = strt.replace('@colorlinknuevomodelo', modelo.colorlinknuevo)
                        strt = strt.replace('@textolinknuevomodelo', modelo.textolinknuevo)

                        #link boton
                        if modelo.linkboton:
                            strt = strt.replace('@linkboton', 'btn btn-' + modelo.colorbotonlinknuevo)
                        else:
                            strt = strt.replace('@linkboton', '')

                        # cd = os.getcwd() + '/' + proyecto.nombre + '/' + aplicacion.nombre + '/' + 'templates/' + aplicacion.nombre 
                        cd = proyecto.directorio + '/' + proyecto.nombre + '/' + aplicacion.nombre + '/' + 'templates/' + aplicacion.nombre 

                        try:
                            os.remove( cd + '/' + modelo.nombre + '_list.html')
                        except:
                            print('no hay archivo')

                        fd = os.open(cd + '/' + modelo.nombre + '_list.html',os.O_CREAT)
                        with os.fdopen(os.open(cd + '/' + modelo.nombre + '_list.html',os.O_CREAT | os.O_RDWR ),'w') as fd:  
                            fd.write(strt)
                        fd.close() 

    # Crear el template form para cada modelo
    cd = os.getcwd() + '/core/static/core/text_files'

    fo = open(cd + '/modelo_form.html', "r+")
    stri = fo.read()
    strt = ''

    for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):

        # Grabar el modelo si su aplicacion tiene modelos con propiedades
        flgCrear = False
        for modelo in Modelo.objects.filter(aplicacion=aplicacion):
            if Propiedad.objects.filter(modelo=modelo).count() > 0:
                flgCrear = True

        if flgCrear and aplicacion.nombre!= 'core':                

            for modelo in Modelo.objects.filter(aplicacion=aplicacion):
                strt = stri            
                strt = strt.replace('@aplicacion', aplicacion.nombre)
                strt = strt.replace('@modelom', modelo.nombre.lower())
                strt = strt.replace('@modeloM', modelo.nombre.upper())
                strt = strt.replace('@modelo', string.capwords(modelo.nombre))
                
                # codigo para la opcion referencia form
                stra = ''

                if modelo.padre == 'nada':
                    stra += '@textotitulopagina' + '\n'
                else:    
                    modelo_padre = Modelo.objects.get(nombre=modelo.padre , proyecto=proyecto)
                    if modelo_padre.padre != 'nada': # el modelo es nieto
                        modelo_abuelo = Modelo.objects.get(nombre=modelo_padre.padre , proyecto=proyecto)

                        # stra += '<div class="row font_encabezado mb-3">' + '\n'
                        stra += '<div class="col">' + '\n'
                        stra += '<div class="" style="float: left;">NUEVO @modeloM&nbsp&nbsp</div>' + '\n'
                        stra += '<div class=""><a href="{% url ' + "'" + '@aplicacionpadrem:editar_@modelopadrem' + "'" + ' @modelopadrem_id %}?@modeloabuelom_id={{@modeloabuelom_id}}">(Volver)</a></div>' + '\n'
                        stra += '</div>' + '\n'
                        # stra += '</div>' + '\n'

                        # stra =  modelo.nombre.upper() + ': <b>{{nombre}}</b>&nbsp&nbsp<a href="{% url ' + "'" + '@aplicacionpadrem:editar_@modelopadrem' + "'" + ' @modelopadrem_id %}?@modeloabuelom_id={{@modeloabuelom_id}}">(Volver)</a>'
                        stra = stra.replace('@modeloabuelom', modelo_abuelo.nombre.lower())        
                    else: # el modelo es hijo
                        # stra += '<div class="row font_encabezado mb-3 ">' + '\n'
                        stra += '<div class="col">' + '\n'
                        stra += '<div class="" style="float: left">NUEVO @modeloM</div>' + '\n'
                        stra += '<div class="" >&nbsp&nbsp<a href="{% url ' + "'" + '@aplicacionpadrem:editar_@modelopadrem' + "'" + ' @modelopadrem_id %}">(Volver)</a></div>' + '\n'
                        stra += '</div>' + '\n'
                        # stra += '</div>' + '\n'

                        # stra = modelo.nombre + ': <b>{{nombre}}</b>&nbsp&nbsp<a href="{% url ' + "'" + '@aplicacionpadrem:editar_@modelopadrem' + "'" + ' @modelopadrem_id %}">(Volver)</a>'
                    stra = stra.replace('@aplicacionpadrem', Aplicacion.objects.get(id=modelo_padre.aplicacion.id).nombre.lower())        
                    stra = stra.replace('@modelopadrem', modelo_padre.nombre.lower())        

                stra = stra.replace('@modeloM', modelo.nombre.upper())        

                strt = strt.replace('@referenciaform', stra)

                #titulo pagina
                strFont = modelo.fonttextotitulopagina.split(',')
                strt = strt.replace('@fonttextotitulopagina', strFont[0])
                strt = strt.replace('@sizetextotitulopagina', strFont[1])
                strt = strt.replace('@boldtextotitulopagina', strFont[2])
                strt = strt.replace('@colortextotitulopagina', modelo.colortextotitulopagina)
                strt = strt.replace('@textotitulopagina', modelo.textotitulopagina)

                # columnas
                strt = strt.replace('@numerocolumnasizquierdanuevo', str(modelo.numerocolumnasizquierdanuevo))
                strt = strt.replace('@numerocolumnasmodelonuevo', str(modelo.numerocolumnasmodelonuevo))
                strt = strt.replace('@numerocolumnasderechanuevo', str(modelo.numerocolumnasderechanuevo))

                strt =  Etiquetas(modelo,strt)

                # #etiquetas
                # strFont = modelo.fontetiqueta.split(',')
                # strt = strt.replace('@fontlabelmodelo', strFont[0])
                # strt = strt.replace('@sizelabelmodelo', strFont[1])
                # strt = strt.replace('@boldlabelmodelo', strFont[2])
                # strt = strt.replace('@colorlabelmodelo', modelo.coloretiqueta)

                # # controles
                # if modelo.controlesautomaticos:
                #     strt = strt.replace('@controles', '{{form.as_p}}')
                # else:
                #     strctl = ''
                #     for propiedad in Propiedad.objects.filter(modelo=modelo):
                #         strctl += '\t\t\t\t\t<div class="row" >' + '\n'
                #         strctl += '\t\t\t\t\t\t<div class="col font_label_' + modelo.nombre.lower() + '">' + propiedad.etiqueta + '</div>' + '\n'
                #         strctl += '\t\t\t\t\t</div>' + '\n'
                #         strctl += '\t\t\t\t\t<div class="row mb-4">' + '\n'
                #         strctl += '\t\t\t\t\t\t<div class="col">' + '\n'
                #         strctl += '\t\t\t\t\t\t\t{{form.' + propiedad.nombre + '}}' + '\n'
                #         strctl += '\t\t\t\t\t\t</div>' + '\n'
                #         strctl += '\t\t\t\t\t</div>' + '\n'
                    
                #     strt = strt.replace('@controles', strctl)


                # cd = os.getcwd() + '/' + proyecto.nombre + '/' + aplicacion.nombre + '/' + 'templates/' + aplicacion.nombre 
                cd = proyecto.directorio + '/' + proyecto.nombre + '/' + aplicacion.nombre + '/' + 'templates/' + aplicacion.nombre 

                try:
                    os.remove( cd + '/' + modelo.nombre + '_form.html')
                except:
                    print('no hay archivo')

                fd = os.open(cd + '/' + modelo.nombre + '_form.html',os.O_CREAT)
                with os.fdopen(os.open(cd + '/' + modelo.nombre + '_form.html',os.O_CREAT | os.O_RDWR ),'w') as fd:  
                    fd.write(strt)
                fd.close() 

    # Crear el template update para cada modelo
    cd = os.getcwd() + '/core/static/core/text_files'

    fo = open(cd + '/modelo_update_allado.html', "r+")

    stri = fo.read()
    strt = ''

    for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):

        # Grabar el modelo si su aplicacion tiene modelos con propiedades
        flgCrear = False
        for modelo in Modelo.objects.filter(aplicacion=aplicacion):
            if Propiedad.objects.filter(modelo=modelo).count() > 0:
                flgCrear = True

        if flgCrear and aplicacion.nombre!= 'core':                

            for modelo in Modelo.objects.filter(aplicacion=aplicacion):

                cd = os.getcwd() + '/core/static/core/text_files'
                if modelo.hijoscontiguos:
                    fo = open(cd + '/modelo_update_allado.html', "r+")
                    stri = fo.read()
                else:
                    fo = open(cd + '/modelo_update.html', "r+")
                    stri = fo.read()

                strt = stri            
                strt = strt.replace('@aplicacion', aplicacion.nombre)
                strt = strt.replace('@modelom', modelo.nombre.lower())
                strt = strt.replace('@modeloM', modelo.nombre.upper())
                strt = strt.replace('@modelo', string.capwords(modelo.nombre))
                
                for propiedad in Propiedad.objects.filter(modelo=modelo):
                    if propiedad.enlista:
                        strt = strt.replace('@nombre', modelo.nombre + '.' + propiedad.nombre)
                        break

                # codigo para la referencia del form
                stra = ''

                if modelo.padre =='nada': # modelo padre
                    stra = '\t\t\t\t\t\t\t<div class="col">@modeloM: {{nombre}}</div>' 
                else:
                    modelo_padre = Modelo.objects.get(nombre=modelo.padre , proyecto=proyecto)
                    if modelo_padre.padre != 'nada': # el modelo es nieto
                        modelo_abuelo = Modelo.objects.get(nombre=modelo_padre.padre , proyecto=proyecto)
                        stra += '\t\t\t\t\t\t\t<div class="col">' + '\n'
                        stra += '\t\t\t\t\t\t\t\t<div class="" style="float: left">@modeloM:&nbsp&nbsp</div>' +'\n'
                        stra += '\t\t\t\t\t\t\t\t<div class="" style="float: left;"><b>{{nombre}}</b>&nbsp&nbsp</div>' + '\n'
                        stra += '\t\t\t\t\t\t\t\t<div class="" style="float: left;"><a href="{% url ' + "'" + '@aplicacionpadrem:editar_@modelopadrem' + "'" + ' @modelopadrem_id %}?@modeloabuelom_id={{@modeloabuelom_id}}">(Volver)</a></div>' + '\n'
                        stra += '\t\t\t\t\t\t\t</div>'
                        # stra =  modelo.nombre.upper() + ': <b>{{nombre}}</b>&nbsp&nbsp<a href="{% url ' + "'" + '@aplicacionpadrem:editar_@modelopadrem' + "'" + ' @modelopadrem_id %}?@modeloabuelom_id={{@modeloabuelom_id}}">(Volver)</a>'
                        stra = stra.replace('@modeloabuelom', modelo_abuelo.nombre.lower())        
                    else: # el modelo es hijo
                        stra += '\t\t\t\t\t\t\t<div class="col text-center">' + '\n'
                        stra += '\t\t\t\t\t\t\t\t<div class="" style="float: left;">@modeloM:&nbsp&nbsp</div>&nbsp' + '\n'
                        stra += '\t\t\t\t\t\t\t\t<div class="" style="float: left"><b>{{nombre}}&nbsp&nbsp</b></div>' + '\n'
                        stra += '\t\t\t\t\t\t\t\t<div class="" style="float: left"><a href="{% url ' + "'" + '@aplicacionpadrem:editar_@modelopadrem' + "'" + ' @modelopadrem_id %}">(Volver)</a></div>' + '\n'
                        stra += '\t\t\t\t\t\t\t</div>'

                            # stra = modelo.nombre + ': <b>{{nombre}}</b>&nbsp&nbsp<a href="{% url ' + "'" + '@aplicacionpadrem:editar_@modelopadrem' + "'" + ' @modelopadrem_id %}">(Volver)</a>'
                    stra = stra.replace('@aplicacionpadrem', Aplicacion.objects.get(id=modelo_padre.aplicacion.id).nombre.lower())        
                    stra = stra.replace('@modelopadrem', modelo_padre.nombre.lower())        

                stra = stra.replace('@modeloM', modelo.nombre.upper())        

                strt = strt.replace('@referenciaform', stra)


                #lista de modelos hijos
                strh = ''
                strBordeHijos = ''
                strffc = ''
                for modelohijo in Modelo.objects.filter(padre=modelo.nombre , proyecto = proyecto):
                    strBordeHijos = 'border'
                    strlh = '\t\t\t\t<div class="container-fluid">' + '\n'

                    strlh += '\t\t\t\t\t<div class="row mt-2 mb-2 font_texto_titulo_lista_@modelom fondo_titulo_lista_@modelom @justificaciontitulolista alto_titulo_lista_hijos_@modelom">' + '\n'
                    strlh += '\t\t\t\t\t\t<div class="col @justificacionverticaltitulolistahijos">' + '\n'
                    strlh += '\t\t\t\t\t\t\t<b>@titulolistahijo</b>' + '\n'
                    strlh += '\t\t\t\t\t\t</div>' + '\n'
                    strlh += '\t\t\t\t\t</div>' + '\n'

                    strlh += '\t\t\t\t\t<div class="row font_columnas_hijos_@modelom borde_inferior borde_superior fondo_columnas_@modelom alto_columnas_hijos_@modelom" >' + '\n'
                    strlh += '\t\t\t\t\t\t{% if numero' + modelohijo.nombre + ' > 0 %}' + '\n'
                    strlh += '@columnashijo' + '\n'
                    strlh += '\t\t\t\t\t\t{% endif %}' + '\n'
                    strlh += '\t\t\t\t\t</div>' + '\n'
                    strlh += '\t\t\t\t\t<div class="row  font_lista" style="background-color: #f1f1f1">' + '\n'
                    strlh += '\t\t\t\t\t\t{% for objeto in lista@hijo %}' + '\n'
                    strlh += '@listaregistroshijo' + '\n'
                    strlh += '\t\t\t\t\t\t\t<div class="col-1 mt-1">' + '\n'
                    strlh += '\t\t\t\t\t\t\t\t@editahijo' + '\n'
                    strlh += '\t\t\t\t\t\t\t</div>' + '\n'
                    strlh += '\t\t\t\t\t\t\t<div class="col-1 ml-2 mt-1">' + '\n'
                    strlh += '\t\t\t\t\t\t\t\t@borrahijo' + '\n'
                    strlh += '\t\t\t\t\t\t\t</div>' + '\n'
                    strlh += '\t\t\t\t\t\t\t<div class="col-1">' + '\n'
                    strlh += '\t\t\t\t\t\t\t</div>' + '\n'
                    strlh += '\t\t\t\t\t\t{% endfor %}' + '\n'
                    strlh += '\t\t\t\t\t</div>' + '\n'
                    strlh += '\t\t\t\t\t<div class="row mt-3 font_lista font-weight-bold">' + '\n'
                    strlh += '\t\t\t\t\t\t<div class="col">' + '\n'
                    strlh += '\t\t\t\t\t\t\t<a class="btn btn-warning btn-block mt-2" href="{% url ' + "'" + '@aplicacionhijo:crear_@hijo' + "'" + '%}?@modelopadrem_id={{ @modelopadrem.id }}">Nuevo registro @hijo</a>' + '\n' + '\n'
                    strlh += '\t\t\t\t\t\t</div>' + '\n'
                    strlh += '\t\t\t\t\t</div>' + '\n'
                    strlh += '\t\t\t\t</div>' + '\n'

                    strlrh = ''
                    strlth = ''

                    # lista hijos
                    for propiedadhijo in Propiedad.objects.filter(modelo=modelohijo):
                        if propiedadhijo.enlista:
                            strlth += '\t\t\t\t\t\t<div class="col-' + str(propiedadhijo.numerocolumnas) + ' @justificaciontextocolumnas align-self-center">' + '\n'

                            if modelohijo.mayusculascolumnaslistahijos:
                                strlth += '\t\t\t\t\t\t\t' + propiedadhijo.textocolumna.upper() + '\n'
                            else:
                                strlth += '\t\t\t\t\t\t\t' + propiedadhijo.textocolumna + '\n'

                            strlth += '\t\t\t\t\t\t</div>' + '\n'

                            strlrh += '\t\t\t\t\t\t<div class="col-' + str(propiedadhijo.numerocolumnas) + ' @justificaciontextocolumnas mt-1">' + '\n'
                            strlrh += '\t\t\t\t\t\t\t\t{{objeto.' + propiedadhijo.nombre + propiedadhijo.formatofecha + '}}' + '\n'
                            strlrh += '\t\t\t\t\t\t</div>' + '\n'

                            #justificacion columnas
                            if propiedadhijo.justificaciontextocolumna == 'i':
                                strJusti = 'text-left'
                            if propiedadhijo.justificaciontextocolumna == 'd':
                                strJusti = 'text-right'
                            if propiedadhijo.justificaciontextocolumna == 'c':
                                strJusti = 'text-center'
                            strlth = strlth.replace('@justificaciontextocolumnas', strJusti)

                    # editar y borrar hijos
                    streh = ''
                    strbh = ''
                    if modelohijo.padre != 'nada': # modelo hijo o nieto
                        modelo_padre = Modelo.objects.get(nombre=modelohijo.padre , proyecto=proyecto)
                        if modelo_padre.padre != 'nada': # modelo nieto
                            modelo_abuelo = Modelo.objects.get(nombre=modelo_padre.padre , proyecto=proyecto)
                            streh += '<a href="{% url ' + "'" + '@aplicacionhijo:editar_@hijo' + "'" + ' objeto.id %}?@modelopadrem_id={{ @modelopadrem_id }}&@modeloabuelom_id={{@modeloabuelom_id}}">Editar</a>' + '\n'
                            strbh += '<a href="{% url ' + "'" + '@aplicacionhijo:borrar_@hijo' + "'" + ' objeto.id %}?@modelopadrem_id={{ @modelopadrem_id }}&@modeloabuelom_id={{@modeloabuelom_id}}">Borrar</a>' + '\n'
                            streh = streh.replace('@modeloabuelom', modelo_abuelo.nombre.lower())
                            strbh = strbh.replace('@modeloabuelom', modelo_abuelo.nombre.lower())
                        else: # modelo hijo
                            streh += '<a href="{% url ' + "'" + '@aplicacionhijo:editar_@hijo' + "'" + ' objeto.id %}?@modelopadrem_id={{ @modelopadrem_id }}">Editar</a>' + '\n'
                            strbh += '<a href="{% url ' + "'" + '@aplicacionhijo:borrar_@hijo' + "'" + ' objeto.id %}?@modelopadrem_id={{ @modelopadrem_id }}">Borrar</a>' + '\n'
                        streh = streh.replace('@modelopadrem', modelo_padre.nombre.lower())
                        strbh = strbh.replace('@modelopadrem', modelo_padre.nombre.lower())
                    else: # modelo sin padre
                        streh += '<a href="{% url ' + "'" + '@aplicacionhijo:editar_@hijo' + "'" + ' objeto.id %}?@modelom_id={{ @modelom.id }}">Editar</a>' + '\n'
                        strbh += '<a href="{% url ' + "'" + '@aplicacionhijo:borrar_@hijo' + "'" + ' objeto.id %}?@modelom_id={{ @modelom.id }}">Borrar</a>' + '\n'
                        streh = streh.replace('@modelom', modelohijo.nombre.lower())
                        strbh = strbh.replace('@modelom', modelohijo.nombre.lower())
                        
                    strlh = strlh.replace('@editahijo', streh)
                    strlh = strlh.replace('@borrahijo', strbh)
                    strlh = strlh.replace('@modelopadrem', modelo.nombre.lower())
                    strlh = strlh.replace('@modeloM', modelohijo.nombre.upper())
                    strlh = strlh.replace('@modelom', modelohijo.nombre.lower())
                    strlh = strlh.replace('@modelohijom', modelohijo.nombre.lower())
                    strlh = strlh.replace('@hijo', modelohijo.nombre)
                    strlh = strlh.replace('@aplicacionhijo', modelohijo.aplicacion.nombre.lower())
                    strlh = strlh.replace('@columnashijo', strlth)
                    strlh = strlh.replace('@listaregistroshijo', strlrh)


                    # justificacion vertical titulo lista hijos
                    if modelohijo.justificacionverticaltitulolistahijos == 's':
                        strJusti = 'align-self-start'
                    if modelohijo.justificacionverticaltitulolistahijos == 'c':
                        strJusti = 'align-self-center'
                    if modelohijo.justificacionverticaltitulolistahijos == 'i':
                        strJusti = 'align-self-end'
                    strlh = strlh.replace('@justificacionverticaltitulolistahijos', strJusti)

                    #justificacion horizaontal
                    if modelohijo.justificaciontitulolistahijos == 'i':
                        strJusti = 'text-left'
                    if modelohijo.justificaciontitulolistahijos == 'd':
                        strJusti = 'text-right'
                    if modelohijo.justificaciontitulolistahijos == 'c':
                        strJusti = 'text-center'
                    strlh = strlh.replace('@justificaciontitulolista', strJusti)

                    #titulo lista hijo
                    if modelohijo.mayusculastitulolistahijos:
                        strlh = strlh.replace('@titulolistahijo', modelohijo.textotitulolistahijos.upper())
                    else:
                        strlh = strlh.replace('@titulolistahijo', modelohijo.textotitulolistahijos)

                    # fondo, font y color de la lista de hijos

                    strffc += '\t\t.font_texto_titulo_lista_@modelom{font-family:  @font; font-size: @sizept; font-weight: @bold;color:@color;}' + '\n'
                    strffc += '\t\t.fondo_titulo_lista_@modelom{background-color: @colorfondotitulolistahijos}' + '\n'
                    strffc += '\t\t.font_columnas_hijos_@modelom{font-family:  @fontcolumnashijos; font-size: @sizecolumnashijospt; font-weight: @boldcolumnashijos;color:@colorcolumnashijos;}' + '\n'
                    strffc += '\t\t.fondo_columnas_@modelom{background-color: @fondocolumnashijos}' + '\n'
                    strffc += '\t\t.alto_titulo_lista_hijos_@modelom{height: @altotitulolistahijospx}' + '\n'
                    strffc += '\t\t.alto_columnas_hijos_@modelom{height: @altocolumnaslistahijospx}' + '\n'

                    strFont = modelohijo.fontcolumnaslistahijos.split(',')
                    strffc = strffc.replace('@fontcolumnashijos', strFont[0])
                    strffc = strffc.replace('@sizecolumnashijos', strFont[1])
                    strffc = strffc.replace('@boldcolumnashijos', strFont[2])
                    strffc = strffc.replace('@colorcolumnashijos', modelohijo.colorcolumnaslistahijos)
                    strffc = strffc.replace('@fondocolumnashijos', modelohijo.fondocolumnaslistahijos)
                    strffc = strffc.replace('@colorfondotitulolistahijos', modelohijo.colorfondotitulolistahijos)
                    strffc = strffc.replace('@altotitulolistahijos', str(modelohijo.altotitulolistahijos))
                    strffc = strffc.replace('@altocolumnaslistahijos', str(modelohijo.altocolumnaslistahijos))

                    strFont = modelohijo.fonttextotitulolistahijos.split(',')
                    strffc = strffc.replace('@font', strFont[0])
                    strffc = strffc.replace('@size', strFont[1])
                    strffc = strffc.replace('@bold', strFont[2])
                    strffc = strffc.replace('@color', modelohijo.colortextolistahijos)

                    strffc = strffc.replace('@modelom', modelohijo.nombre.lower())

                    strh += strlh
                    
                strt = strt.replace('@listahijos', strh)
                strt = strt.replace('@stylelistahijos', strffc)
                strt = strt.replace('@bordehijos', strBordeHijos)
                strt = strt.replace('@numerocolumnasizquierdaedicion', str(modelo.numerocolumnasizquierdaedicion))
                strt = strt.replace('@numerocolumnasderechaedicion', str(modelo.numerocolumnasderechaedicion))
                strt = strt.replace('@numerocolumnasmodeloedicion', str(modelo.numerocolumnasmodeloedicion))
                strt = strt.replace('@numerocolumnashijosedicion', str(modelo.numerocolumnashijosedicion))
                
                #etiquetas
                strt = Etiquetas(modelo,strt)

                # if modelo.padre != 'nada':

                # cd = os.getcwd() + '/' + proyecto.nombre + '/' + aplicacion.nombre + '/' + 'templates/' + aplicacion.nombre 
                cd = proyecto.directorio + '/' + proyecto.nombre + '/' + aplicacion.nombre + '/' + 'templates/' + aplicacion.nombre 

                try:
                    os.remove( cd + '/' + modelo.nombre + '_update_form.html')
                except:
                    print('no hay archivo')
                fd = os.open(cd + '/' + modelo.nombre + '_update_form.html',os.O_CREAT)
                with os.fdopen(os.open(cd + '/' + modelo.nombre + '_update_form.html',os.O_CREAT | os.O_RDWR ),'w') as fd:  
                    fd.write(strt)
                fd.close() 

    # Crear el template confirm delete para cada modelo
    cd = os.getcwd() + '/core/static/core/text_files'

    fo = open(cd + '/modelo_confirm_delete.html', "r+")
    stri = fo.read()
    strt = ''

    for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):

        # Grabar el modelo si su aplicacion tiene modelos con propiedades
        flgCrear = False
        for modelo in Modelo.objects.filter(aplicacion=aplicacion):
            if Propiedad.objects.filter(modelo=modelo).count() > 0:
                flgCrear = True

        if flgCrear and aplicacion.nombre!= 'core':                

            for modelo in Modelo.objects.filter(aplicacion=aplicacion):
                strt = stri            

                # definir la vista de retorno
                if modelo.padre =='nada':
                    strt = strt.replace('@vistadespues', 'listar_@modelom')
                else:
                    strt = strt.replace('@vistadespues', 'listar_@modelom')


                # cancelar el borrado
                strcb = ''
                if modelo.padre != 'nada': # modelo hijo o nieto
                    modelo_padre = Modelo.objects.get(nombre=modelo.padre , proyecto=proyecto)
                    if modelo_padre.padre != 'nada': # modelo nieto
                        modelo_abuelo = Modelo.objects.get(nombre=modelo_padre.padre , proyecto=proyecto)
                        strcb = '<a class="btn btn-danger" href="{% url ' + "'" + '@aplicacionpadre:editar_@modelopadrem' + "'" + ' @modelopadrem_id %}?@modeloabuelom_id={{@modeloabuelom_id}}">Cancelar</a>'
                        strcb = strcb.replace('@modeloabuelom', modelo_abuelo.nombre)
                    else: # modelo hijo
                        strcb = '<a class="btn btn-danger" href="{% url ' + "'" + '@aplicacionpadre:editar_@modelopadrem' + "'" + ' @modelopadrem_id %}">Cancelar</a>'
                    strcb = strcb.replace('@aplicacionpadre', Aplicacion.objects.get(id=modelo_padre.aplicacion.id).nombre)
                    strcb = strcb.replace('@modelopadrem', modelo_padre.nombre)
                else: # modelo sin padre
                    strcb = '<a class="btn btn-danger" href="{% url ' + "'" + '@aplicacion:listar_@modelom' + "'" + ' %}">Cancelar</a>'
                    strcb = strcb.replace('@aplicacion', Aplicacion.objects.get(id=modelo.aplicacion.id).nombre)

                # font texto borrado
                strFont = modelo.fonttextoborrado.split(',')
                strt = strt.replace('@fonttextoborrado', strFont[0])
                strt = strt.replace('@sizetextoborrado', strFont[1])
                strt = strt.replace('@boldtextoborrado', strFont[2])
                strt = strt.replace('@colortextoborrado', modelo.colortextoborrado)

                strt = strt.replace('@cancelaborrado', strcb)
                strt = strt.replace('@textoborrado', modelo.textoborrado)
                strt = strt.replace('@textobotonborrado', modelo.textobotonborrado)
                strt = strt.replace('@aplicacion', aplicacion.nombre)
                strt = strt.replace('@modelom', modelo.nombre.lower())
                strt = strt.replace('@modeloM', modelo.nombre.upper())
                strt = strt.replace('@modelo', string.capwords(modelo.nombre))

                # cd = os.getcwd() + '/' + proyecto.nombre + '/' + aplicacion.nombre + '/' + 'templates/' + aplicacion.nombre 
                cd = proyecto.directorio + '/' + proyecto.nombre + '/' + aplicacion.nombre + '/' + 'templates/' + aplicacion.nombre 

                try:
                    os.remove( cd + '/' + modelo.nombre + '_confirm_delete.html')
                except:
                    print('no hay archivo')
                fd = os.open(cd + '/' + modelo.nombre + '_confirm_delete.html',os.O_CREAT)
                with os.fdopen(os.open(cd + '/' + modelo.nombre + '_confirm_delete.html',os.O_CREAT | os.O_RDWR ),'w') as fd:  
                    fd.write(strt)
                fd.close()     

def Etiquetas(modelo,strt):
    #etiquetas
    strFont = modelo.fontetiqueta.split(',')
    strt = strt.replace('@fontlabelmodelo', strFont[0])
    strt = strt.replace('@sizelabelmodelo', strFont[1])
    strt = strt.replace('@boldlabelmodelo', strFont[2])
    strt = strt.replace('@colorlabelmodelo', modelo.coloretiqueta)

    # controles
    if modelo.controlesautomaticos:
        strt = strt.replace('@controles', '{{form.as_p}}')
    else:
        strctl = ''
        for propiedad in Propiedad.objects.filter(modelo=modelo):
            if propiedad.etiquetaarriba:
                strctl += '\t\t\t\t\t<div class="row" >' + '\n'
                strctl += '\t\t\t\t\t\t<div class="col font_label_' + modelo.nombre.lower() + '">' + propiedad.etiqueta + '</div>' + '\n'
                strctl += '\t\t\t\t\t</div>' + '\n'
                if propiedad.tipo == 'p': 
                    strctl += '\t\t\t\t\t<div class="row">' + '\n'
                    strctl += '\t\t\t\t\t\t<div class="col">' + '\n'
                    strctl += '\t\t\t\t\t\t\t{% if ' + modelo.nombre + '.' + propiedad.nombre + ' %}' + '\n'
                    strctl += '\t\t\t\t\t\t\t\t<img src="{{' + modelo.nombre + '.' + propiedad.nombre + '.url}}" width="50px" height="50px" alt="">' + '\n'
                    strctl += '\t\t\t\t\t\t\t{% endif %}' + '\n'
                    strctl += '\t\t\t\t\t\t</div>' + '\n'
                    strctl += '\t\t\t\t\t</div>' + '\n'
                strctl += '\t\t\t\t\t<div class="row mb-4">' + '\n'
                strctl += '\t\t\t\t\t\t<div class="col">' + '\n'
                strctl += '\t\t\t\t\t\t\t{{form.' + propiedad.nombre + '}}' + '\n'
                strctl += '\t\t\t\t\t\t</div>' + '\n'
                strctl += '\t\t\t\t\t</div>' + '\n'
            else:
                strctl += '\t\t\t\t\t<div class="row" >' + '\n'
                strctl += '\t\t\t\t\t\t<div class="col-5 font_label_' + modelo.nombre.lower() + '">' + propiedad.etiqueta + '</div>' + '\n'
                strctl += '\t\t\t\t\t\t<div class="col-7">' + '\n'
                strctl += '\t\t\t\t\t\t\t{{form.' + propiedad.nombre + '}}' + '\n'
                strctl += '\t\t\t\t\t\t</div>' + '\n'
                strctl += '\t\t\t\t\t</div>' + '\n'

        strt = strt.replace('@controles', strctl)

    return strt

def CopiaImagenes(destino,upload,url):
    try:
        #borrar el destino
        try:
            os.remove( destino)
        except Exception as e:
            print(e)

        print('11')
        img = url.split('/')
        imagen = ''
        for i in img:
            imagen = i
        origen = os.getcwd() + '/media/' + upload + '/' + imagen
        print('12')
        if os.path.exists(origen):
            with open(origen, 'rb') as forigen:
                with open(destino, 'wb') as fdestino:
                    shutil.copyfileobj(forigen, fdestino)
    except Exception as e:
        print(e)

class CrearSeguridadView(FormView):
    template_name = "crear/CrearSeguridad.html"
    form_class = CrearForm
    model = Crear

    def get_success_url(self):
        return reverse_lazy('crear:proyecto') + '?proyecto_id='+ self.request.GET['proyecto_id']

    def get_context_data(self,**kwargs):
        context = super(CrearSeguridadView, self).get_context_data(**kwargs)
        context['lista'] = ListaCrear(self.request.GET['proyecto_id'])
        context['proyecto_id'] = self.request.GET['proyecto_id']
        return context      

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        proyecto = Proyecto.objects.get(id = request.GET['proyecto_id'])

        # ante de crear la seguridad verificar que el proyecto tenga aplicaciones
        if Aplicacion.objects.filter(proyecto=proyecto).count() > 0:
            if proyecto.conseguridad:
                CrearSeguridad(proyecto)

        return HttpResponseRedirect(self.get_success_url())

def CrearSeguridad(proyecto):

    # aplicaciones seguridad
    # borrar si existiera un registro de aplicacion registration
    try:
        aplicacion = Aplicacion.objects.filter(nombre='registration', proyecto=proyecto)
        aplicacion.delete()
    except:
        none

    #crear un registro registraion
    aplicacion = Aplicacion.objects.create(nombre='registration',proyecto=proyecto,textoenmenu='seguiridad')
    aplicacion.save()

    # crear los directorios
    cd = proyecto.directorio + '/' + proyecto.nombre
    try:               
        os.mkdir(cd + '/' + 'registration') 
    except:
        print ('ya existe ' + 'registration')

    cd = proyecto.directorio + '/' + proyecto.nombre + '/registration'
    try:               
        os.mkdir(cd + '/' + 'templates') 
    except:
        print ('ya existe ' + 'templates')

    cd = proyecto.directorio + '/' + proyecto.nombre + '/registration/templates'
    try:               
        os.mkdir(cd + '/' + 'registration') 
    except:
        print ('ya existe ' + 'registration')

    # modificar archivo settings.py  del proyecto con el nombre de la aplicacion registration
    cd = proyecto.directorio + '/' + proyecto.nombre + '/' + proyecto.nombre 
    fo = open(cd + '/settings.py', "r+")
    stri = fo.read()
    
    stri = stri.replace('#@registration', "'" + 'registration' + "'" + ',')

    try:
        os.remove( cd + "/settings.py")
    except:
        print('no hay archivo')
    
    fd = os.open(cd + '/settings.py',os.O_CREAT)
    with os.fdopen(os.open(cd + '/settings.py',os.O_CREAT | os.O_RDWR ),'w') as fd:  
        fd.write(stri)
    fd.close() 

    # forms.py seguridad
    if proyecto.conseguridad:
        cd = os.getcwd() + '/core/static/core/text_files/registration'

        try:

            # leer archivo modelo.py de core/text_files
            fo = open(cd + '/forms.py', "r+")
            stri = fo.read()

            cd = proyecto.directorio + '/' + proyecto.nombre + '/' + 'registration' 

            try:
                os.remove( cd + "/forms.py")
            except:
                print('no hay archivo')

            fd = os.open(cd + '/forms.py',os.O_CREAT)
            with os.fdopen(os.open(cd + '/forms.py',os.O_CREAT | os.O_RDWR ),'w') as fd:  
                fd.write(stri)
            fd.close()    

        except:
            print('No existe la aplicacion registration')

    # views.py seguridad
    if proyecto.conseguridad:
        cd = os.getcwd() + '/core/static/core/text_files/registration'

        try:

            # leer archivo modelo.py de core/text_files
            fo = open(cd + '/views.py', "r+")
            stri = fo.read()

            cd = proyecto.directorio + '/' + proyecto.nombre + '/' + 'registration' 

            try:
                os.remove( cd + "/views.py")
            except:
                print('no hay archivo')

            fd = os.open(cd + '/views.py',os.O_CREAT)
            with os.fdopen(os.open(cd + '/views.py',os.O_CREAT | os.O_RDWR ),'w') as fd:  
                fd.write(stri)
            fd.close()    

        except:
            print('No existe la aplicacion registration')

    # models.py seguridad
    if proyecto.conseguridad:
        cd = os.getcwd() + '/core/static/core/text_files/registration'

        try:

            # leer archivo modelo.py de core/text_files
            fo = open(cd + '/models.py', "r+")
            stri = fo.read()

            cd = proyecto.directorio + '/' + proyecto.nombre + '/' + 'registration' 

            try:
                os.remove( cd + "/models.py")
            except:
                print('no hay archivo')

            fd = os.open(cd + '/models.py',os.O_CREAT)
            with os.fdopen(os.open(cd + '/models.py',os.O_CREAT | os.O_RDWR ),'w') as fd:  
                fd.write(stri)
            fd.close()    

        except:
            print('No existe la aplicacion registration')

    # urls.py seguridad

    if proyecto.conseguridad:
        strlfp = 'from registration.urls import registration_patterns' + '\n'
        strlpp = '\tpath(' + "'" + 'accounts/' + "'" + ', include(' + "'" + 'django.contrib.auth.urls' + "'" + ')),' + '\n'
        strlpp += '\tpath(' + "'" + 'accounts/' + "'" + ', include(registration_patterns)),' + '\n'

    # leer archivo urls.py del proyecto
    cd = proyecto.directorio + '/' + proyecto.nombre + '/' + proyecto.nombre

    fo = open(cd + '/urls.py', "r+")
    stri = fo.read()

    stri = stri.replace('#@patternsseguridad', strlfp)
    stri = stri.replace('#@pathseguridad', strlpp)

    try:
        os.remove( cd + "/urls.py")
    except:
        print('no hay archivo')

    fd = os.open(cd + '/urls.py',os.O_CREAT)
    with os.fdopen(os.open(cd + '/urls.py',os.O_CREAT | os.O_RDWR ),'w') as fd:  
        fd.write(stri)
    fd.close() 

    if proyecto.conseguridad:
        cd = os.getcwd() + '/core/static/core/text_files/registration'

        try:

            # leer archivo modelo.py de core/text_files
            fo = open(cd + '/urls.py', "r+")
            stri = fo.read()

            cd = proyecto.directorio + '/' + proyecto.nombre + '/' + 'registration' 

            try:
                os.remove( cd + "/urls.py")
            except:
                print('no hay archivo')

            fd = os.open(cd + '/urls.py',os.O_CREAT)
            with os.fdopen(os.open(cd + '/urls.py',os.O_CREAT | os.O_RDWR ),'w') as fd:  
                fd.write(stri)
            fd.close()    

        except:
            print('No existe la aplicacion registration')

    # seguridad templates
    if proyecto.conseguridad:


        CreaSeguridadHtml(proyecto,'login.html')
        CreaSeguridadHtml(proyecto,'password_change_done.html')
        CreaSeguridadHtml(proyecto,'password_change_form.html')
        CreaSeguridadHtml(proyecto,'password_reset_complete.html')
        CreaSeguridadHtml(proyecto,'password_reset_confirm.html')
        CreaSeguridadHtml(proyecto,'password_reset_done.html')
        CreaSeguridadHtml(proyecto,'password_reset_form.html')
        CreaSeguridadHtml(proyecto,'profile_form.html')
        CreaSeguridadHtml(proyecto,'registro.html')

        strs = '\t\t\t\t\t\t<ul class="navbar-nav">' + '\n'
        strs += '\t\t\t\t\t\t\t{% if not request.user.is_authenticated %}  ' + '\n'
        strs += '\t\t\t\t\t\t\t\t<li class="nav-item">' + '\n'
        
        if proyecto.mayusculas:
            strs += '\t\t\t\t\t\t\t\t\t<a class="nav-link text-@coloropcionmenu font_opcion_menu_core" href="{% url ' + "'" + 'login' + "'" + '%}">LOGIN</a>' + '\n'
        else:
            strs += '\t\t\t\t\t\t\t\t\t<a class="nav-link text-@coloropcionmenu font_opcion_menu_core" href="{% url ' + "'" + 'login' + "'" + '%}">login</a>' + '\n'
        
        strs += '\t\t\t\t\t\t\t\t</li>' + '\n'
        strs += '\t\t\t\t\t\t\t\t<li class="nav-item">' + '\n'
        
        if proyecto.mayusculas:
            strs += '\t\t\t\t\t\t\t\t\t<a class="nav-link text-@coloropcionmenu font_opcion_menu_core" href="{% url ' + "'" + 'registration:registro' + "'" + '%}">REGISTRO</a>' + '\n'
        else:
            strs += '\t\t\t\t\t\t\t\t\t<a class="nav-link text-@coloropcionmenu font_opcion_menu_core" href="{% url ' + "'" + 'registration:registro' + "'" + '%}">Registro</a>' + '\n'
        
        strs += '\t\t\t\t\t\t\t\t</li>' + '\n'
        strs += '\t\t\t\t\t\t\t{% else %}' + '\n'
        strs += '\t\t\t\t\t\t\t\t<li class="nav-item">' + '\n'
        
        if proyecto.mayusculas:
            strs += '\t\t\t\t\t\t\t\t\t<a class="nav-link text-@coloropcionmenu font_opcion_menu_core" href="{% url ' + "'" + 'registration:profile' + "'" + '%}">PERFIL</a>' + '\n'
        else:
            strs += '\t\t\t\t\t\t\t\t\t<a class="nav-link text-@coloropcionmenu font_opcion_menu_core" href="{% url ' + "'" + 'registration:profile' + "'" + '%}">perfil</a>' + '\n'
        
        strs += '\t\t\t\t\t\t\t\t</li>' + '\n'
        strs += '\t\t\t\t\t\t\t\t<li class="nav-item">' + '\n'

        if proyecto.mayusculas:
            strs += '\t\t\t\t\t\t\t\t\t<a class="nav-link text-@coloropcionmenu font_opcion_menu_core" href="{% url ' + "'" + 'logout' + "'" + '%}">SALIR</a>' + '\n'
        else:
            strs += '\t\t\t\t\t\t\t\t\t<a class="nav-link text-@coloropcionmenu font_opcion_menu_core" href="{% url ' + "'" + 'logout' + "'" + '%}">salir</a>' + '\n'
        
        strs += '\t\t\t\t\t\t\t\t</li>' + '\n'
        strs += '\t\t\t\t\t\t\t{% endif %}' + '\n'
        strs += '\t\t\t\t\t\t</ul>' + '\n'

        strs = strs.replace('@coloropcionmenu', proyecto.colormenu)

        for aplicacion in Aplicacion.objects.filter(proyecto=proyecto):
            cd = proyecto.directorio + '/' + proyecto.nombre + '/core/templates/core/includes' 

            try:

                # leer archivo modelo.py de core/text_files
                fo = open(cd + '/menu_' + aplicacion.nombre + '.html', "r+")
                stri = fo.read()

                try:
                    os.remove( cd + '/menu_' + aplicacion.nombre + '.html')
                except:
                    print('no hay archivo')

                stri = stri.replace('<!-- seguridad -->', strs)

                fd = os.open(cd + '/menu_' + aplicacion.nombre + '.html',os.O_CREAT)
                with os.fdopen(os.open(cd + '/menu_' + aplicacion.nombre + '.html',os.O_CREAT | os.O_RDWR ),'w') as fd:  
                    fd.write(stri)
                fd.close()    

            except:
                print('No existe la aplicacion registration')


