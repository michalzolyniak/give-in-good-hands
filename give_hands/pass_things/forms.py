from django import forms
from .models import SCHOOL_CLASS, Student, CONVERSION, SchoolSubject, \
    GRADES, Toppings, COLORS
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()


class SearchStudentForm(forms.Form):
    text = forms.CharField()


class AddStudentForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    school_class = forms.ChoiceField(choices=SCHOOL_CLASS)
    year_of_birth = forms.IntegerField()


class ConvertCurrency(forms.Form):
    currency_value = forms.FloatField()
    usd_course = forms.FloatField()
    conversion = forms.ChoiceField(choices=CONVERSION)


class AddStudentModelForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'school_class', 'year_of_birth']


class StudentPresentForm(forms.Form):
    student = forms.ModelChoiceField(queryset=Student.objects.all())
    # day = forms.DateField(widget=forms.HiddenInput)
    day = forms.DateField()
    present = forms.BooleanField()


class CheckSexForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        last_letter = first_name[-1]
        if last_letter.lower() != 'a':
            raise ValidationError('Nie jesteś kobietą!')
        return first_name


class StudentGradeForm(forms.Form):
    student = forms.ModelChoiceField(queryset=Student.objects.all())
    # school_subject = forms.ModelChoiceField(queryset=SchoolSubject.objects.all().values_list('name', flat=True))
    school_subject = forms.ModelChoiceField(queryset=SchoolSubject.objects.all())
    grade = forms.ChoiceField(choices=GRADES)


class AddToppings(forms.Form):
    toppings = forms.ModelChoiceField(queryset=Toppings.objects.all(), widget=forms.CheckboxSelectMultiple)


class BackgroundColorForm(forms.Form):
    color = forms.ChoiceField(choices=COLORS, widget=forms.RadioSelect)


class LoginForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_login(self):
        login = self.cleaned_data['login']
        error_text = "A sio, hackerze!"
        if login != 'root':
            raise ValidationError(error_text)
        return login

    def clean_password(self):
        password = self.cleaned_data['password']
        error_text = "A sio, hackerze!"
        if password != 'very_secret':
            raise ValidationError(error_text)
        return password


class MailUrlForm(forms.Form):
    name = forms.CharField()
    surname = forms.CharField()
    mail = forms.EmailField()
    url = forms.URLField()

    # def clean_mail(self):
    #     first_name = self.cleaned_data['mail']
    #     last_letter = first_name[-1]
    #     if last_letter.lower() != 'a':
    #         raise ValidationError('Nie jesteś kobietą!')
    #     return first_name


class UserCreateForm(forms.Form):
    login = forms.CharField(max_length=150)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    name = forms.CharField(max_length=150)
    surname = forms.CharField(max_length=150)

    def clean(self):
        cd = super().clean()
        password1 = cd.get('password1')
        password2 = cd.get('password2')
        if password1 != password2:
            raise ValidationError('Hasła nie są identyczne.')

    def clean_login(self):
        login = self.cleaned_data['login']
        if User.objects.filter(username=login).exists():
            raise ValidationError('Login jest niepoprawy')
        return login


class LoginForm(forms.Form):
    login = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cd = super().clean()
        login = cd.get('login')
        password = cd.get('password')
        user = authenticate(username=login, password=password)
        if user is None:
            raise ValidationError('Dane logowania nie są prawidłowe')


# class PasswordChangeForm(forms.Form):
#     password1 = forms.CharField(widget=forms.PasswordInput)
#     password2 = forms.CharField(widget=forms.PasswordInput)
#
#
#     def clean(self):
#         cd = super().clean()
#         password1 = cd.get('password1')
#         password2 = cd.get('password2')
#         if password1 != password2:
#             raise ValidationError('Hasła nie są identyczne.')


class PasswordChangeForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:

        model = User
        fields = ['password']

    def clean(self):
        cd = super().clean()
        password1 = cd.get('password')
        password2 = cd.get('password2')
        if password1 != password2:
            raise ValidationError('Hasła nie są identyczne.')
