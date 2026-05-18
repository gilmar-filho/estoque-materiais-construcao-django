from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver(post_save, sender='vitrine.ItemReserva')
def adicionar_reserva(sender, instance, created, **kwargs):
    if created:
        instance.produto.quantidade_reservada += instance.quantidade
        instance.produto.save()

@receiver(post_delete, sender='vitrine.ItemReserva')
def remover_reserva(sender, instance, **kwargs):
    instance.produto.quantidade_reservada -= instance.quantidade
    instance.produto.save()