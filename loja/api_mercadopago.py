#import mercadopago

public_key = 'TEST-782abbf2-028c-4c73-889c-e4304757293b'
access_token = 'TEST-6553658564379008-052411-d2fe2367d296076447945a1f9ca91c41-630114112'

def criar_pagamento(itens_pedido, link, external_reference):
    # Configure as credenciais
    sdk = mercadopago.SDK(access_token)

    # Crie um item na preferência
    itens = []
    for item in itens_pedido:
        quantidade = int(item.quantidade)
        nome_produto = item.item_estoque.produto.nome_produto
        preco_unitario = float(item.item_estoque.produto.preco)
        itens.append({
            "title": nome_produto,
            "quantity": quantidade,
            "unit_price": preco_unitario,
            "currency_id": "BRL"
        })

    # Dados da preferência
    preference_data = {
        "items": itens,
        "auto_return": "approved",
        "back_urls": {
            "success": link,
            "pending": link,
            "failure": link,
        },
        "external_reference": external_reference
    }

    resposta = sdk.preference().create(preference_data)
    link_pagamento = resposta["response"]["init_point"]
    id_pagamento = resposta["response"]["id"]
    return link_pagamento, id_pagamento
