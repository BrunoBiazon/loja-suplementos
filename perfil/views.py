from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, update_session_auth_hash
 
from . import models
from . import forms


class BasePerfil(View):
    template_name = 'perfil/criar.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        data = request.POST or None

        if request.user.is_authenticated:
            perfil, _ = models.PerfilUsuario.objects.get_or_create(user=request.user)

            self.contexto = {
                'userform': forms.UserForm(
                    data=data,
                    user=request.user,
                    instance=request.user
                ),
                'perfilform': forms.PerfilForm(
                    data=data,
                    instance=perfil
                )
            }
        else:
            self.contexto = {
                'userform': forms.UserForm(data=data),
                'perfilform': forms.PerfilForm(data=data)
            }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.contexto)


class Criar(BasePerfil):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        userform = self.contexto['userform']
        perfilform = self.contexto['perfilform']

        if userform.is_valid() and perfilform.is_valid():
            usuario = userform.save(commit=False)

            senha = userform.cleaned_data.get('password')
            usuario.set_password(senha)

            usuario.save()

            perfil = perfilform.save(commit=False)
            perfil.user = usuario
            perfil.save()

            messages.success(request, "Usuário cadastrado com sucesso.")
            return redirect('/')

        messages.error(request, "Não foi possível efetuar o cadastro.")
        return render(request, self.template_name, self.contexto)


class Update(BasePerfil):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('perfil:login')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('perfil:login')

        userform = self.contexto['userform']
        perfilform = self.contexto['perfilform']

        if userform.is_valid() and perfilform.is_valid():
            usuario = userform.save(commit=False)

            senha = userform.cleaned_data.get('password')

            if senha:
                usuario.set_password(senha)

            usuario.save()

            if senha:
                update_session_auth_hash(request, usuario)

            perfil = perfilform.save(commit=False)
            perfil.user = usuario
            perfil.save()

            messages.success(request, "Dados atualizados com sucesso.")
            return redirect('/')

        messages.error(request, "Erro ao atualizar dados.")
        return render(request, self.template_name, self.contexto)


class Login(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        form = AuthenticationForm()
        return render(request, 'perfil/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')

        messages.error(request, 'Usuário ou senha inválidos.')
        return render(request, 'perfil/login.html', {'form': form})


class Logout(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'Você saiu da sua conta com sucesso.')
        return redirect('/')