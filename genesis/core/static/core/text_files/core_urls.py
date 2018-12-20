
from django.urls import path, include
from core.views import CorePageView

core_patterns = ([
	path('',CorePageView.as_view(),name='home'),
],'core')

