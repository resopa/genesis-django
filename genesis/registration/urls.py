from django.urls import path
from .views import RegistroView, ProfileUpdate,EmailUpdate

registration_patterns = ([
	path('registro/',RegistroView.as_view(), name='registro'),
	path('profile/',ProfileUpdate.as_view(), name='profile'),
	path('profile/email/',EmailUpdate.as_view(), name='profile_email'),
], 'registration')