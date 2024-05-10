import checkout
from django.urls import path
from .views import *

urlpatterns = [
    path('', homepage, name='homepage'),
    path('loja/', loja, name='loja'),
    path('loja/<str:nome_categoria>/', loja, name="loja"),
    path('produto/<str:id_produto>/', ver_produto, name="ver_produto"),
    path('produto/<str:id_produto>/<int:id_cor>/', ver_produto, name="ver_produto"),
    path('sacola/', sacola, name='sacola'),
    path('minhaconta/', minha_conta, name='minha_conta'),
    path('login/', login, name='login'),
    path('checkout/', checkout, name='checkout'),
]