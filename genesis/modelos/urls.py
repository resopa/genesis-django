from django.urls import path
from .views import CrearModeloView, EditarModeloView, BorrarModeloView

modelos_patterns = ([
    path('crear/',CrearModeloView.as_view(), name='crear'),
    path('editar/<int:pk>/',EditarModeloView.as_view(), name='editar'),
    path('borrar/<int:pk>/',BorrarModeloView.as_view(), name='borrar'),
], 'modelos')