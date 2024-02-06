from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

from django.urls import reverse_lazy


class UserRegistration(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('blog:index')
