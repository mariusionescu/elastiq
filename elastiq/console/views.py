
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.views.generic import View
from django.http import Http404
from console.models import Node
from django import forms
from random import choice

from django.utils.text import slugify

import string
chars = string.letters + string.digits


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


class NodeAddForm(forms.Form):

    name = forms.CharField(label='Username', max_length=100, widget=forms.TextInput({
        'placeholder': "The name will be slugged"
    }))
    memory = forms.IntegerField(
        label='Memory',
        min_value=1,
        max_value=30,
        initial=1,
        widget=forms.TextInput({'placeholder': "Memory allocated"})
    )
    cpu = forms.IntegerField(
        label='CPU',
        min_value=1,
        max_value=12,
        initial=1,
        widget=forms.TextInput({'placeholder': "CPUs allocated"})
    )

    def clean_name(self):
        name = slugify(self.cleaned_data['name'].replace('.', '-'))

        if Node.objects.filter(name=name).exists():
            raise forms.ValidationError("A node with this name already exists.")
        return name

class NodeEditForm(forms.Form):

    memory = forms.IntegerField(
        label='Memory',
        min_value=1,
        max_value=30,
        initial=1,
        widget=forms.TextInput({'placeholder': "Memory allocated"})
    )
    cpu = forms.IntegerField(
        label='CPU',
        min_value=1,
        max_value=12,
        initial=1,
        widget=forms.TextInput({'placeholder': "CPUs allocated"})
    )


class ConsoleView(View):

    def get(self, request):
        nodes = Node.objects.all()
        return render(request, 'console.html', {'nodes': nodes})


class NodeAddView(View):

    def get(self, request):
        form = NodeAddForm()
        return render(request, 'node_add.html', {'form': form, 'error': False})

    def post(self, request):

        form = NodeAddForm(request.POST)

        if form.is_valid():
            name = slugify(form.cleaned_data['name'].replace('.', '-'))
            memory = form.cleaned_data['memory']
            cpu = form.cleaned_data['cpu']

            node = Node(
                name=name,
                memory=memory,
                cpu=cpu,
                status='pending',
                username=''.join(choice(chars) for _ in range(8)).lower(),
                password=''.join(choice(chars) for _ in range(16))
            )
            messages.add_message(request, messages.INFO, 'The node has been added')
            node.save()
            return redirect('/console/')
        else:
            return render(request, 'node_add.html', {'form': form, 'error': True})


class NodeEditView(View):

    def get(self, request, node_id):

        try:
            node = Node.objects.get(pk=node_id)
        except Node.DoesNotExists:
            raise Http404
        form = NodeEditForm(initial={
            'memory': node.memory,
            'cpu': node.cpu
        })

        return render(request, 'node_edit.html', {'form': form, 'error': False, 'node': node})

    def post(self, request, node_id=None):

        form = NodeEditForm(request.POST)

        try:
            node = Node.objects.get(pk=node_id)
        except Node.DoesNotExists:
            raise Http404

        if form.is_valid():
            memory = form.cleaned_data['memory']
            cpu = form.cleaned_data['cpu']

            node.memory = memory
            node.cpu = cpu
            node.status = 'pending'
            messages.add_message(request, messages.INFO, 'The node has been saved')
            node.save()
            return redirect('/console/')
        else:
            return render(request, 'node_edit.html', {'form': form, 'error': True, 'node': node})


class NodeDeleteView(View):

    def get(self, request, node_id):

        try:
            node = Node.objects.get(pk=node_id)
        except Node.DoesNotExists:
            raise Http404
        node.delete()

        messages.add_message(request, messages.INFO, 'The node has been deleted')
        return redirect('/console/')

