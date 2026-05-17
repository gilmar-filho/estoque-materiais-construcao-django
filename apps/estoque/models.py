from django.db import models
from cloudinary.models import CloudinaryField

class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Marca(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Fornecedor(models.Model):
    nome_fantasia = models.CharField(max_length=255)
    cnpj_cpf = models.CharField(max_length=20, unique=True)
    telefone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.nome_fantasia

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    imagem_principal = CloudinaryField('imagem')
    
    # Controle de Estoque via Signals
    quantidade_fisica = models.IntegerField(default=0)
    quantidade_reservada = models.IntegerField(default=0)
    estoque_minimo = models.IntegerField(default=5)

    def __str__(self):
        return f"{self.nome} - {self.marca.nome}"

class MovimentacaoEstoque(models.Model):
    TIPO_CHOICES = (
        ('ENTRADA', 'Entrada'),
        ('SAIDA', 'Saída'),
        ('AJUSTE_PERDA', 'Ajuste/Perda'),
    )

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES)
    quantidade = models.IntegerField()
    custo_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True, blank=True)
    data_movimentacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} - {self.produto.nome} ({self.quantidade} un)"