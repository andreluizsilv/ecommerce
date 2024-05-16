from django.db.models import Max, Min


def filtrar_produtos(produtos, filtro):
    if filtro:
        if "-" in filtro:
            categoria, tipo = filtro.split("-")
            produtos = produtos.filter(tipo__slug=tipo, categoria__slug=categoria)
        else:
            produtos = produtos.filter(categoria__slug=filtro)
    return produtos


def preco_minimo_maximo(produtos):
    minimo = 0
    maximo = 0
    if len(produtos) > 0:
        minimo = list(produtos.aggregate(Min("preco")).values())[0]
        minimo = round(minimo, 2)
        maximo = list(produtos.aggregate(Max("preco")).values())[0]
        maximo = round(maximo, 2)
    return minimo, maximo

def ordenar_produtos(produtos, ordem):
    if ordem == 'menor-preco':
        produtos = produtos.order_by('preco')
    elif ordem == 'maior-preco':
        produtos = produtos.order_by('-preco')
    elif ordem == 'mais-vendido':
        lista_produtos = []
        for produto in produtos:
            lista_produtos.append((produto.total_vendas(), produto))
        lista_produtos = sorted(lista_produtos, reverse=True)
        produtos = [item[1] for item in lista_produtos]
    return produtos