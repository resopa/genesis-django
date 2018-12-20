from django.urls import path
from .views import CrearView,CrearProyectoView,CrearDirectoriosView, CrearModelosView, CrearVistasView, CrearFormsView, CrearUrlsView, CrearTemplatesView
from .views import CrearAplicacionesView, CrearSeguridadView

crear_patterns = ([
    path('', CrearView.as_view(), name='home'),
    path('proyecto/', CrearProyectoView.as_view(), name='proyecto'),
    path('aplicaciones/', CrearAplicacionesView.as_view(), name='aplicaciones'),
    path('directorios/', CrearDirectoriosView.as_view(), name='directorios'),
    path('modelos/', CrearModelosView.as_view(), name='modelos'),
    path('vistas/', CrearVistasView.as_view(), name='vistas'),
    path('forms/', CrearFormsView.as_view(), name='forms'),
    path('urls/', CrearUrlsView.as_view(), name='urls'),
    path('templates/', CrearTemplatesView.as_view(), name='templates'),
    path('seguridad/', CrearSeguridadView.as_view(), name='seguridad'),
], 'crear')