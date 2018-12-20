from django.urls import path
from .views import CrearAplicacionView, EditarAplicacionView, BorrarAplicacionView

aplicaciones_patterns = ([
    path('crear/',CrearAplicacionView.as_view(), name='crear'),
    path('editar/<int:pk>/',EditarAplicacionView.as_view(), name='editar'),
    path('borrar/<int:pk>/',BorrarAplicacionView.as_view(), name='borrar'),
], 'aplicaciones')