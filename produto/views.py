from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from . import models

class ListaProdutos(ListView):
    model = models. Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = 10
class Detalheproduto(DetailView):
    model = models. Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'

class AdicionarAoCarrinho(View):
    def get(self, request, *args, **kwargs): 
        http_referer = request.META.get(
            'HTTP_REFERER',
             reverse('produto:lista')                                
        )
        id_prod = request.GET.get('vid')
        
        if not id_prod:
            messages.error(
                request, 'Produto não existe'
            )
            return redirect(http_referer) 
            
            variacao = get_object_or_404(models.Variacao, id= variacao_id)
            
            if not self.request.seesion.get('carrinho'):
                self.request.session['carrinho'] = {}
                self.request.session.save()
                
            carrinho = self.request.session['carrinho']
            
            if variacao_id in carrinho:
                TODO
                pass
            else:   
                TODO
            
        return redirect(http_referer)

class RemoverDoCarrinho(View):
    pass

class Carrinho(View):
    pass
class Finalizar(View):
    pass