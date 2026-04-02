from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View

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
                    usuario=self.request.user,  
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
    def post(self,*args,**kwargs):
        return self.renderizar

class Update(BasePerfil):
    pass

class Login(View):
    pass

class Logout(View):
    pass