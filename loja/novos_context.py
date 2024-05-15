from .models import *
def sacola(request):
    qtde_prod_sacola = 0
    if request.user.is_authenticated:
        cliente = request.user.cliente
    else:
        if request.COOKIES.get("id_sessao"):
            id_sessao = request.COOKIES.get("id_sessao")
            cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
        else:
            return {'qtde_prod_sacola': qtde_prod_sacola}
    pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
    itens_pedido = ItensPedido.objects.filter(pedido=pedido)
    for item in itens_pedido:
        qtde_prod_sacola += item.quantidade
    return {'qtde_prod_sacola': qtde_prod_sacola}


def categoria_tipos(request):
    categorias_navbar = Categoria.objects.all()
    tipos_navbar = Tipo.objects.all()
    return {'categorias_navbar': categorias_navbar, 'tipos_navbar': tipos_navbar}