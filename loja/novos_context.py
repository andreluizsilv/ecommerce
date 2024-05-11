from .models import *
def sacola(request):
    qtde_prod_sacola = 0
    if request.user.is_authenticated:
        cliente = request.user.cliente
    else:
        return {'qtde_prod_sacola': qtde_prod_sacola}
    pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
    itens_pedido = ItensPedido.objects.filter(pedido=pedido)
    for item in itens_pedido:
        qtde_prod_sacola += item.quantidade
    return {'qtde_prod_sacola': qtde_prod_sacola}