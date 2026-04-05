from django.shortcuts import render,redirect
from django.views.generic.list import ListView
from django.views import View

class Pagar(View):
    template_name = 'pedido/pagar.html'
    
    def get(self,request, *arg, **kwargs):
        
        contexto = {
            
        }
        return render(request, self.template_name , contexto)

class Salvar(View):
    pass

class Detalhe(View):
    pass