from django import forms
from .models import Produto, Marca, Categoria, Fornecedor

_input = 'w-full px-4 py-2.5 rounded-xl border border-stone-300 dark:border-stone-600 bg-white dark:bg-stone-900 text-stone-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-orange-500 text-sm'
_select = _input


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'categoria', 'marca', 'preco_venda', 'estoque_minimo', 'imagem_principal']
        widgets = {
            'nome': forms.TextInput(attrs={'class': _input}),
            'categoria': forms.Select(attrs={'class': _select}),
            'marca': forms.Select(attrs={'class': _select}),
            'preco_venda': forms.NumberInput(attrs={'class': _input, 'step': '0.01'}),
            'estoque_minimo': forms.NumberInput(attrs={'class': _input}),
        }


class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nome']
        widgets = {'nome': forms.TextInput(attrs={'class': _input, 'placeholder': 'Nome da marca'})}


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome']
        widgets = {'nome': forms.TextInput(attrs={'class': _input, 'placeholder': 'Nome da categoria'})}


class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ['nome_fantasia', 'cnpj_cpf', 'telefone', 'email']
        widgets = {
            'nome_fantasia': forms.TextInput(attrs={'class': _input, 'placeholder': 'Nome fantasia'}),
            'cnpj_cpf': forms.TextInput(attrs={'class': _input, 'placeholder': 'CNPJ ou CPF'}),
            'telefone': forms.TextInput(attrs={'class': _input, 'placeholder': 'Telefone'}),
            'email': forms.EmailInput(attrs={'class': _input, 'placeholder': 'E-mail'}),
        }
