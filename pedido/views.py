from django.shortcuts import render, redirect, reverse
from django.views.generic import DetailView
from django.views import View
from django.contrib import messages 
from django.http import HttpResponse
from produto.models import Variacao
from .models import Pedido, ItemPedido
from produto import context_processors

import mercadopago
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
class Pagar(DetailView):
    template_name = 'pedido/pagar.html'
    model = Pedido
    pk_url_kwarg = 'pk'
    context_object_name = 'pedido'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        pedido = self.get_object()

        
        sdk = mercadopago.SDK(settings.MERCADO_PAGO_TOKEN)

        
        preference_data = {
            "items": [
                {
                    "title": f"Pedido #{pedido.pk} - Smart Suplementos",
                    "quantity": 1,
                    "unit_price": float(pedido.total), 
                }
            ],
            "external_reference": str(pedido.pk),   
            "back_urls": {
                "success": "https://jill-unchastened-stewart.ngrok-free.dev/pedido/retorno/",
                "failure": "https://jill-unchastened-stewart.ngrok-free.dev/pedido/retorno/",
                "pending": "https://jill-unchastened-stewart.ngrok-free.dev/pedido/retorno/"
            },
            # TODO remover a fazer deploy para teste do mercado pago 
            " auto_return": "approved",
        }

        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]

        #TODO debug mercado pago
        if 'init_point' not in preference:
            print(" ERRO DO MERCADO PAGO")
            print(preference) 
            contexto['link_pagamento'] = "#" 
        else:
            contexto['link_pagamento'] = preference['init_point']
        
        return contexto
class Salvar(View):
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
        
        return redirect(
            reverse(
                'pedido:pagar',
                kwargs= {'pk': pedido.pk
                }
            )
        )
        
class RetornoPagamento(View):
    def get(self, request, *args, **kwargs):
        status = request.GET.get('status')
        
        if status == 'approved':
            messages.success(request, 'Pagamento aprovado! Você pode chegar na aba pedidos no perfil')
        elif status == 'pending':
            messages.warning(request, 'Seu pagamento está em análise pelo Mercado Pago.')
        else:
            messages.error(request, 'O pagamento não foi concluído. Tente novamente.')

        return redirect('produto:lista')

@csrf_exempt
def MercadoPago(request):
    resource_id = None
    topic = None

    if request.method == 'POST' and request.body:
        try:
            data = json.loads(request.body)
            resource_id = data.get('id') or data.get('data', {}).get('id')
            topic = data.get('type') or data.get('action')
        except: pass
    
    if not resource_id:
        resource_id = request.GET.get('id') or request.GET.get('data.id')
        topic = request.GET.get('topic') or request.GET.get('type')

    if resource_id:
        sdk = mercadopago.SDK(settings.MERCADO_PAGO_TOKEN)
        resposta = None
        
        if 'payment' in str(topic):
            payment_info = sdk.payment().get(resource_id)
            if payment_info["status"] in [200, 201]:
                resposta = payment_info["response"]
        
        elif 'order' in str(topic):
            order_info = sdk.merchant_order().get(resource_id)
            if order_info["status"] in [200, 201]:
                
                res_order = order_info["response"]
                for p in res_order.get('payments', []):
                    if p.get('status') == 'approved':
                        resposta = res_order
                        break

        if resposta:
            pedido_id = resposta.get('external_reference')
            status_mp = resposta.get('status') 

            if pedido_id and (status_mp == 'approved' or status_mp == 'closed'):
                try:
                    pedido = Pedido.objects.get(pk=pedido_id)
                    if pedido.status != 'A': 
                        pedido.status = 'A'
                        pedido.save()
                        print(f" {pedido_id} aprovado via Webhook!")
                except Pedido.DoesNotExist:
                    print(f"{pedido_id} não encontrado.")

    return HttpResponse(status=200)
class Lista(View):
    def get(self, request, *arg, **kwargs):
        return HttpResponse('lista')
class Detalhe(View):
    pass