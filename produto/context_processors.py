def carrinho(request):
    carrinho_data = request.session.get('carrinho', {})
    
    total_itens = sum(item.get('quantidade', 0) for item in carrinho_data.values())
    valor_total = sum(float(item.get('preco_quantitativo_promocional', 0)) for item in carrinho_data.values())
    
    return {
        'carrinho': carrinho_data,
        'total_itens_carrinho': total_itens,
        'valor_total_carrinho': valor_total,
}