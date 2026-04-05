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
        http_referer = request.META.get('HTTP_REFERER', '/')
        
        variacao_id = request.GET.get('vid')

        if not variacao_id:
            messages.error(
                request,
                f'O produto não foi encontrado',
            )
            
            return redirect(http_referer)
            
        if not request.session.get('carrinho'):
            messages.error(
                request,
                f'Erro ao tentar remover do carrinho',
            )            
            return redirect(http_referer)

        if variacao_id not in request.session['carrinho']:
            messages.error(
                request,
                f'O produto não foi encontrado no carrinho',
            )                 
            return redirect(http_referer)

        carrinho = request.session['carrinho']
        produto_nome = carrinho[variacao_id]['produto_nome'] 
        
        del carrinho[variacao_id]

        request.session.modified = True
        
        messages.success(
            request,
            f'O produto {produto_nome} foi removido do carrinho.'
            )
        return redirect(http_referer)
class Carrinho(ListView):
    def get(self, request, *args, **kwargs):
        return render(request, 'produto/carrinho.html')

class ResumoCompra(View):
    def get(self, request, *args, **kwargs):
        
        if not request.request.user.is_authenticated:
            messages.error(
                request,
                'Faça o login para acessar pagamentos'
                
            )
            return redirect('perfil:login')
        
        if not request.request.session.get('carrinho'):
            messages.error(
                request,
                'Coloque produtos no carrinho para acessar resumo da compra'
                
            )
            return redirect('produto:lista')

        contexto = {
            'usuario': request.user,
            'perfil': request.user.perfil,
            'carrinho': request.session['carrinho'],
        }
        
        return render(request, 'produto/resumocompra.html', contexto)
    
    
class BaseCategoria(ListView):
    model = models.Produto
    context_object_name = 'produtos'
    paginate_by = 12
    template_name = 'produto/categoria.html'

    categoria = None

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.categoria:
            queryset = queryset.filter(categoria=self.categoria)

        return queryset.order_by('-id')
    

class Promocao(BaseCategoria):
    template_name = 'produto/promocao.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(promocao_relampago='S')
    
class Snacks(BaseCategoria):
    template_name = 'produto/snacks.html'
    categoria = 'Snacks'


class Whey(BaseCategoria):
    template_name = 'produto/whey.html'
    categoria = 'Whey'


class Saude(BaseCategoria):
    template_name = 'produto/saude.html'
    categoria = 'Saude'


class Creatina(BaseCategoria):
    template_name = 'produto/creatina.html'
    categoria = 'Creatina'


class Pretreino(BaseCategoria):
    template_name = 'produto/pretreino.html'
    categoria = 'Pretreino'


class Termo(BaseCategoria):
    template_name = 'produto/termo.html'
    categoria = 'Termo'


class Hiper(BaseCategoria):
    template_name = 'produto/hiper.html'
    categoria = 'Hiper'


class Endurance(BaseCategoria):
    template_name = 'produto/endurance.html'
    categoria = 'Endurance'


class Outro(BaseCategoria):
    template_name = 'produto/outro.html'
    categoria = 'Outro'

