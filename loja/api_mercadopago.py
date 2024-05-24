import mercadopago

public_key = 'TEST-782abbf2-028c-4c73-889c-e4304757293b'
access_token = 'TEST-6553658564379008-052411-d2fe2367d296076447945a1f9ca91c41-630114112'
def criar_pagamento(itens_pedido, link):
    # Configure as credenciais
    sdk = mercadopago.SDK(access_token)
    # Crie um item na preferencia


    # itens do cliente  no formato de dicionario
    itens = []
    for item in itens_pedido:
        quantidade = int(item.quantidade)
        nome_produto = str(item.item_estoque.produto.nome_produto)
        preco_unitario = float(item.item_estoque.produto.preco)
        itens.append({
            "title": nome_produto,
            "quantity": quantidade,
            "unit_price": preco_unitario,
        })
    preference_data = {
        "items": itens,

        "back_urls": {
            "success": '',
            "pending": '',
            "failure": '',
        }
    }
    resposta = sdk.preference().create(preference_data)
    link = resposta['response']['init_point']
    id_pagamento = resposta["response"]["id"]

    print(link, id_pagamento)

