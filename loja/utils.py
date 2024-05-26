from django.db.models import Max, Min
from django.core.mail import send_mail



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
        lista_produtos = sorted(lista_produtos, reverse=True, key=lambda tupla: tupla[0])
        produtos = [item[1] for item in lista_produtos]
    return produtos

def enviar_email_compra(pedido):
    email = pedido.cliente.email
    assunto = f'Compra Aprovado: {pedido.id}'
    corpo = f"""PARABÈNS! Seu Compra foi Aprovado.
                        ID do Pedido: {pedido.id}
                        Valor Total da Compra: {pedido.preco_total}"""
    remetente = 'milindobruto2@gmail.com'
    send_mail(assunto, corpo, remetente, [email])