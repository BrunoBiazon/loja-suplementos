from django.urls import path
from . import views

app_name = "pedido"

urlpatterns = [
    path('pagar/', views.Pagar.as_view(), name='pagar'),
    path('salvar/', views.Salvar.as_view(), name="salvar"),
    path('detalhe/', views.Detalhe.as_view(), name = "detalhe"),
]

