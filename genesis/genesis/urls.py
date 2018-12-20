"""webplayground URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from core.urls import core_patterns
from proyectos.urls import proyectos_patterns
from aplicaciones.urls import aplicaciones_patterns
from modelos.urls import modelos_patterns
from propiedades.urls import propiedades_patterns
from reglas.urls import reglas_patterns
from registration.urls import registration_patterns
from crear.urls import crear_patterns
from profiles.urls import profiles_patterns

urlpatterns = [
    path('',include(core_patterns)),
    path('proyectos/',include(proyectos_patterns)),
    path('aplicaciones/',include(aplicaciones_patterns)),
    path('modelos/',include(modelos_patterns)),
    path('propiedades/',include(propiedades_patterns)),
    path('reglas/',include(reglas_patterns)),
    path('crear/',include(crear_patterns)),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include(registration_patterns)),
    path('profiles/', include(profiles_patterns)),
]

if settings.DEBUG == True:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)