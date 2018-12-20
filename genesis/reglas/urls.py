from django.urls import path
from .views import CrearReglaView, EditarReglaView, BorrarReglaView

reglas_patterns = ([
    path('crear/',CrearReglaView.as_view(), name='crear'),
    path('editar/<int:pk>/',EditarReglaView.as_view(), name='editar'),
    path('borrar/<int:pk>/',BorrarReglaView.as_view(), name='borrar'),
], 'reglas')