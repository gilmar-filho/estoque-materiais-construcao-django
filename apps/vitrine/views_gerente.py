from functools import wraps
from django.db import models
from django.shortcuts import render, redirect
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
