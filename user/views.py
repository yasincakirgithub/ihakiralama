from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from user.forms import LoginForm,RegisterForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
from django.utils.translation import gettext_lazy as _

# Create your views here.
def loginPage(request):
    if request.user.pk:
        return HttpResponseRedirect(reverse('dashboardPage'))
    if request.POST:
        form = LoginForm(data=request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('dashboardPage'))
            else:
                return render(request, 'user/login.html',
                              context={'form': form, "error": _("Wrong username or password!")})
        else:
            return render(request, 'user/login.html',
                          context={'form': form, "error": _("Wrong username or password!")})

    return render(request, 'user/login.html')


def logoutPage(request):
    logout(request)
    return redirect('loginPage')


def registerPage(request):
    form = RegisterForm(data=request.POST or None)
    if request.POST:
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse('dashboardPage'))
    return render(request,'user/register.html',context={"form":form})
