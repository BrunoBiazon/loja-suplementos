from django.shortcuts import render,redirect
from django.views.generic.list import ListView
from django.views import View
from django.contrib import messages 

class Pagar(View):
    template_name = 'pedido/pagar.html'
    
    def get(self,request, *arg, **kwargs):
        
        if not request.request.user.is_authenticated:
            messages.error(
                request,
                'Faça o login para acessar pagamentos'
                
            )
            return redirect('perfil:login')
        
        if not request.request.session.get('carrinho'):
            messages.error(
                request,
                'Coloque produtos no carrinho para acessar pagametos'
                
            )
            return redirect('produto:lista')
        contexto = {
            
        }
        return render(request, self.template_name , contexto)

class Salvar(View):
    pass

class Detalhe(View):
    pass