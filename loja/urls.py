import checkout
from django.urls import path
from .views import *

urlpatterns = [
    path('', homepage, name='homepage'),
    path('loja/', loja, name='loja'),
    path('sacola/', sacola, name='sacola'),
    path('minhaconta/', minha_conta, name='minha_conta'),
    path('login/', login, name='login'),
    path('checkout/', checkout, name='checkout'),
]