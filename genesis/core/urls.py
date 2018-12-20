from django.urls import path
from .views import CorePageView,DespliegaGenesisView,TutorialEncabezadoListaView, EditarTutorialEncabezadoView
from .views import BorrarTutorialEncabezadoView, CrearTutorialEncabezadoView
from .views import BorrarTutorialDetalleView, CrearTutorialDetalleView,EditarTutorialDetalleView,DespliegaTutorialView, DesplegarPreciosView, CompraExitosaView

core_patterns = ([
    path('', CorePageView.as_view(), name='home'),
    path('despliega', DespliegaGenesisView.as_view(), name='despliega'),
    path('desplegar_tutorial', DespliegaTutorialView.as_view(), name='desplegar_tutorial'),
    path('desplegar_precios', DesplegarPreciosView.as_view(), name='desplegar_precios'),
    path('tutorial', TutorialEncabezadoListaView.as_view(), name='tutorial'),
    path('editar_tutorial_encabezado/<int:pk>/', EditarTutorialEncabezadoView.as_view(), name='editar_tutorial_encabezado'),
    path('borrar_tutorial_encabezado/<int:pk>/',BorrarTutorialEncabezadoView.as_view(), name='borrar_tutorial_encabezado'),
    path('crear_tutorial_encabezado/',CrearTutorialEncabezadoView.as_view(), name='crear_tutorial_encabezado'),
    path('crear_turorial_detalle/',CrearTutorialDetalleView.as_view(), name='crear_tutorial_detalle'),
    path('editar_tutorila_detalle/<int:pk>/',EditarTutorialDetalleView.as_view(), name='editar_tutorial_detalle'),
    path('borrar_editar-detalle/<int:pk>/',BorrarTutorialDetalleView.as_view(), name='borrar_tutorial_detalle'),    
   	path('compraexitosa/',CompraExitosaView.as_view(), name='compraexitosa'),
], 'core')