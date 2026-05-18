from django.contrib import admin, messages
from django.db import transaction
from unfold.admin import ModelAdmin, TabularInline
from .models import Reserva, ItemReserva

class ItemReservaInline(TabularInline):
    model = ItemReserva
    extra = 1

@admin.register(Reserva)
class ReservaAdmin(ModelAdmin):
    list_display = ('id', 'cliente', 'status', 'data_reserva')
    inlines = [ItemReservaInline]

    def save_model(self, request, obj, form, change):
        try:
            with transaction.atomic():
                if change:
                    reserva_antiga = Reserva.objects.get(pk=obj.pk)
                    if reserva_antiga.status != 'CONCLUIDO' and obj.status == 'CONCLUIDO':
                        for item in obj.itens.all():
                            if item.produto.quantidade_fisica < item.quantidade:
                                raise ValueError(f"Estoque físico insuficiente para o produto: {item.produto.nome}")
                            
                            item.produto.quantidade_fisica -= item.quantidade
                            item.produto.quantidade_reservada -= item.quantidade
                            item.produto.save()
                            
                super().save_model(request, obj, form, change)
                
        except ValueError as erro:
            messages.set_level(request, messages.ERROR)
            messages.error(request, str(erro))
            obj.status = 'PENDENTE'
            super().save_model(request, obj, form, change)