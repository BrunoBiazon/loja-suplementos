from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from . import models
from pprint import pprint # teste carrinho

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
            'HTTP_REFERER', reverse('produto:lista')                                
        )
        id_prod = request.GET.get('vid')
        
        if not id_prod:
            messages.error(
                request, 'Produto não existe'
            )
            return redirect(http_referer) 
            
        variacao = get_object_or_404(models.Variacao, id=id_prod)
        variacao_estoque = variacao.estoque
        produto = variacao.produto
        
        produto_id = produto.id
        produto_nome = produto.nome
        variacao_nome = variacao.nome
        variacao_id = str(variacao.id) 
        preco_unitario = variacao.preco
        preco_unitario_promocional = variacao.preco_promocional
        quantidade = 1
        slug = produto.slug
        imagem = produto.imagem
            
        if imagem:
            imagem = imagem.name
        else:
            imagem = ""

        if variacao.estoque < 1:
            messages.error(
                self.request, 'Não há mais produtos em estoque'
            )
            return redirect(http_referer) 
            
        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()
            
        carrinho = self.request.session['carrinho']
            
        if variacao_id in carrinho:
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            quantidade_carrinho += 1
            
            if variacao.estoque < quantidade_carrinho:
                messages.warning(
                    self.request,
                    f'Não há estoque suficiente para {quantidade_carrinho}x do produto {produto_nome}.' 
                    f'Mantivemos o limite máximo de {variacao.estoque}x no seu carrinho.'
                )
                quantidade_carrinho = variacao.estoque
                
            carrinho[variacao_id]['quantidade'] = quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo'] = preco_unitario * quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo_promocional'] = preco_unitario_promocional * quantidade_carrinho
        else:   
            carrinho[variacao_id] = {
                'produto_id' : produto_id,
                'produto_nome': produto_nome,
                'variacao_nome': variacao_nome,
                'variacao_id': variacao_id,
                'preco_unitario': preco_unitario,
                'preco_unitario_promocional': preco_unitario_promocional,
                'preco_quantitativo': preco_unitario, 
                'preco_quantitativo_promocional': preco_unitario_promocional, 
                'quantidade': 1,  
                'slug': slug,
                'imagem': imagem,
                }
            
        self.request.session.save() 
        
        messages.success(
            request,
            f"Produto: {produto_nome} adicionado com sucesso!"
        )
        
        return redirect(http_referer)

class RemoverDoCarrinho(View):
     def get(self, request, *args, **kwargs): 
        pass

class Carrinho(View):
    def get(self, *args, **kwargs): 
        return render(self.request, 'produto/carrinho.html')
class Finalizar(View):
    pass