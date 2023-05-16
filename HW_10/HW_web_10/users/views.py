from django import dispatch
from django.shortcuts import render, redirect
from django.views import View
from .forms import RegisterForm
from django.contrib import messages


# Create your views here.
class RegisterView(View):
    form_class = RegisterForm
    template_name = 'users/signup.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(to="app_instagram:home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Вітаємо {username}')
            return redirect(to='users:login')
        return render(request, self.template_name, {'form': form})
