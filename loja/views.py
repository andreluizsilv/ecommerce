from django.shortcuts import render

# Create your views here.
def homepage(request):
    return render(request, 'homepage.html')


def loja(request):
    return render(request, 'loja.html')


def sacola(request):
    return render(request, 'sacola.html')


def checkout(request):
    return render(request, 'checkout.html')


def minha_conta(request):
    return render(request, 'usuario/minha_conta.html')


def login(request):
    return render(request, 'usuario/login.html')


