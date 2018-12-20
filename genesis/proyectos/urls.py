from django.urls import path
from .views import ListarProyectoView,  EditarProyectoView, CrearProyectoView, BorrarProyectoView, dumpView,ListaArbolView
# from .views import CrearDirectoriosView,ListarArchivosView,LeerArchivosView,EscribirArchivosView
from . import views

proyectos_patterns = ([
    path('', ListarProyectoView.as_view(), name='home'),
    path('editar/<int:pk>/',EditarProyectoView.as_view(), name='editar'),
    path('crear/',CrearProyectoView.as_view(), name='crear'),
    path('borrar/<int:pk>/',BorrarProyectoView.as_view(), name='borrar'),
    path('descarga/',dumpView.as_view(), name='descarga'),
    path('listaarbol/<int:pk>/',ListaArbolView.as_view(), name='listaarbol'),
    # path('creardirectorios/',CrearDirectoriosView, name='creardirectorios'),
    # path('listararchivos/',ListarArchivosView, name='listararchivos'),
    # path('leerarchivos/',LeerArchivosView, name='leerarchivos'),
    # path('escribirarchivos/',EscribirArchivosView, name='escribirarchivos'),
], 'proyectos')