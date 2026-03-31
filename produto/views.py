from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from . import models
from pprint import pprint # teste carrinho

class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = 12
class Detalheproduto(DetailView):
    model = models.Produto
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
            messages.error(request, 'Produto não existe')
            return redirect(http_referer) 
            
        variacao = get_object_or_404(models.Variacao, id=id_prod)
        produto = variacao.produto
        
        preco_unitario = variacao.preco
        preco_unitario_promocional = variacao.preco_promocional
        
        if not preco_unitario_promocional:
            preco_unitario_promocional = preco_unitario

        if produto.imagem:
            imagem = produto.imagem.url
        else:
            imagem = ""

        if variacao.estoque < 1:
            messages.error(self.request, 'Não há mais produtos em estoque')
            return redirect(http_referer) 
            
        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()
            
        carrinho = self.request.session['carrinho']
        variacao_id = str(variacao.id)
            
        if variacao_id in carrinho:
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            quantidade_carrinho += 1
            
            if variacao.estoque < quantidade_carrinho:
                messages.warning(
                    self.request,
                    f'Estoque insuficiente. Mantivemos {variacao.estoque}x no carrinho.'
                )
                quantidade_carrinho = variacao.estoque
                
            carrinho[variacao_id]['quantidade'] = quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo'] = preco_unitario * quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo_promocional'] = preco_unitario_promocional * quantidade_carrinho
        else:   
            carrinho[variacao_id] = {
                'produto_id' : produto.id,
                'produto_nome': produto.nome,
                'variacao_nome': variacao.nome,
                'variacao_id': variacao_id,
                'preco_unitario': preco_unitario,
                'preco_unitario_promocional': preco_unitario_promocional,
                'preco_quantitativo': preco_unitario, 
                'preco_quantitativo_promocional': preco_unitario_promocional, 
                'quantidade': 1,  
                'slug': produto.slug,
                'imagem': imagem,
            }
            
        self.request.session.save() 
        messages.success(request, f"Produto: {produto.nome} adicionado!")
        return redirect(http_referer)
class RemoverDoCarrinho(View):
     def get(self, request, *args, **kwargs): 
        pass

class Carrinho(ListView):
    def get(self, request, *args, **kwargs):
        return render(request, 'produto/carrinho.html')


class Promocao(ListView):
    model = models.Produto
    template_name = 'produto/promocao.html'
    context_object_name = 'produtos'
    paginate_by = 12
    
    def get_queryset(self):
        ProdPromocaoRelampago = super().get_queryset() 
        
        ProdPromocaoRelampago = ProdPromocaoRelampago.filter(promocao_relampago='S') 
        
        return ProdPromocaoRelampago
    
class Snacks(ListView):
    model = models.Produto
    template_name = 'produto/snacks.html'
    context_object_name = 'produtos'
    paginate_by = 12
    
    def get_queryset(self):
        ProdSnacks = super().get_queryset() 
        
        ProdSnacks =ProdSnacks.filter(categoria='Snacks').order_by('-id') 
        
        return ProdSnacks
    
    
class Whey(ListView):
    model = models.Produto
    template_name = 'produto/whey.html'
    context_object_name = 'produtos'
    paginate_by = 12
    
    def get_queryset(self):
        ProdWhey = super().get_queryset() 
        ProdWhey = ProdWhey.filter(categoria='Whey').order_by('-id') 
        return ProdWhey


class Saude(ListView):
    model = models.Produto
    template_name = 'produto/saude.html'
    context_object_name = 'produtos'
    paginate_by = 12
    
    def get_queryset(self):
        ProdSaude = super().get_queryset() 
        ProdSaude = ProdSaude.filter(categoria='Saude').order_by('-id') 
        return ProdSaude


class Creatina(ListView):
    model = models.Produto
    template_name = 'produto/creatina.html'
    context_object_name = 'produtos'
    paginate_by = 12
    
    def get_queryset(self):
        ProdCreatina = super().get_queryset() 
        ProdCreatina = ProdCreatina.filter(categoria='Creatina').order_by('-id') 
        return ProdCreatina


class Pretreino(ListView):
    model = models.Produto
    template_name = 'produto/pretreino.html'
    context_object_name = 'produtos'
    paginate_by = 12
    
    def get_queryset(self):
        ProdPretreino = super().get_queryset() 
        ProdPretreino = ProdPretreino.filter(categoria='Pretreino').order_by('-id') 
        return ProdPretreino


class Termo(ListView):
    model = models.Produto
    template_name = 'produto/termo.html'
    context_object_name = 'produtos'
    paginate_by = 12
    
    def get_queryset(self):
        ProdTermo = super().get_queryset() 
        ProdTermo = ProdTermo.filter(categoria='Termo').order_by('-id') 
        return ProdTermo


class Hiper(ListView):
    model = models.Produto
    template_name = 'produto/hiper.html'
    context_object_name = 'produtos'
    paginate_by = 12
    
    def get_queryset(self):
        ProdHiper = super().get_queryset() 
        ProdHiper = ProdHiper.filter(categoria='Hiper').order_by('-id') 
        return ProdHiper


class Endurance(ListView):
    model = models.Produto
    template_name = 'produto/endurance.html'
    context_object_name = 'produtos'
    paginate_by = 12
    
    def get_queryset(self):
        ProdEndurance = super().get_queryset() 
        ProdEndurance = ProdEndurance.filter(categoria='Endurance').order_by('-id') 
        return ProdEndurance


class Outro(ListView):
    model = models.Produto
    template_name = 'produto/outro.html'
    context_object_name = 'produtos'
    paginate_by = 12
    
    def get_queryset(self):
        ProdOutro = super().get_queryset() 
        ProdOutro = ProdOutro.filter(categoria='Outro').order_by('-id') 
        return ProdOutro    

class Finalizar(View):
    pass