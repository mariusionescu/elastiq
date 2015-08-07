
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.views.generic import View
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, widget=forms.TextInput({'placeholder': "Username"}))
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput({'placeholder': "Password"}))

class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('/console/')
            else:
                message = 'Authentication failed'
                return render(request, 'login.html', {'form': form, 'message': message})
        else:
            message = 'Authentication failed'
            return render(request, 'login.html', {'form': form, 'message': message})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('/console/login/')


class ConsoleView(View):

    def get(self, request):
        return render(request, 'console.html')
