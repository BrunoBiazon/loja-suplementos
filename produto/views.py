from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse

class ListaProdutos(ListView):
    def get(self, request, *args, **kwargs):
        return HttpResponse("<h1>teste</h1>")

class Detalheproduto(View):
    pass

class AdicionarAoCarrinho(View):
    pass
class RemoverDoCarrinho(View):
    pass

class Carrinho(View):
    pass
class Finalizar(View):
    pass