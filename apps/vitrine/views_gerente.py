from functools import wraps
from django.contrib import messages
from django.db import models, transaction
from django.shortcuts import render, redirect, get_object_or_404
from apps.estoque.models import Produto
from apps.vitrine.models import Reserva


def gerente_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f'/login/?next={request.path}')
        if not request.user.is_staff:
            return redirect('catalogo')
        return view_func(request, *args, **kwargs)
    return wrapper


@gerente_required
def gerente_dashboard(request):
    stats = {
        'total_produtos': Produto.objects.count(),
        'reservas_pendentes': Reserva.objects.filter(status='PENDENTE').count(),
        'estoque_critico': Produto.objects.filter(
            quantidade_fisica__lte=models.F('estoque_minimo')
        ).count(),
    }
    return render(request, 'vitrine/gerente/dashboard.html', {'stats': stats})


@gerente_required
def gerente_reservas(request):
    reservas = (
        Reserva.objects
        .select_related('cliente')
        .prefetch_related('itens__produto')
        .annotate(
            ordem=models.Case(
                models.When(status='PENDENTE', then=0),
                models.When(status='CONCLUIDO', then=1),
                models.When(status='CANCELADO', then=2),
                default=3,
                output_field=models.IntegerField(),
            )
        )
        .order_by('ordem', '-data_reserva')
    )
    return render(request, 'vitrine/gerente/reservas.html', {'reservas': reservas})


@gerente_required
def gerente_confirmar_reserva(request, reserva_id):
    if request.method != 'POST':
        return redirect('gerente_reservas')

    reserva = get_object_or_404(Reserva, id=reserva_id, status='PENDENTE')

    try:
        with transaction.atomic():
            for item in reserva.itens.all():
                produto = item.produto
                if produto.quantidade_fisica < item.quantidade:
                    raise ValueError(f'Estoque insuficiente para "{produto.nome}" — disponível: {produto.quantidade_fisica}, necessário: {item.quantidade}.')
                produto.quantidade_fisica -= item.quantidade
                produto.quantidade_reservada -= item.quantidade
                produto.save()
            reserva.status = 'CONCLUIDO'
            reserva.save()
        messages.success(request, f'Reserva #{reserva.id} confirmada com sucesso.')
    except ValueError as erro:
        messages.error(request, str(erro))

    return redirect('gerente_reservas')


@gerente_required
def gerente_cancelar_reserva(request, reserva_id):
    if request.method != 'POST':
        return redirect('gerente_reservas')

    reserva = get_object_or_404(Reserva, id=reserva_id, status='PENDENTE')

    with transaction.atomic():
        for item in reserva.itens.all():
            produto = item.produto
            produto.quantidade_reservada -= item.quantidade
            produto.save()
        reserva.status = 'CANCELADO'
        reserva.save()

    messages.success(request, f'Reserva #{reserva.id} cancelada.')
    return redirect('gerente_reservas')
