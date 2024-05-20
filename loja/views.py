from django.shortcuts import render, redirect
from .models import *
import uuid
from .utils import filtrar_produtos, preco_minimo_maximo, ordenar_produtos
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


# Create your views here.
def homepage(request):
    banners = Banner.objects.filter(ativo=True)
    context = {'banners': banners}
    return render(request, 'homepage.html', context)


def loja(request, filtro=None):
    produtos = Produto.objects.filter(ativo=True)
    produtos = filtrar_produtos(produtos, filtro)
    # aplicar os filtros no formulario
    if request.method == 'POST':
        dados = request.POST.dict()
        produtos = produtos.filter(preco__gte=dados.get('preco_minimo'), preco__lte=dados.get('preco_maximo'))
        if 'tamanho' in dados:
            itens = ItemEstoque.objects.filter(produto__in=produtos, tamanho=dados.get('tamanho'))
            ids_produtos = itens.values_list('produto', flat=True).distinct()
            produtos = produtos.filter(id__in=ids_produtos)
        if 'categoria' in dados:
            produtos = produtos.filter(categoria__slug=dados.get('categoria'))
        if 'tipo' in dados:
            produtos = produtos.filter(tipo__slug=dados.get('tipo'))
    itens = ItemEstoque.objects.filter(quantidade__gt=0, produto__in=produtos)
    tamanhos = itens.values_list('tamanho', flat=True).distinct()
    ids_categorias = produtos.values_list('categoria', flat=True).distinct()
    categorias = Categoria.objects.filter(id__in=ids_categorias)
    minimo, maximo = preco_minimo_maximo(produtos)

    ordem = request.GET.get('ordem', 'menor-preco')
    produtos = ordenar_produtos(produtos, ordem)

    context = {"produtos": produtos,
               "minimo": minimo,
               "maximo": maximo,
               "tamanhos": tamanhos,
               'categorias': categorias
               }
    return render(request, 'loja.html', context)


def ver_produto(request, id_produto, id_cor=None):
    tem_estoque = False
    cores = {}
    tamanhos = {}
    cor_selecionada = None
    if id_cor:
        cor_selecionada =Cor.objects.get(id=id_cor)
    produto = Produto.objects.get(id=id_produto)
    itens_estoque = ItemEstoque.objects.filter(produto=produto, quantidade__gt=0)
    if len(itens_estoque) > 0:
        tem_estoque = True
        cores = {item.cor for item in itens_estoque}
        if id_cor:
            itens_estoque = ItemEstoque.objects.filter(produto=produto, quantidade__gt=0, cor__id=id_cor)
            tamanhos = {item.tamanho for item in itens_estoque}
    context = {
        'produto': produto,
        'tem_estoque': tem_estoque,
        'cores': cores,
        'tamanhos': tamanhos,
        'cor_selecionada': cor_selecionada
    }
    return render(request, 'ver_produto.html', context)


def adicionar_sacola(request, id_produto):
    if request.method == "POST" and id_produto:
        dados = request.POST.dict()
        tamanho = dados.get("tamanho")
        id_cor = dados.get("cor")
        if not tamanho:
            return redirect('loja')

        resposta = redirect('sacola')

        # Verifica se o usuário está autenticado
        if request.user.is_authenticated:
            cliente = request.user.cliente
        else:
            # Verifica se existe id_sessao nos cookies
            id_sessao = request.COOKIES.get("id_sessao", str(uuid.uuid4()))
            cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
            resposta.set_cookie(key="id_sessao", value=id_sessao, max_age=60 * 60 * 24 * 30)

        # Obtém ou cria um pedido não finalizado
        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)

        item_estoque = ItemEstoque.objects.get(produto__id=id_produto, tamanho=tamanho, cor__id=id_cor)
        item_pedido, criado = ItensPedido.objects.get_or_create(item_estoque=item_estoque, pedido=pedido)
        item_pedido.quantidade += 1
        item_pedido.save()

        return resposta
    else:
        return redirect('loja')


def remover_sacola(request, id_produto):
    if request.method == "POST" and id_produto:
        dados = request.POST.dict()
        tamanho = dados.get("tamanho")
        id_cor = dados.get("cor")
        if not tamanho:
            return redirect('loja')

        if request.user.is_authenticated:
            cliente = request.user.cliente
        else:
            id_sessao = request.COOKIES.get("id_sessao")
            if not id_sessao:
                return redirect('loja')
            cliente, _ = Cliente.objects.get_or_create(id_sessao=id_sessao)

        pedido, _ = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
        item_estoque = ItemEstoque.objects.get(produto__id=id_produto, tamanho=tamanho, cor__id=id_cor)
        item_pedido, _ = ItensPedido.objects.get_or_create(item_estoque=item_estoque, pedido=pedido)

        item_pedido.quantidade -= 1
        item_pedido.save()

        if item_pedido.quantidade <= 0:
            item_pedido.delete()

        return redirect('sacola')
    else:
        return redirect('loja')


def sacola(request):
    if request.user.is_authenticated:
        cliente = request.user.cliente
    else:
        id_sessao = request.COOKIES.get("id_sessao")
        if not id_sessao:
            context = {"cliente_existente": False, "itens_pedido": None, "pedido": None}
            return render(request, 'sacola.html', context)
        cliente, _ = Cliente.objects.get_or_create(id_sessao=id_sessao)

    pedido, _ = Pedido.objects.get_or_create(cliente=cliente, finalizado=True)
    itens_pedido = ItensPedido.objects.filter(pedido=pedido)

    context = {"itens_pedido": itens_pedido, "pedido": pedido, "cliente_existente": True}
    return render(request, 'sacola.html', context)


def checkout(request):
    if request.user.is_authenticated:
        cliente = request.user.cliente
    else:
        if request.COOKIES.get("id_sessao"):
            id_sessao = request.COOKIES.get("id_sessao")
            cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
        else:
            return redirect('loja')
    pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=True)
    enderecos = Endereco.objects.filter(cliente=cliente)
    context = {"pedido": pedido, "enderecos": enderecos}
    return render(request, 'checkout.html', context)


def adicionar_endereco(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            cliente = request.user.cliente
        else:
            if request.COOKIES.get("id_sessao"):
                id_sessao = request.COOKIES.get("id_sessao")
                cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
            else:
                return redirect('loja')
        dados = request.POST.dict()
        endereco = Endereco.objects.create(cliente=cliente, rua=dados.get('rua'),
                                           numero=int(dados.get('numero')), cidade=dados.get('cidade'),
                                           estado=dados.get('estado'), cep=dados.get('cep'),
                                           complemento=dados.get('complemento'))
        endereco.save()
        return redirect('checkout')
    else:
        context = {}
        return render(request, 'adicionar_endereco.html', context)

@login_required
def minha_conta(request):
    erro = None
    alterado = False
    if request.method == 'POST':
        dados = request.POST.dict()
        if 'senha_atual' in dados:
            # está modificando a senha
            senha_atual = dados.get('senha_atual')
            nova_senha = dados.get('nova_senha')
            nova_senha_confirmacao = dados.get('nova_senha_confirmacao')
            # verificar se senha está certa
            if nova_senha == nova_senha_confirmacao:
                usuario = authenticate(request, username=request.user.email, password=senha_atual)
                if usuario:
                    usuario.set_password(nova_senha)
                    usuario.save()
                    alterado = True
                else:
                    erro = 'senha_incorreta'
            else:
                erro = 'senhas_diferentes'

        elif 'email' in dados:
            nome = dados.get('nome')
            email = dados.get('email')
            telefone = dados.get('telefone')
            if email != request.user.email:
                usuarios = User.objects.filter(email=email)
                if len(usuarios) > 0:
                    erro = 'email_existente'
            if not erro:
                cliente = request.user.cliente
                cliente.email = email
                request.user.email = email
                request.user.username = email
                cliente.nome_cliente = nome
                cliente.telefone = telefone
                cliente.save()
                request.user.save()
                alterado = True
        else:
            erro = 'formulario_invalido'
    context = {'erro': erro, 'alterado': alterado}
    return render(request, 'usuario/minha_conta.html', context)
@login_required
def meus_pedidos(request):
    cliente = request.user.cliente
    pedidos = Pedido.objects.filter(finalizado=True, cliente=cliente).order_by('-data_finalizacao')
    context = {'pedidos': pedidos}
    return render(request, 'usuario/meus_pedidos.html', context)


def fazer_login(request):
    erro = False
    if request.user.is_authenticated:
        return redirect('loja')

    if request.method == "POST":
        dados = request.POST.dict()
        if "email" in dados and "senha" in dados:
            email = dados.get("email")
            senha = dados.get("senha")
            usuario = authenticate(request, username=email, password=senha)
            if usuario:
                login(request, usuario)
                # Associação do cliente ao usuário
                if not hasattr(usuario, 'cliente'):
                    # Se o usuário não tem um cliente associado, crie um
                    Cliente.objects.create(usuario=usuario, email=email)
                return redirect('loja')
            else:
                erro = True
        else:
            erro = True

    context = {"erro": erro}
    return render(request, 'usuario/fazer_login.html', context)


def criar_conta(request):
    erro = None
    if request.user.is_authenticated:
        return redirect("loja")
    if request.method == "POST":
        dados = request.POST.dict()
        if "email" in dados and "senha" in dados and "confirmacao_senha" in dados:
            # criar conta
            email = dados.get("email")
            senha = dados.get("senha")
            confirmacao_senha = dados.get("confirmacao_senha")
            try:
                validate_email(email)
            except ValidationError:
                erro = "email_invalido"
            if senha == confirmacao_senha:
                # criar conta
                usuario, criado = User.objects.get_or_create(username=email, email=email)
                if not criado:
                    erro = "usuario_existente"
                else:
                    usuario.set_password(senha)
                    usuario.save()
                    # fazer o login
                    usuario = authenticate(request, username=email, password=senha)
                    login(request, usuario)
                    # criar o cliente
                    # verificar se existe o id_sessao nos cookies
                    if request.COOKIES.get("id_sessao"):
                        id_sessao = request.COOKIES.get("id_sessao")
                        cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
                    else:
                        cliente, criado = Cliente.objects.get_or_create(email=email)
                    cliente.usuario = usuario
                    cliente.email = email
                    cliente.save()
                    return redirect("loja")
            else:
                erro = "senhas_diferentes"
        else:
            erro = "preenchimento"

    context = {"erro": erro}
    return render(request, "usuario/criar_conta.html", context)

    context = {"erro": erro}
    return render(request, "usuario/criar_conta.html", context)

@login_required
def fazer_lougout(request):
    logout(request)
    return redirect('fazer_login')
