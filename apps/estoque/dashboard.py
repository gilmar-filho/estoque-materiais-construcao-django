from django.db import models
from django.utils import timezone
from apps.estoque.models import Produto, MovimentacaoEstoque
from apps.vitrine.models import Reserva


def dashboard_callback(request, context):
    hoje = timezone.now()
    context['stats'] = {
        'estoque_critico': Produto.objects.filter(
            quantidade_fisica__lte=models.F('estoque_minimo')
        ).count(),
        'reservas_pendentes': Reserva.objects.filter(status='PENDENTE').count(),
        'entradas_mes': MovimentacaoEstoque.objects.filter(
            tipo='ENTRADA',
            data_movimentacao__year=hoje.year,
            data_movimentacao__month=hoje.month,
        ).count(),
        'saidas_mes': MovimentacaoEstoque.objects.filter(
            tipo__in=['SAIDA', 'AJUSTE_PERDA'],
            data_movimentacao__year=hoje.year,
            data_movimentacao__month=hoje.month,
        ).count(),
    }
    return context
