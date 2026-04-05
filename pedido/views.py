from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views import View
from django.contrib import messages 

from produto.models import Variacao
from .models import Pedido, ItemPedido
from produto import context_processors

class Pagar(View):
    template_name = 'pedido/pagar.html'
    
    def get(self, request, *arg, **kwargs):
        
        if not request.user.is_authenticated:
            messages.error(
                request,
                'Faça o login para acessar pagamentos'
            )
            return redirect('perfil:login')
        
        if not request.session.get('carrinho'):
            messages.error(
                request,
                'Coloque produtos no carrinho para acessar pagamentos'
            )
            return redirect('produto:lista')
        
        carrinho = request.session.get('carrinho')
        carrinho_variacoes_ids = [ids for ids in carrinho]
        bd_variacao = list(Variacao.objects.select_related('produto').filter(id__in=carrinho_variacoes_ids))
        
        for variacao in bd_variacao:
            id = str(variacao.id)
            estoque = variacao.estoque
            qtd_carrinho = carrinho[id]['quantidade']
            preco_unt = carrinho[id]['preco_unitario']
            preco_unt_promo = carrinho[id]['preco_unitario_promocional']
            
            if estoque < qtd_carrinho:
                carrinho[id]['quantidade'] = estoque
                carrinho[id]['preco_quantitativo'] = estoque * preco_unt
                carrinho[id]['preco_quantitativo_promocional'] = estoque * preco_unt_promo
                
                messages.error(
                    request,
                    'Estoque insuficiente para alguns produtos. Quantidades ajustadas automaticamente.'
                )
                request.session.save()
                return redirect('produto:carrinho')
            
        dados_carrinho = context_processors.carrinho(request)
        qnt_itens_carrinho = dados_carrinho['total_itens_carrinho']
        valor_total_carrinho = dados_carrinho['valor_total_carrinho']

        pedido = Pedido(
            usuario=request.user,
            qnt_total=qnt_itens_carrinho,
            total=valor_total_carrinho,
            status='C'
        )

        pedido.save()
        
        ItemPedido.objects.bulk_create(
            [
                ItemPedido(
                    pedido=pedido,
                    produto=i['produto_nome'],
                    produto_id=i['produto_id'],
                    variacao=i.get('variacao_nome') or '',
                    variacao_id=i['variacao_id'],
                    preco=i['preco_quantitativo'],
                    preco_promocional=i['preco_quantitativo_promocional'],
                    quantidade=i['quantidade'],
                    imagem=i['imagem']
                ) for i in carrinho.values()
            ]
        )
        del request.session['carrinho']
        
        return render(request, self.template_name, contexto)

class Salvar(View):
    pass

class Detalhe(View):
    pass