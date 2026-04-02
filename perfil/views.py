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

        if self.request.user.is_authenticated: # User antigo (uptade)
            self.contexto = {
                'userform': forms.UserForm(
                    data=data,
                    user=self.request.user,  
                    instance=self.request.user   
                ),
                'perfilform': forms.PerfilForm(data=data)
            }
        else:
            self.contexto = {
                'userform': forms.UserForm(data=data), # User novo (cadastro)
                'perfilform': forms.PerfilForm(data=data)
            }

        self.renderizar = render(
            self.request, self.template_name, self.contexto
        )

    def get(self, *args, **kwargs):
        return self.renderizar
class Criar(BasePerfil):
    
    def get(self, *args, **kwargs): # caso ja tenha conta, não consegue acessar cadastro
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
            
            print('Perfil salvo teste')
            
            messages.success(self.request, "Usuário Cadastrado com sucesso.")
            return redirect('/')
            
        else:
            print('Perfil não salvo teste - Erro de Validação')
            
            messages.error(self.request, "Não foi possível efetuar o cadastro.")
        
        return self.renderizar

class Update(BasePerfil):
    pass

class Login(View):
    pass

class Logout(View):
    pass