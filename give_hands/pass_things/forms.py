
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()


class RegisterForm(forms.Form):
    name = forms.CharField(max_length=150)
    surname = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)


class LoginForm(forms.Form):
    email = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)






# class RegisterForm(UserCreationForm):
#     class Meta:
#         model = get_user_model()
#         # fields = ('email', 'username', 'password1', 'password2')
#         fields = ('first_name', 'last_name', 'email', 'password1', 'password2')
#         fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
#
#         # fields = ('email', 'password1', 'password2')


# class LoginForm(AuthenticationForm):
#     username = forms.CharField(label='Email / Username')

#





