from django.urls import path
from . import views, views_gerente

urlpatterns = [
    path('gerente/', views_gerente.gerente_dashboard, name='gerente_dashboard'),

    path('', views.catalogo, name='catalogo'),

    path(
        'carrinho/adicionar/<int:produto_id>/',
        views.adicionar_carrinho,
        name='adicionar_carrinho'
    ),
        path(
        'carrinho/remover/<int:produto_id>/',
        views.remover_carrinho,
        name='remover_carrinho'
    ),

    path('carrinho/', views.carrinho, name='carrinho'),
    path('checkout/', views.checkout, name='checkout'),
    path('login/', views.login_cliente, name='login'),
    path('cadastro/', views.cadastro_cliente, name='cadastro'),
]