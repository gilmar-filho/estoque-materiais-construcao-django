from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from unfold.admin import ModelAdmin
from .models import Categoria, Marca, Fornecedor, Produto, MovimentacaoEstoque

class MovimentacaoEstoqueForm(forms.ModelForm):
    class Meta:
        model = MovimentacaoEstoque
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        fornecedor = cleaned_data.get('fornecedor')

        if tipo == 'ENTRADA' and not fornecedor:
            raise ValidationError("Toda ENTRADA de estoque exige um fornecedor atrelado.")
        
        return cleaned_data

@admin.register(Produto)
class ProdutoAdmin(ModelAdmin):
    list_display = ('nome', 'categoria', 'marca', 'preco_venda', 'quantidade_fisica', 'quantidade_reservada')
    search_fields = ('nome', 'marca__nome')
    list_filter = ('categoria', 'marca')
    readonly_fields = ('quantidade_fisica', 'quantidade_reservada')
    fieldsets = (
        ('Identificação', {'fields': ('nome', 'categoria', 'marca', 'imagem_principal')}),
        ('Preço e Estoque', {'fields': ('preco_venda', 'estoque_minimo', 'quantidade_fisica', 'quantidade_reservada')}),
    )

@admin.register(MovimentacaoEstoque)
class MovimentacaoEstoqueAdmin(ModelAdmin):
    form = MovimentacaoEstoqueForm
    list_display = ('tipo', 'produto', 'quantidade', 'custo_unitario', 'fornecedor', 'data_movimentacao')
    list_filter = ('tipo', 'data_movimentacao', 'produto__categoria', 'fornecedor')
    date_hierarchy = 'data_movimentacao'

@admin.register(Categoria)
class CategoriaAdmin(ModelAdmin):
    search_fields = ('nome',)

@admin.register(Marca)
class MarcaAdmin(ModelAdmin):
    search_fields = ('nome',)

@admin.register(Fornecedor)
class FornecedorAdmin(ModelAdmin):
    list_display = ('nome_fantasia', 'cnpj_cpf', 'telefone')
    search_fields = ('nome_fantasia', 'cnpj_cpf')