from django.db import models
from django.conf import settings
from apps.estoque.models import Produto

class Reserva(models.Model):
    STATUS_CHOICES = (
        ('PENDENTE', 'Pendente (Reservado)'),
        ('CONCLUIDO', 'Concluído (Retirada)'),
        ('CANCELADO', 'Cancelado'),
    )
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    data_reserva = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDENTE')
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Reserva #{self.id} ({self.status})"

class ItemReserva(models.Model):
    reserva = models.ForeignKey(Reserva, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.IntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"