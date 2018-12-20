from django.urls import path
from .views import CrearPropiedadView, EditarPropiedadView, BorrarPropiedadView

propiedades_patterns = ([
    path('crear/',CrearPropiedadView.as_view(), name='crear'),
    path('editar/<int:pk>/',EditarPropiedadView.as_view(), name='editar'),
    path('borrar/<int:pk>/',BorrarPropiedadView.as_view(), name='borrar'),
], 'propiedades')