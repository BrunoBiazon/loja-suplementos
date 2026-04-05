from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views import View

from django.contrib import messages
from django.shortcuts import render
from django.views import View

from . import models
from . import forms

class BasePerfil(View):
    template_name = 'perfil/criar.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        data = self.request.POST or None

        if self.request.user.is_authenticated:
            self.contexto = {
                'userform': forms.UserForm(
                    data=data,
                    user=self.request.user,
                    instance=self.request.user
                ),
                'perfilform': forms.PerfilForm(
                    data=data,
                    instance=self.request.user
                )
            }
        else:
            self.contexto = {
                'userform': forms.UserForm(data=data),
                'perfilform': forms.PerfilForm(data=data)
            }

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, self.contexto)


class Criar(BasePerfil):

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('/')
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        userform = self.contexto['userform']
        perfilform = self.contexto['perfilform']

        if userform.is_valid() and perfilform.is_valid():
            usuario = userform.save(commit=False)

            usuario.is_staff = False
            usuario.is_superuser = False

            senha = userform.cleaned_data.get('password')
            usuario.set_password(senha)

            usuario.save()

            perfil = perfilform.save(commit=False)
            perfil.user = usuario
            perfil.save()

            messages.success(self.request, "Usuário Cadastrado com sucesso.")
            return redirect('/')

        messages.error(self.request, "Não foi possível efetuar o cadastro.")
        return render(self.request, self.template_name, self.contexto)


class Update(BasePerfil):

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:login')
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:login')

        userform = self.contexto['userform']
        perfilform = self.contexto['perfilform']

        if userform.is_valid() and perfilform.is_valid():
            usuario = userform.save(commit=False)

            senha = userform.cleaned_data.get('password')
            if senha:
                usuario.set_password(senha)

            usuario.save()

            perfil = perfilform.save(commit=False)
            perfil.user = usuario
            perfil.save()

            messages.success(self.request, "Dados atualizados com sucesso.")
            return redirect('/')

        messages.error(self.request, "Erro ao atualizar dados.")
        return render(self.request, self.template_name, self.contexto)
class Login(View):
    pass

class Logout(View):
    pass