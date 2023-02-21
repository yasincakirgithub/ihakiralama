from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(required=True, label=_("Username"),
                               widget=forms.TextInput(attrs={"class": "form-control", "placeholder": _('Username')}))
    password = forms.CharField(required=True, label=_("Password"),
                               widget=forms.PasswordInput(
                                   attrs={"class": "form-control", "placeholder": _('Password')}))

class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "first_name","last_name", "password1", "password2")

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        if commit:
            user.save()
        return user

