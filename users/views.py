from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

class RegisterUser(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    def form_valid(self, form):
        messages.success(self.request, "User created successfully!")
        return super().form_valid(form)

def LogoutView(request):
    logout(request)
    return redirect('login')