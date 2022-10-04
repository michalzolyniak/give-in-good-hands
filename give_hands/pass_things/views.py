from django.shortcuts import render
from django.views import View


# Create your views here.

class LandingPage(View):
    def get(self, request):
        return render(request, "pass_things/index.html")


class AddDonation(View):
    def get(self, request):
        return render(request, "pass_things/form.html")


class Login(View):
    def get(self, request):
        return render(request, "pass_things/login.html")


class Register(View):
    def get(self, request):
        return render(request, "pass_things/register.html")
