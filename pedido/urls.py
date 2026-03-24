from django.urls import path
from . import views

app_name = "pedido"

urlpatterns = [
    path('', views.Pagar.as_view(), name="Pagar"), 
    path('fecharpedido/', views.FecharPedido.as_view(), name="fecharpedido"),
    path('detalhepedido/', views.DetalhePedido.as_view(), name = "detalhepedido"),
]

