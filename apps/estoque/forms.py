from django import forms
from .models import Produto, Marca, Categoria, Fornecedor


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'categoria', 'marca', 'preco_venda', 'estoque_minimo', 'imagem_principal']


class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nome']


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome']


class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ['nome_fantasia', 'cnpj_cpf', 'telefone', 'email']
