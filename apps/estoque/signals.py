from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.estoque.models import MovimentacaoEstoque

@receiver(post_save, sender='vitrine.ItemReserva')
def adicionar_reserva(sender, instance, created, **kwargs):
    if created:
        instance.produto.quantidade_reservada += instance.quantidade
        instance.produto.save()

@receiver(post_delete, sender='vitrine.ItemReserva')
def remover_reserva(sender, instance, **kwargs):
    instance.produto.quantidade_reservada -= instance.quantidade
    instance.produto.save()

@receiver(post_save, sender=MovimentacaoEstoque)
def atualizar_estoque_fisico(sender, instance, created, **kwargs):
    if not created:
        return
    
    produto = instance.produto
    
    if instance.tipo == 'ENTRADA':
        produto.quantidade_fisica += instance.quantidade
    elif instance.tipo in ('SAIDA', 'AJUSTE_PERDA'):
        produto.quantidade_fisica -= instance.quantidade
    
    produto.save()