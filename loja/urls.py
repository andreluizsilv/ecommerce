import checkout
from django.urls import path
from .views import *

urlpatterns = [
    path('', homepage, name='homepage'),
    path('loja/', loja, name='loja'),
    path('loja/<str:filtro>/', loja, name="loja"),
    path('produto/<str:id_produto>/', ver_produto, name="ver_produto"),
    path('produto/<str:id_produto>/<int:id_cor>/', ver_produto, name="ver_produto"),
    path('sacola/', sacola, name='sacola'),
    path('minhaconta/', minha_conta, name='minha_conta'),
    path('login/', login, name='login'),
    path('checkout/', checkout, name='checkout'),
    path('adicionarsacola/<int:id_produto>/', adicionar_sacola, name='adicionar_sacola'),
    path('removersacola/<int:id_produto>/', remover_sacola, name='remover_sacola'),
    path('adicionarendereco/', adicionar_endereco, name='adicionar_endereco'),
]

