from django.urls import path
from . import views

app_name = "pedido"

urlpatterns = [
    path('pagar/<int:pk>', views.Pagar.as_view(), name='pagar'),
    path('lista/', views.Lista.as_view(), name='lista'),
    path('salvar/', views.Salvar.as_view(), name="salvar"),
    path('detalhe/', views.Detalhe.as_view(), name = "detalhe"),
    path('retorno/', views.RetornoPagamento.as_view(), name='retorno'),
]

