# from django.contrib.auth.forms import UserCreationForm
from .forms import UserCreationFormWithEmail, ProfileForm, EmailForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django import forms
from .models import Profile

# Create your views here.
class RegistroView(CreateView):
	form_class = UserCreationFormWithEmail
	#success_url = reverse_lazy('login')
	template_name = 'registration/registro.html'

	def get_success_url(self):
		return reverse_lazy('login') + '?register'

	def get_form(self, form_class=None):
		form = super(RegistroView, self).get_form()
		#Modificar en tiempo real
		form.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder':'Nombre de Usuario', 'autocomplete': 'off'}) 
		form.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control mb-2', 'placeholder':'Direccion email', 'autocomplete': 'off'}) 
		form.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-2', 'placeholder':'Contrasena'}) 
		form.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-2', 'placeholder':'Repite la contrasena'}) 
		return form

# @method_decorator(login_required,name='dispatch')
class ProfileUpdate(UpdateView):
	form_class = ProfileForm
	success_url = reverse_lazy('registration:profile')	
	template_name = 'registration/profile_form.html'

	def get_object(self):
		#recuperar el objeto que se va a aeditar
		profile , created = Profile.objects.get_or_create(user=self.request.user)
		return profile


# @method_decorator(login_required,name='dispatch')
class EmailUpdate(UpdateView):
	form_class = EmailForm
	success_url = reverse_lazy('registration:profile')	
	template_name = 'registration/profile_email_form.html'

	def get_object(self):
		#recuperar el usuario
		return self.request.user

	def get_form(self,form_class=None):
		form = super(EmailUpdate, self).get_form()
		#Modificar en tiempo real
		form.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control mb-2', 'placeholder':'Email'}) 
		return form