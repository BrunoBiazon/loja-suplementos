from django.urls import path
from . import views

app_name = 'produto'

urlpatterns = [
    path('', views.ListaProdutos.as_view(), name= "lista"),
    path('<slug>', views.Detalheproduto.as_view(), name= "detalhe"),
    path('adiconaraocarrinho/', views.AdicionarAoCarrinho.as_view(), name= "adicionaraocarrinho"),
    path('removerdocarrinho/', views.RemoverDoCarrinho.as_view(), name= "removerdocarrinho"),
    path('carrinho/', views.Carrinho.as_view(), name= "carrinho"),
    path('finalizar/', views.Finalizar.as_view(), name= "finalizar"),
    path('promocao/', views.Promocao.as_view(), name= "promocao"),
    path('snacks/', views.Snacks.as_view(), name="snacks"),
    path('whey/', views.Whey.as_view(), name="whey"),
    path('saude/', views.Saude.as_view(), name="saude"),
    path('creatina/', views.Creatina.as_view(), name="creatina"),
    path('pretreino/', views.Pretreino.as_view(), name="pretreino"),
    path('termo/', views.Termo.as_view(), name="termo"),
    path('hiper/', views.Hiper.as_view(), name="hiper"),
    path('endurance/', views.Endurance.as_view(), name="endurance"),
    ]   