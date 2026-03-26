from django.template import Library
from utils.formatapreco import formata_preco as formatar

register = Library()

@register.filter
def formata_preco(preco):
    return formatar(preco)