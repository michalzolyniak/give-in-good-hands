import json
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import get_user_model, login, \
    authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginForm, RegisterForm
from django.urls import reverse_lazy
from django.views.generic import RedirectView
from django.views.generic import FormView
from django.db.models import Sum, Count
from django.http import JsonResponse
from .models import Donation, Category, Institution

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
            if user:
                login(self.request, user)
                return redirect('landing-page')
            else:
                return redirect('register')
        return render(request, 'pass_things/login.html', context)


class LogoutView(RedirectView):
    """
        Logout view
    """
    url = reverse_lazy('landing-page')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class LandingPage(View):
    def get(self, request):
        count_bags = Donation.objects.aggregate(Sum('quantity'))
        count_bags = count_bags['quantity__sum']
        count_organization = Donation.objects.values('institution').distinct().count()
        context = {'count_bags': count_bags,
                   'count_organization':count_organization}
        return render(request, "pass_things/index.html",
                      context)

        context = {'form': form}
        # if form.is_valid():
        #     cd = form.cleaned_data
        #     breakpoint()
        #     print(cd['name'])
        #     # User.objects.create_user(
        #     #     first_name=cd['name'],
        #     #     last_name=cd['surname'],
        #     #     email=cd['email'],
        #     #     password=cd['password'],
        #     # )
        #
        #     return redirect('login')


# u = User.objects.get(pk=1)
#     i = Institution.objects.get(pk=1)
#     d = Donation(quantity=3, institution=i, address="Narutowicza", phone_number="509-214-447", city="Szczecinek",
#                  zip_code="78-400", pick_up_date=datetime.datetime.now(), pick_up_time=datetime.time(),
#                  pick_up_comment="test test", user=u)
#     d.save()



class AddDonation(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        context = {'categories': categories,
                   'institutions': institutions}
        return render(request, "pass_things/form.html", context)

    def post(self, request, *args, **kwargs):
        data = dict(request.POST)
        metarCode = data['name']
        breakpoint()
        return JsonResponse({'MetarCode': metarCode})

