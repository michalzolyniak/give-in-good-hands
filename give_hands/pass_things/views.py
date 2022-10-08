from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import get_user_model, login, \
    authenticate, logout
from .forms import LoginForm, RegisterForm
from django.urls import reverse_lazy
from django.views.generic import RedirectView
from django.views.generic import FormView

User = get_user_model()


# Create your views here.


class RegisterView(View):
    form_class = RegisterForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {'form': form}
        return render(request, 'pass_things/register.html', context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = {'form': form}
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(
                first_name=cd['name'],
                last_name=cd['surname'],
                email=cd['email'],
                password=cd['password'],
            )

            return redirect('login')
        return render(request, 'pass_things/register.html', context)


class LoginView(FormView):
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {'form': form}
        return render(request, 'pass_things/login.html', context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = {'form': form}
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(email=cd['email'], password=cd['password'])
            login(self.request, user)
            return redirect('landing-page')
        return render(request, 'pass_things/login.html', context)


class LandingPage(View):
    def get(self, request):
        return render(request, "pass_things/index.html")


class AddDonation(View):
    def get(self, request):
        return render(request, "pass_things/form.html")


class LogoutView(RedirectView):
    """
        Logout view
    """
    url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class LogoutView(RedirectView):
    """
        Logout view
    """
    url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)
