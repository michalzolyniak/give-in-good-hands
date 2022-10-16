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
import datetime

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
                   'count_organization': count_organization}
        return render(request, "pass_things/index.html",
                      context)


class AddDonation(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        context = {'categories': categories,
                   'institutions': institutions}
        return render(request, "pass_things/form.html", context)

    def post(self, request, *args, **kwargs):
        data = dict(request.POST)
        quantity = int(data['bags'][0])
        institution = data['organization'][0]
        institution = Institution.objects.get(pk=int(institution))
        address = data['address'][0]
        phone_number = data['phone'][0]
        city = data['city'][0]
        zip_code = data['postcode'][0]
        pick_up_date = data['data'][0]
        pick_up_time = data['time'][0]
        pick_up_comment = data['more_info'][0]
        user = request.user
        categories_to_add = data['categories']
        donation = Donation.objects.create(
            quantity=quantity,
            institution=institution,
            address=address,
            phone_number=phone_number,
            city=city,
            zip_code=zip_code,
            pick_up_date=pick_up_date,
            pick_up_time=pick_up_time,
            pick_up_comment=pick_up_comment,
            user=user
        )

        for category in categories_to_add:
            donation.categories.add(category)

        return JsonResponse({'response': 'ok'})


class ConfirmationView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "pass_things/form-confirmation.html")
