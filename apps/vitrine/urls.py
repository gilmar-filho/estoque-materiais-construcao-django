from django.urls import path
from . import views, views_gerente

urlpatterns = [
    path('gerente/', views_gerente.gerente_dashboard, name='gerente_dashboard'),
    path('gerente/reservas/', views_gerente.gerente_reservas, name='gerente_reservas'),
    path('gerente/reservas/<int:reserva_id>/confirmar/', views_gerente.gerente_confirmar_reserva, name='gerente_confirmar_reserva'),
    path('gerente/reservas/<int:reserva_id>/cancelar/', views_gerente.gerente_cancelar_reserva, name='gerente_cancelar_reserva'),
    path('gerente/produtos/', views_gerente.gerente_produtos, name='gerente_produtos'),
    path('gerente/produtos/novo/', views_gerente.gerente_produto_form, name='gerente_produto_novo'),
    path('gerente/produtos/<int:produto_id>/editar/', views_gerente.gerente_produto_form, name='gerente_produto_editar'),

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