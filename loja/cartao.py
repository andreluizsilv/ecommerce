from PIL import Image, ImageDraw, ImageFont
from datetime import date
import random
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings
import os
from .models import Cliente, Cartao


def gerar_numero_cartao():
    return ' '.join(f"{random.randint(1000, 9999)}" for _ in range(4))


def gerar_cartao_cliente(cliente_id):
    try:
        # Busca o cliente no banco de dados
        cliente = Cliente.objects.get(id=cliente_id)

        # Gera os detalhes do cartão
        numero_cartao = gerar_numero_cartao()
        mes = date.today().month
        ano = date.today().year + 5
        validade = f"{mes:02d}/{ano % 100:02d}"

        # Caminho absoluto para a imagem do cartão
        imagem_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'cartaodecredito.jpg')

        # Verifica se a imagem existe
        if not os.path.exists(imagem_path):
            print(f"Imagem não encontrada no caminho: {imagem_path}")
            return None

        # Cria a imagem do cartão
        imagem_cartao = Image.open(imagem_path)

        # Caminho absoluto para a fonte
        fonte_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'Heavitas.ttf')

        # Verifica se a fonte existe
        if not os.path.exists(fonte_path):
            print(f"Fonte não encontrada no caminho: {fonte_path}")
            return None

        # Carrega a fonte
        fonte = ImageFont.truetype(fonte_path, 60)

        # Adiciona os textos na imagem
        draw = ImageDraw.Draw(imagem_cartao)
        draw.text((150, 52), numero_cartao, font=fonte)
        draw.text((150, 72), cliente.nome_cliente, font=fonte)
        draw.text((150, 92), validade, font=fonte)

        # Salva a imagem diretamente na memória
        imagem_io = BytesIO()
        imagem_cartao.save(imagem_io, format='JPEG')
        imagem_content = ContentFile(imagem_io.getvalue(), name=f'imagemcartao_{cliente.id}.jpg')

        # Cria e salva o registro do cartão no banco de dados
        novo_cartao = Cartao(
            cartao_cliente=cliente,
            numero_cartao=numero_cartao,
            validade_cartao=validade,
            images_cartao=imagem_content
        )
        novo_cartao.save()

        return novo_cartao

    except Cliente.DoesNotExist:
        print("Cliente não encontrado")
        return None
